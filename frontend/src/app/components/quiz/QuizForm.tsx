import { useState } from "react";
import { QuizGenerationOptions } from "../../interfaces/interface";
import { QuestionType } from "../../interfaces/type";
import QueryBot from "./QueryBot";
import LanguageSelect from "../ui/LanguageSelect";
import QuestionTypeSelector from "./QuestionTypeSelector";

interface QuizFormProps {
  text: string;
  formData: QuizGenerationOptions;
  handleQuestionType: (val: QuestionType[]) => void;
  handleChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}

const QuizForm: React.FC<QuizFormProps> = ({
  text,
  formData,
  handleQuestionType,
  handleChange,
  handleSubmit,
}) => {
  const [showEmphasisOther, setShowEmphasisOther] = useState(false);

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;

    if (name === "emphasis") {
      setShowEmphasisOther(value === "other");
    }

    const newValue = name === "include_explanations" ? value === "true" : value;

    handleChange(e);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full h-full">
      <label className="form-control">
        <div className="label">
          <span className="label-text font-semibold ">
            Enter number of quiz questions to generate
          </span>
        </div>
        <input
          name="number_of_questions"
          type="number"
          placeholder="10"
          className="input input-bordered rounded-full border-black border-2 w-full mb-2"
          onChange={handleChange}
          value={formData.number_of_questions}
        />
      </label>

      <QuestionTypeSelector
        questionTypes={formData.question_types}
        setQuestionTypes={handleQuestionType}
      />

      <label className="form-control w-full ">
        <div className="label">
          <span className="label-text font-semibold">
            Select preferred difficulty level of the questions
          </span>
        </div>
        <select
          name="difficulty_level"
          value={formData.difficulty_level}
          onChange={handleChange}
          className="select select-bordered rounded-full border-black border-2 w-full"
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
          <option value="mix">Mix</option>
        </select>
      </label>
      <label className="form-control w-full ">
        <div className="label">
          <span className="label-text font-semibold">
            Select whether to include explanations for the answers
          </span>
        </div>
        <select
          name="include_explanations"
          value={formData.include_explanations.toString()}
          onChange={handleSelectChange}
          className="select select-bordered rounded-full border-black border-2 w-full"
        >
          <option value="false">No</option>
          <option value="true">Yes</option>
        </select>
      </label>
      <label className="form-control w-full ">
        <div className="label">
          <span className="label-text font-semibold">
            Select what to emphasize in the quiz questions
          </span>
        </div>
        <select
          name="emphasis"
          value={formData.emphasis}
          onChange={handleSelectChange}
          className="select select-bordered rounded-full border-black border-2 w-full"
        >
          <option value="key_points">Key Points</option>
          <option value="details">Details</option>
          <option value="definitions">Definitions</option>
          <option value="other">Other</option>
        </select>
        {showEmphasisOther && (
          <input
            name="emphasis_custom"
            type="text"
            placeholder="Please specify"
            className="input input-bordered rounded-full border-black border-2 w-full mt-2"
            onChange={handleChange}
          />
        )}
      </label>

      <LanguageSelect
        language={formData.language}
        handleChange={handleChange}
      />
      <div className="flex flex-row justify-center items-center gap-2">
        <button className="btn btn-secondary" type="submit">
          {text}
        </button>
        <QueryBot />
      </div>
    </form>
  );
};

export default QuizForm;
