"use client";

import { useEffect, useState } from "react";
import Layout from "../components/ui/layout";
import GeneratedText from "../components/generate/GeneratedText";
import { useRouter } from "next/navigation";
import { QuizGenerationOptions } from "@/app/interfaces/interface";
import { QuestionType } from "@/app/interfaces/type";
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
    getMarkdown();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleQuestionType = (val: QuestionType[]) => {
    setFormData({
      ...formData,
      question_types: val,
    });
  };

  const handleNavigate = () => {
    router.push("/quiz");
  };

  const handleQuiz = async (e: React.FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    e.preventDefault();

    setFormData({
      ...formData,
      number_of_questions: +formData?.number_of_questions,
    });

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          const token = await user.getIdToken();

          const response = await fetch(
            "http://0.0.0.0:8000/v1/api/get-quiz-from-uploaded-notes",
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
            console.log("Quiz generation successful", result);
            localStorage.setItem("quiz", JSON.stringify(result));
            handleNavigate();
          } else {
            console.error("", response.statusText);
          }
        }
      });
    } catch (error) {
      console.error("Error:", error);
      setIsLoading(false);
    }
  };

  const getMarkdown = () => {
    const summary = localStorage.getItem("summary");

    if (summary) {
      try {
        const parsedSummary = JSON.parse(summary);

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
          <OwlLoader />
        </div>
      )}
    </div>
  );
};

export default Page;
