"use client";
import { ChangeEvent, MouseEvent, useState } from "react";
import { auth } from "../../firebase";
import { QuestionProps } from "../../interfaces/props";
import { HttpError } from "../../utils/errors";
import OwlLoader from "../ui/OwlLoader";

const TextQuestion: React.FC<QuestionProps> = ({
  index,
  totalQuestion,
  question,
  answer,
  explanation,
  handleNext,
  handleComplete,
}) => {
  const [studentAnswer, setStudentAnswer] = useState("");
  const [hasSubmit, setHasSubmit] = useState(false);
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const [error, setError] = useState<string>("");

  const handleNextQuestion = () => {
    setHasSubmit(false);
    setResult("");
    setStudentAnswer("");
    handleNext();
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setStudentAnswer(e.target.value);
  };

  const handleSubmit = (e: MouseEvent<HTMLButtonElement>) => {
    setIsLoading(true);
    e.preventDefault();

    const data = {
      question_and_answer: {
        answer: answer,
        question: question,
      },
      student_answer: studentAnswer,
    };

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          try {
            const token = await user.getIdToken();

            const response = await fetch(
              `${process.env.NEXT_PUBLIC_API_URL}/v1/api/evaluate-student-answer`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(data),
              }
            );
            setIsLoading(false);

            if (response.ok) {
              const result = await response.json();
              console.log("Quiz answer successful", result);
              setHasSubmit(true);
              setResult(result.correctness);
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

  return (
    <div className="m-5 prose">
      <h1>Question {index}</h1>
      <p>{question}</p>
      <input
        type="text"
        placeholder="Enter answer"
        className="input input-bordered rounded-full border-black border-2 w-full my-2"
        onChange={handleChange}
        value={studentAnswer}
      />
      <div className="flex items-center justify-center">
        {!hasSubmit ? (
          <button
            className="btn btn-active btn-secondary mt-2"
            onClick={handleSubmit}
          >
            Submit
          </button>
        ) : (
          <div className="flex flex-col">
            {result ? (
              <p className="text-green-400">Correct! </p>
            ) : (
              <p className="text-red-400">Wrong!</p>
            )}
            <div>Answer: {answer} </div>
            {explanation && <div>Explanation: {explanation}</div>}
            {index !== totalQuestion ? (
              <button
                className="btn btn-active btn-secondary mt-2 self-center"
                onClick={handleNextQuestion}
              >
                Next
              </button>
            ) : (
              <button
                className="btn btn-active btn-secondary mt-2"
                onClick={handleComplete}
              >
                Finish
              </button>
            )}
          </div>
        )}
        {isLoading && (
          <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
            <OwlLoader text="From wise to wiser—one hoot at a time..." />
          </div>
        )}
      </div>
    </div>
  );
};

export default TextQuestion;
