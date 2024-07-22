import Markdown from "react-markdown";

interface GeneratedTextProps {
  markdown?: string;
}

const GeneratedText: React.FC<GeneratedTextProps> = ({ markdown: string }) => {
  const exampleMarkdown = `A paragraph with *emphasis* and **strong importance**.`;
  return (
    <div className="flex flex-row justify-start items-start m-5 h-screen">
      <div className="card bg-base-100 h-4/5 basis-1/2 overflow-y-auto p-5">
        <Markdown>{exampleMarkdown}</Markdown>
      </div>
      <div className="flex flex-col justify-center items-center h-4/5">
        <h1>Notes has been generated...</h1>
      </div>
    </div>
  );
};

export default GeneratedText;
