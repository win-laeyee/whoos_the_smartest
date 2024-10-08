"use client";
import { useRef, useState, useEffect, MouseEvent } from "react";
import { auth } from "../../firebase";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import OwlLoader from "../ui/OwlLoader";
import Image from "next/image";

const QueryBot: React.FC = () => {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const modalRef = useRef<HTMLDialogElement>(null);

  const [error, setError] = useState<string>("");

  const handleQuestion = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(e.target.value);
  };

  const openModal = () => {
    if (modalRef.current) {
      modalRef.current.showModal();
    }
  };

  const handleQueryBot = (e: MouseEvent<HTMLButtonElement>) => {
    setIsLoading(true);
    e.preventDefault();

    const data = {
      query: question,
    };

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          const token = await user.getIdToken();

          const response = await fetch("http://0.0.0.0:8000/v1/api/query-bot", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(data),
          });

          setIsLoading(false);

          if (response.ok) {
            const result = await response.json();
            console.log("Query successful", result);
            setAnswer(result.answer);
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
    const handleClose = () => {
      setQuestion("");
      setAnswer("");
    };

    const modal = modalRef.current;
    if (modal) {
      modal.addEventListener("close", handleClose);
    }

    return () => {
      if (modal) {
        modal.removeEventListener("close", handleClose);
      }
    };
  }, []);

  return (
    <div>
      <div className="relative group inline-block">
        <button
          className="btn btn-neutral rounded-full p-2 w-16 h-16 flex items-center justify-center transition-transform transform group-hover:scale-110 ml-5"
          type="button"
          onClick={openModal}
        >
          <Image
            src="/whoo_static.png"
            alt="whoots"
            width={40}
            height={40}
            className="rounded-full"
            priority
          />
        </button>
        <div className="absolute left-1/2 bottom-0 transform -translate-x-1/2 translate-y-2 bg-black text-white text-xs rounded py-1 px-2 opacity-0 hover:opacity-100 transition-opacity duration-300">
          Ask me anything
        </div>
      </div>

      <dialog id="query_modal" className="modal" ref={modalRef}>
        <div className="modal-box min-h-64">
          <button
            className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
            onClick={() => {
              if (modalRef.current) {
                modalRef.current.close();
              }
            }}
          >
            ✕
          </button>
          <h3 className="font-bold text-lg">
            Hello! Feel free to ask any queries you have about your notes!
          </h3>
          <div className="flex items-center gap-2 mt-4">
            <input
              type="text"
              className="input input-bordered flex-grow"
              placeholder="Enter your query here"
              value={question}
              onChange={handleQuestion}
            />
            <button className="btn btn-secondary" onClick={handleQueryBot}>
              Submit
            </button>
          </div>
          {isLoading && (
            <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
              <OwlLoader text="Turning hoots into insights..." />
            </div>
          )}
          {answer && (
            <Markdown
              className="bg-base-100 overflow-y-auto mt-2 flex-grow"
              remarkPlugins={[remarkGfm]}
            >
              {answer}
            </Markdown>
          )}
        </div>
      </dialog>
    </div>
  );
};

export default QueryBot;
