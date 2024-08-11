"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { auth } from "../firebase";
import { NotesRequest } from "@/app/interfaces/interface";
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
    if (file) {
      setFile(file);
    } else {
      setFile("");
    }
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
    setIsLoading(true);
    e.preventDefault();

    const formData = new FormData();
    formData.append("notes_customisation", JSON.stringify(notesData));
    formData.append("file", file);

    if (!file) {
      setError("Make sure you choose your file");
      setIsLoading(false);
    } else {
      try {
        auth.onAuthStateChanged(async (user) => {
          if (user) {
            const token = await user.getIdToken();
            const response = await fetch(
              "http://0.0.0.0:8000/v1/api/get-notes-from-uploaded-file",
              {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${token}`,
                },
                body: formData,
              }
            );
            setIsLoading(false);
            if (response.ok) {
              const result = await response.json();
              console.log("Generation successful", result);
              localStorage.setItem("summary", JSON.stringify(result));
              handleNavigateGenerate();
            } else {
              console.error("", response.statusText);
              setError("Generation failed. Please check your file.");
            }
          }
        });
      } catch (error) {
        console.error("Error:", error);
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="flex flex-col bg-primary w-full min-h-screen">
      <Layout />
      {error && <ErrorModal errorMessage={error} />}
      <div className="card bg-base-100 p-5 mx-5 mt-5 border-black border-2">
        <div className="card-body">
          <h2 className="card-title">Drag and drop files here</h2>
          <p>File type accepted: .mov, .mp4, .pdf, .pptx</p>
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
          <OwlLoader />
        </div>
      )}
    </div>
  );
}
