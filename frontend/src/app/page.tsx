"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const handleNavigate = () => {
    router.push("/upload");
  };

  return (
    <main className="flex flex-col min-h-screen min-w-screen bg-primary justify-center items-center">
      <div className="prose flex flex-col items-center text-center">
        <h1>Welcome to whoo</h1>
        <p className="mb-5">
          Upload your document and whoo will help you generate notes and take
          care of the rest!
        </p>
      </div>
      <button className="btn btn-secondary" onClick={handleNavigate}>
        Click here to get started
      </button>
    </main>
  );
}
