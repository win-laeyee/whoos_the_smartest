"use client";

import { useEffect, useState } from "react";
import Layout from "../components/ui/layout";
import GeneratedText from "../components/generate/GeneratedText";
import { useRouter } from "next/navigation";
import { QuizGenerationOptions } from "@/app/interfaces/interface";
import { QuestionType } from "@/app/interfaces/type";
import { HttpError } from "../utils/errors";
import { auth } from "../firebase";
import QuizForm from "../components/quiz/QuizForm";
import OwlLoader from "../components/ui/OwlLoader";

const Page: React.FC = () => {
  const router = useRouter();
  const [formData, setFormData] = useState<QuizGenerationOptions>({
    number_of_questions: 10,
    question_types: ["multiple_choice"],
    difficulty_level: "mix",
    include_explanations: false,
    emphasis: "key_points",
    emphasis_custom: "",
    language: "English",
  });
  const [markdown, setMarkDown] = useState("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    console.log("Running useEffect to get markdown");
    getMarkdown();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    console.log(`Form field ${name} changed to ${value}`);
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const [error, setError] = useState<string>("");

  const handleQuestionType = (val: QuestionType[]) => {
    console.log("Question types selected: ", val);
    setFormData({
      ...formData,
      question_types: val,
    });
  };

  const handleNavigate = () => {
    console.log("Navigating to /quiz");
    router.push("/quiz");
  };

  const handleQuiz = async (e: React.FormEvent<HTMLFormElement>) => {
    console.log("Quiz form submitted with data:", formData);
    setIsLoading(true);
    e.preventDefault();

    setFormData({
      ...formData,
      number_of_questions: +formData?.number_of_questions,
    });

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          try {
            const token = await user.getIdToken();

            const response = await fetch(
              `${process.env.NEXT_PUBLIC_API_URL}/v1/api/get-quiz-from-uploaded-notes`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(formData),
              }
            );

            setIsLoading(false);
            if (response.ok) {
              const result = await response.json();
              console.log("Quiz generation successful:", result);
              localStorage.setItem("quiz", JSON.stringify(result));
              handleNavigate();
            } else {
              console.error("Error:", response.statusText, response.status);
              throw new HttpError(response.statusText, response.status);
            }
          } catch (fetchError) {
            setIsLoading(false);
            console.error("Fetch error:", fetchError);

            if (fetchError instanceof HttpError) {
              switch (fetchError.status) {
                case 400:
                  setError("Bad request. Please check your input.");
                  break;
                case 401:
                  setError("Unauthorized. Please log in.");
                  break;
                case 403:
                  setError("Forbidden. You do not have access.");
                  break;
                case 404:
                  setError(
                    "Not found. The requested resource could not be found."
                  );
                  break;
                case 413:
                  setError("Request entity too large.");
                  break;
                case 422:
                  setError(
                    "Unprocessable entity. The request was well-formed but unable to be followed due to semantic errors."
                  );
                  break;
                case 500:
                  setError(
                    "Internal server error. Please try again later. Gemini API resource limit may have been reached."
                  );
                  break;
                case 504:
                  setError(
                    "Gateway timeout. The server took too long to respond."
                  );
                  break;
                default:
                  setError(
                    "Generation failed. The request took too long to process. Please try again later. Note: The maximum duration allowed is 60 seconds."
                  );
                  break;
              }
            } else {
              setError(
                "An unexpected error occurred. The request took too long to process. Please try again later. Note: The maximum duration allowed is 60 seconds."
              );
            }
          }
        } else {
          setError("User is not authenticated.");
        }
      });
    } catch (authError) {
      setIsLoading(false);
      console.error("Authentication error:", authError);
      setError("Authentication failed.");
    }
  };

  const getMarkdown = () => {
    const summary = localStorage.getItem("summary");
    console.log("Retrieved summary from localStorage:", summary);

    if (summary) {
      try {
        const parsedSummary = JSON.parse(summary);
        console.log("Parsed summary:", parsedSummary);

        if (parsedSummary && parsedSummary.summarised_notes) {
          setMarkDown(parsedSummary.summarised_notes);
        } else {
          console.error(
            'Property "summarised_notes" not found in the parsed JSON.'
          );
          return null;
        }
      } catch (e) {
        console.error("Error parsing JSON:", e);
        return null;
      }
    } else {
      console.error("No summary found in localStorage.");
      return null;
    }
  };

  const downloadMarkdown = () => {
    console.log("Downloading markdown content");
    // Create a Blob with the markdown content
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });

    // Create an anchor element and simulate a click to trigger the download
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "content.md";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col bg-primary min-w-screen">
      <Layout />

      <div className="flex flex-col max-w-screen">
        <GeneratedText markdown={markdown} />

        <div className="flex flex-row items-center justify-center mt-5 gap-2">
          <button className="btn btn-secondary" onClick={downloadMarkdown}>
            Download
          </button>
        </div>
      </div>

      <div className="prose m-5 flex flex-col max-w-full items-center justify-center">
        <p className="mt-0 mb-2">
          Once you have reviewed, go ahead to quiz yourself!
        </p>
        <QuizForm
          text="Generate"
          formData={formData}
          handleChange={handleChange}
          handleQuestionType={handleQuestionType}
          handleSubmit={handleQuiz}
        />
      </div>
      {isLoading && (
        <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
          <OwlLoader text="Wisdom without the fluff..." />
        </div>
      )}
    </div>
  );
};

export default Page;
