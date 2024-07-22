import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface GeneratedTextProps {
  markdown?: string;
}

const GeneratedText: React.FC<GeneratedTextProps> = ({ markdown: string }) => {
  const exampleMarkdown = `A paragraph with *emphasis* and **strong importance**.

  > A block quote with ~strikethrough~ and a URL: https://reactjs.org.

* Lists
* [ ] todo
* [x] done

A table:

| a | b |
| - | - |`;
  return (
    <div className="flex flex-row justify-start items-start mx-5 w-screen h-screen prose">
      <Markdown
        className="bg-base-100 h-4/5 w-1/2 overflow-y-auto p-5 mr-5 flex-grow"
        remarkPlugins={[remarkGfm]}
      >
        {exampleMarkdown}
      </Markdown>
    </div>
  );
};

export default GeneratedText;
