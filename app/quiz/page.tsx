"use client";
import { useEffect, useState } from "react";

import Layout from "../components/ui/layout";
import { auth } from "../firebase";
import { Evaluation, QuizGenerationOptions } from "../interfaces/interface";
import { QuestionType } from "../interfaces/type";
import QuizForm from "../components/quiz/QuizForm";
import Question from "../components/quiz/Question";
import OwlLoader from "../components/ui/OwlLoader";

const Page: React.FC = () => {
  const [quiz, setQuiz] = useState<Array<any> | null>(null);
  const [numQuestions, setNumQuestion] = useState(0);
  const [totalQuestion, setTotalQuestion] = useState(10);
  const [complete, setComplete] = useState(false);
  const [evaluation, setEvaluation] = useState<Evaluation>({
    score: 0,
    strength: "",
    weakness: "",
  });
  const [formData, setFormData] = useState<QuizGenerationOptions>({
    number_of_questions: 10,
    question_types: ["multiple_choice"],
    difficulty_level: "mix",
    include_explanations: false,
    emphasis: "key_points",
    language: "English",
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    getQuiz();
  }, []);

  const getQuiz = () => {
    const quizString = localStorage.getItem("quiz");
    if (quizString) {
      try {
        const quiz = JSON.parse(quizString);

        // Check if questions_and_answers exists and is an array
        if (
          quiz.questions_and_answers &&
          Array.isArray(quiz.questions_and_answers)
        ) {
          setQuiz(quiz.questions_and_answers);
          setTotalQuestion(quiz.questions_and_answers.length);
        } else {
          console.error(
            'Property "questions_and_answers" is missing or not an array.'
          );
        }
      } catch (e) {
        console.error("Error parsing JSON:", e);
      }
    } else {
      console.error("No quiz found in localStorage.");
    }
  };

  const handleQuestionType = (val: QuestionType[]) => {
    setFormData({
      ...formData,
      question_types: val,
    });
  };

  const [error, setError] = useState<string>("");

  const handleNext = () => {
    if (quiz && numQuestions < quiz.length - 1) {
      setNumQuestion(numQuestions + 1);
    }
  };

  const handleComplete = () => {
    setComplete(true);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleRegenerateQuiz = (e: React.FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    e.preventDefault();

    const data = {
      quiz_customisation: formData,
      strength_and_weakness: evaluation,
    };

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          const token = await user.getIdToken();

          const response = await fetch(
            "http://0.0.0.0:8000/v1/api/regenerate-quiz",
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
            console.log("Regeneration of quiz successful", result);
            localStorage.setItem("quiz", JSON.stringify(result));
            getQuiz();
            setComplete(false);
          } else {
            console.error("Error:", response.statusText);
          }
        }
      });
    } catch (error) {
      console.error("Error:", error);
      setIsLoading(false);
      setError("Request failed.");
    }
  };

  useEffect(() => {
    if (complete) {
      setIsLoading(true);
      const fetchEvaluation = async () => {
        const data = { num_of_qns: totalQuestion };
        try {
          auth.onAuthStateChanged(async (user) => {
            if (user) {
              const token = await user.getIdToken();

              const response = await fetch(
                "http://0.0.0.0:8000/v1/api/get-student-strength-weakness",
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
              setNumQuestion(0);
              if (response.ok) {
                const result = await response.json();
                setEvaluation(result);
              } else {
                console.error("Error:", response.statusText);
              }
            }
          });
        } catch (error) {
          console.error("Error:", error);
          setIsLoading(false);
          setError("Request failed.");
        }
      };

      fetchEvaluation();
    }
  }, [complete, totalQuestion]);

  const currentQuestion = quiz ? quiz[numQuestions] : "";

  return (
    <div className="bg-primary min-h-screen min-w-screen overflow-y-auto">
      <Layout></Layout>

      {complete ? (
        <div className="prose m-5 flex flex-col max-w-full items-center justify-center">
          <svg
            width="50"
            height="50"
            viewBox="0 0 38 31"
            fill="green"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path d="M30.9801 0.206238L27.7033 3.62557L14.5008 16.828L10.6541 13.1237L7.23477 9.70438L0.538574 16.4006L3.95791 19.8199L11.0815 26.9435L14.3584 30.3628L17.7777 26.9435L34.3995 10.3218L37.8188 6.90243L30.9801 0.206238Z" />
          </svg>
          <div>Score: {evaluation.score}%</div>

          <div className="p-5 bg-green-200 rounded-lg my-2 w-full">
            Strength: {evaluation.strength}
          </div>
          <div className="p-5 bg-red-200 rounded-lg my-2 w-full">
            Weakness: {evaluation.weakness}
          </div>
          <QuizForm
            text="Regenerate"
            formData={formData}
            handleChange={handleChange}
            handleQuestionType={handleQuestionType}
            handleSubmit={handleRegenerateQuiz}
          />
        </div>
      ) : (
        <div className="flex flex-col justify-center items-center mt-5">
          <Question
            index={numQuestions + 1}
            totalQuestion={totalQuestion}
            question={currentQuestion.question}
            answer={currentQuestion.answer}
            explanation={currentQuestion.explanation}
            choices={currentQuestion.choices}
            handleNext={handleNext}
            handleComplete={handleComplete}
          />

          <progress
            className="progress progress-success w-56 mt-10 mb-2"
            value={((numQuestions + 1) / totalQuestion) * 100}
            max="100"
          ></progress>
          <p>
            Question {numQuestions + 1} of {totalQuestion}
          </p>
        </div>
      )}
      {isLoading && (
        <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
          <OwlLoader text="Simplifying the chaos..." />
        </div>
      )}
    </div>
  );
};

export default Page;
