"use client";
import { MouseEvent, useState } from "react";
import { auth } from "../../firebase";
import { QuestionProps } from "../../interfaces/props";
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

  const handleNextQuestion = () => {
    setHasSubmit(false);
    setResult("");
    setSelectedIndex(null);
    handleNext();
  };

  // Handle button click to set selected index
  const handleButtonClick = (index: number) => {
    setSelectedIndex(index);
  };

  const handleSubmit = (e: MouseEvent<HTMLButtonElement>) => {
    setIsLoading(true);
    e.preventDefault();

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
          const token = await user.getIdToken();

          const response = await fetch(
            "http://0.0.0.0:8000/v1/api/evaluate-student-answer",
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
            console.error("", response.statusText);
          }
        }
      });
    } catch (error) {
      console.error("Error:", error);
      setIsLoading(false);
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
