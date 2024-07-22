"use client";

import Layout from "../ui/layout";
import GeneratedText from "./GeneratedText";
import { useRouter } from "next/navigation";

const Page: React.FC = () => {
  const router = useRouter();

  const handleNavigate = () => {
    router.push("/quiz");
  };

  return (
    <div className="flex h-full flex-col justify-center items-center bg-primary w-screen min-h-screen">
      <Layout />
      <div className="flex w-full h-full">
        <GeneratedText />
        <div className="flex flex-col w-1/2 h-full prose mr-5 justify-center">
          <h1>Notes has been generated...</h1>
          <button className="btn btn-secondary mb-5">Download</button>
          <h1>Once you have reviewed, go ahead to quiz yourself!</h1>
          <button className="btn btn-secondary" onClick={handleNavigate}>
            Quiz
          </button>
        </div>
      </div>
    </div>
  );
};

export default Page;
