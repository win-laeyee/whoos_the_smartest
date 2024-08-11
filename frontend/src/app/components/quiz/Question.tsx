import { QuestionProps } from "../../interfaces/props";
import ChoiceQuestion from "./ChoiceQuestion";
import MultiSelectQuestion from "./MultiSelectQuestion";
import TextQuestion from "./TextQuestion";

const Question: React.FC<QuestionProps> = ({
  index,
  totalQuestion,
  question,
  answer,
  explanation,
  choices,
  handleNext,
  handleComplete,
}) => {
  const getQuestionType = () => {
    if (answer === "True" || answer === "False") {
      return "choices";
    } else if (typeof answer === "string") {
      return "text";
    } else if (typeof answer === "number") {
      return "choices";
    } else if (Array.isArray(answer) && answer.every(Number.isInteger)) {
      return "multi-select";
    } else {
      return "unknown";
    }
  };

  const questionType = getQuestionType();

  return (
    <div className="m-5 prose">
      {questionType === "text" && (
        <TextQuestion
          index={index}
          totalQuestion={totalQuestion}
          question={question}
          answer={answer}
          explanation={explanation}
          handleNext={handleNext}
          handleComplete={handleComplete}
        />
      )}
      {questionType === "choices" && (
        <ChoiceQuestion
          index={index}
          totalQuestion={totalQuestion}
          question={question}
          answer={answer}
          explanation={explanation}
          choices={choices}
          handleNext={handleNext}
          handleComplete={handleComplete}
        />
      )}
      {questionType === "multi-select" && (
        <MultiSelectQuestion
          index={index}
          totalQuestion={totalQuestion}
          question={question}
          answer={answer}
          explanation={explanation}
          choices={choices}
          handleNext={handleNext}
          handleComplete={handleComplete}
        />
      )}
    </div>
  );
};

export default Question;
