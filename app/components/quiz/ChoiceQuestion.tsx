"use client";

import { MouseEvent, useState } from "react";
import { auth } from "../../firebase";
import { QuestionProps } from "../../interfaces/props";
import { HttpError } from "../../utils/errors";
import OwlLoader from "../ui/OwlLoader";

interface ColorChangingButtonProps {
  text: string;
  isSelected: boolean;
  onClick: () => void;
}

const ColorChangingButton: React.FC<ColorChangingButtonProps> = ({
  text,
  isSelected,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      className={`btn ${isSelected ? "btn-secondary" : "bg-white"}`}
    >
      {text}
    </button>
  );
};

const ChoiceQuestion: React.FC<QuestionProps> = ({
  index,
  totalQuestion,
  question,
  answer,
  explanation,
  choices,
  handleNext,
  handleComplete,
}) => {
  // State to track the index of the selected button
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [hasSubmit, setHasSubmit] = useState(false);
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>("");

  const handleNextQuestion = () => {
    setHasSubmit(false);
    setResult("");
    setSelectedIndex(null);
    setError("");
    handleNext();
  };

  const handleButtonClick = (index: number) => {
    if (!hasSubmit) {
      setSelectedIndex(index);
      setError("");
    }
  };

  const handleSubmit = async (e: MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setIsLoading(true);

    if (selectedIndex === null) {
      setError("Please select an option before submitting.");
      setIsLoading(false);
      return;
    }

    const data = {
      question_and_answer: {
        answer: answer,
        question: question,
        choices: choices,
      },
      student_answer:
        typeof answer === "number"
          ? selectedIndex
          : choices && selectedIndex !== null
          ? choices[selectedIndex]
          : null,
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
                    "An unexpected error occurred. Please try again later."
                  );
                  break;
              }
            } else {
              setError("An error occurred while processing your request.");
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
      <div className="flex flex-col">
        {choices &&
          choices.map((choice, idx) => (
            <ColorChangingButton
              key={idx}
              text={choice}
              isSelected={selectedIndex === idx}
              onClick={() => handleButtonClick(idx)}
            />
          ))}
      </div>
      <div className="flex items-center justify-center">
        {error && <p className="text-red-500">{error}</p>}
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
              <p className="text-green-400 my-1">Correct! </p>
            ) : (
              <p className="text-red-400 my-1">Wrong!</p>
            )}
            {choices && typeof answer === "number" && (
              <div>Answer: {choices[answer as number]} </div>
            )}
            {choices && typeof answer === "string" && (
              <div>Answer: {answer} </div>
            )}
            {explanation && <div>Explanation: {explanation}</div>}
            {index !== totalQuestion ? (
              <button
                className="btn btn-active btn-secondary mt-2"
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
          <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 overflow-auto">
            <OwlLoader text="Simplifying the chaos..." />
          </div>
        )}
      </div>
    </div>
  );
};

export default ChoiceQuestion;
