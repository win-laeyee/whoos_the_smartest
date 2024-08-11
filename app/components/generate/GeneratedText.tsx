import React from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { GeneratedTextProps } from "../../interfaces/props";

const GeneratedText: React.FC<GeneratedTextProps> = ({ markdown }) => {
  return (
    <div className="w-full prose">
      <Markdown
        className="w-screen-minus-10 ml-5 h-96 bg-base-100 overflow-y-auto p-5 border-black border-2"
        remarkPlugins={[remarkGfm]}
      >
        {markdown}
      </Markdown>
    </div>
  );
};

export default GeneratedText;
