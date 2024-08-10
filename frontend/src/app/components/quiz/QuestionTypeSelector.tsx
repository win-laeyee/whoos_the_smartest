import { QuestionTypeSelectorProps } from "@/app/interfaces/props";
import React from "react";
import { QuestionType } from "../../interfaces/type";

const QuestionTypeSelector: React.FC<QuestionTypeSelectorProps> = ({
  questionTypes,
  setQuestionTypes,
}) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const options = event.target.options;
    const selected: QuestionType[] = [...questionTypes];

    for (let i = 0; i < options.length; i++) {
      if (options[i].selected) {
        const value = options[i].value as QuestionType;
        const index = selected.indexOf(value);

        if (index > -1) {
          // If already selected, remove it (deselect)
          selected.splice(index, 1);
        } else {
          // Otherwise, add it (select)
          selected.push(value);
        }
      }
    }

    setQuestionTypes(selected);
  };

  return (
    <div className="w-full">
      <label className="block w-full label-text font-semibold">
        Select type(s) of questions to include in the quiz
      </label>
      <select
        multiple
        value={questionTypes}
        onChange={handleChange}
        className="select select-bordered rounded-lg border-black border-2 w-full mt-2 pt-2"
      >
        <option value="multiple_choice">Multiple Choice</option>
        <option value="multi_select">Multi-Select</option>
        <option value="true_false">True/False</option>
        <option value="fill_in_the_blank">Fill in the Blank</option>
        <option value="short_answer">Short Answer</option>
        <option value="long_answer">Long Answer</option>
      </select>
    </div>
  );
};

export default QuestionTypeSelector;
