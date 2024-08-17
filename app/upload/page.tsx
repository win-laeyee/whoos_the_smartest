"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "../firebase";
import { NotesRequest } from "@/app/interfaces/interface";
import { HttpError } from "../utils/errors";
import Layout from "../components/ui/layout";
import ErrorModal from "../components/ui/ErrorModal";
import NoteForm from "../components/upload/NoteForm";
import OwlLoader from "../components/ui/OwlLoader";

export default function Page() {
  const router = useRouter();
  const [file, setFile] = useState<string | Blob>("");
  const [notesData, setNotesData] = useState<NotesRequest>({
    focus: undefined,
    focus_custom: "",
    tone: undefined,
    tone_custom: "",
    emphasis: undefined,
    emphasis_custom: "",
    length: undefined,
    length_custom: "",
    language: "English",
  });
  const [error, setError] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleNavigateGenerate = () => {
    router.push("/generate");
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setFile(file || "");
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setNotesData({
      ...notesData,
      [name]: value,
    });
  };

  const handleGenerate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    const formData = new FormData();
    formData.append("notes_customisation", JSON.stringify(notesData));
    formData.append("file", file);

    if (!file) {
      setError("Make sure you choose your file");
      setIsLoading(false);
      return;
    }

    try {
      auth.onAuthStateChanged(async (user) => {
        if (user) {
          try {
            const token = await user.getIdToken();
            const response = await fetch(
              `${process.env.NEXT_PUBLIC_API_URL}/v1/api/get-notes-from-uploaded-file`,
              {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
                body: formData,
              }
            );
            setIsLoading(false);

            if (!response.ok) {
              console.error("Error:", response.statusText, response.status);
              throw new HttpError(response.statusText, response.status);
            }

            const result = await response.json();
            console.log("Generation successful", result);
            localStorage.setItem("summary", JSON.stringify(result));
            handleNavigateGenerate();
          } catch (fetchError) {
            setIsLoading(false);
            console.error("Fetch error:", fetchError);

            if (fetchError instanceof HttpError) {
              switch (fetchError.status) {
                case 400:
                  setError("Bad request. Please check your input.");
                  break;
                case 401:
                  setError("Unauthorized. Please log in.");
                  break;
                case 403:
                  setError("Forbidden. You do not have access.");
                  break;
                case 404:
                  setError(
                    "Not found. The requested resource could not be found."
                  );
                  break;
                case 413:
                  setError("Request entity too large.");
                  break;
                case 422:
                  setError(
                    "Unprocessable entity. The request was well-formed but unable to be followed due to semantic errors."
                  );
                  break;
                case 500:
                  setError(
                    "Internal server error. Please try again later. Gemini API resource limit may have been reached."
                  );
                  break;
                case 504:
                  setError(
                    "Gateway timeout. The server took too long to respond."
                  );
                  break;
                default:
                  setError(
                    "Generation failed. The request took too long to process. Please try again later. Note: The maximum duration allowed is 60 seconds."
                  );
                  break;
              }
            } else {
              setError(
                "An unexpected error occurred. The request took too long to process. Please try again later. Note: The maximum duration allowed is 60 seconds."
              );
            }
          }
        } else {
          setError("User is not authenticated.");
        }
        setIsLoading(false);
      });
    } catch (authError) {
      setIsLoading(false);
      console.error("Authentication error:", authError);
      setError("Authentication failed.");
    }
  };

  return (
    <div className="flex flex-col bg-primary w-full min-h-screen">
      <Layout />
      {error && <ErrorModal errorMessage={error} />}
      <div className="card bg-base-100 p-5 mx-5 mt-5 border-black border-2">
        <div className="card-body">
          <h2 className="card-title">Drag and drop files here</h2>
          <p>
            File type accepted (MAX SIZE: 4.5 MB): .docx, .jpg, .jpeg, .png,
            .mov, .mp4, .pdf
          </p>
          <input
            type="file"
            className="file-input border-black flex-grow file-input-secondary"
            onChange={handleFileChange}
          />
        </div>
      </div>
      <NoteForm
        handleChange={handleChange}
        handleSubmit={handleGenerate}
        notesData={notesData}
      />
      {isLoading && (
        <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
          <OwlLoader text="Turning hoots into insights..." />
        </div>
      )}
    </div>
  );
}
