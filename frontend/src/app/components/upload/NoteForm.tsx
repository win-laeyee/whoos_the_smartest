"use client";
import { useState } from "react";
import LanguageSelect from "../ui/LanguageSelect";
import { NoteFormProps } from "@/app/interfaces/props";

const NoteForm: React.FC<NoteFormProps> = ({
  notesData,
  handleChange,
  handleSubmit,
}) => {
  const [showFocusOther, setShowFocusOther] = useState(false);
  const [showToneOther, setShowToneOther] = useState(false);
  const [showEmphasisOther, setShowEmphasisOther] = useState(false);
  const [showLengthOther, setShowLengthOther] = useState(false);

  // Function to handle changes in the select inputs
  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;

    if (name === "focus") {
      setShowFocusOther(value === "other");
    } else if (name === "tone") {
      setShowToneOther(value === "other");
    } else if (name === "emphasis") {
      setShowEmphasisOther(value === "other");
    } else if (name === "length") {
      setShowLengthOther(value === "other");
    }

    handleChange(e);
  };

  return (
    <form
      className="flex max-w-full h-full flex-col bg-primary mx-5 my-2"
      onSubmit={handleSubmit}
    >
      <div className="flex flex-col justify-center">
        <label className="form-control w-full ">
          <div className="label">
            <span className="label-text font-semibold">
              Select focus area for the notes
            </span>
          </div>
          <select
            name="focus"
            value={notesData.focus}
            onChange={handleSelectChange}
            className="select select-bordered rounded-full border-black border-2 w-full"
          >
            <option value="general">General</option>
            <option value="specific_concepts">Specific concepts</option>
            <option value="examples">Examples</option>
            <option value="summary">Summary</option>
            <option value="other">Other</option>
          </select>
          {showFocusOther && (
            <input
              name="focus_custom"
              type="text"
              placeholder="Please specify"
              className="input input-bordered rounded-full border-black border-2 w-full mt-2"
              onChange={handleChange}
            />
          )}
        </label>

        <label className="form-control w-full ">
          <div className="label">
            <span className="label-text font-semibold">
              Select preferred tone for the notes
            </span>
          </div>
          <select
            name="tone"
            value={notesData.tone}
            onChange={handleSelectChange}
            className="select select-bordered rounded-full border-black border-2 w-full"
          >
            <option value="formal">Formal</option>
            <option value="informal">Informal</option>
            <option value="conversational">Conversational</option>
            <option value="other">Other</option>
          </select>
          {showToneOther && (
            <input
              name="tone_custom"
              type="text"
              placeholder="Please specify"
              className="input input-bordered rounded-full border-black border-2 w-full mt-2"
              onChange={handleChange}
            />
          )}
        </label>

        <label className="form-control w-full ">
          <div className="label">
            <span className="label-text font-semibold">
              Select what to emphasize in the notes
            </span>
          </div>
          <select
            name="emphasis"
            value={notesData.emphasis}
            onChange={handleSelectChange}
            className="select select-bordered rounded-full border-black border-2 w-full "
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

        <label className="form-control w-full ">
          <div className="label">
            <span className="label-text font-semibold">
              Select desired length of the notes
            </span>
          </div>
          <select
            name="length"
            value={notesData.length}
            onChange={handleSelectChange}
            className="select select-bordered rounded-full border-black border-2 w-full "
          >
            <option value="concise">Concise</option>
            <option value="moderate">Moderate</option>
            <option value="detailed">Detailed</option>
            <option value="other">Other</option>
          </select>
          {showLengthOther && (
            <input
              name="length_custom"
              type="text"
              placeholder="Please specify"
              className="input input-bordered rounded-full border-black border-2 w-full mt-2"
              onChange={handleChange}
            />
          )}
        </label>

        <LanguageSelect
          language={notesData.language}
          handleChange={handleChange}
        />
      </div>
      <button
        type="submit"
        className="btn btn-secondary rounded-md self-center"
      >
        Generate
      </button>
    </form>
  );
};

export default NoteForm;
