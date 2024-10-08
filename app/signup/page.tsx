"use client";
import "firebaseui/dist/firebaseui.css";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { useState } from "react";
import ErrorModal from "../components/ui/ErrorModal";
import OwlLoader from "../components/ui/OwlLoader";

const Page: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showPopup, setShowPopup] = useState(false);

  const router = useRouter();
  const handleNavigateLogin = () => {
    router.push("/");
  };

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    setIsLoading(true);
    e.preventDefault();

    const data = { email, password };

    try {
      const response = await fetch("http://0.0.0.0:8000/v1/api/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      setIsLoading(false);
      if (response.ok) {
        const result = await response.json();
        console.log("Login successful", result);
        setShowPopup(true);
      } else {
        console.error("Login failed", response.statusText);
        setError("Sign up failed. Please check your email and password.");
      }
    } catch (error) {
      console.error("Error:", error);
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col min-h-screen min-w-screen bg-primary justify-center items-center">
      {error && <ErrorModal errorMessage={error} />}
      {showPopup && (
        <div className="fixed inset-0 bg-opacity-60 bg-gray-800 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-xl text-center max-w-sm w-full">
            <p className="text-lg font-semibold text-gray-800 mb-4">
              Your account has been created successfully!
            </p>
            <p className="text-md text-gray-600">
              You can now log in with your email.
            </p>
            <button
              onClick={() => {
                setShowPopup(false);
                handleNavigateLogin();
              }}
              className="mt-4 px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              OK
            </button>
          </div>
        </div>
      )}
      <div className="prose flex flex-col items-center text-center">
        <h1>Welcome to whoots</h1>

        <Image
          src="/whoo_static.png"
          alt="whoots"
          width={150}
          height={150}
          priority
        />
        <form className="space-y-4" onSubmit={handleLogin}>
          <label className="input input-bordered flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70"
            >
              <path d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
              <path d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
            </svg>
            <input
              type="text"
              className="grow"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <label className="input input-bordered flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70"
            >
              <path
                fillRule="evenodd"
                d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
                clipRule="evenodd"
              />
            </svg>
            <input
              type="password"
              className="grow"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="submit" className="btn btn-secondary">
            Sign up
          </button>
        </form>
      </div>

      <a className="link link-neutral mt-2" onClick={handleNavigateLogin}>
        Click here to log in
      </a>
      {isLoading && (
        <div className="fixed inset-0 bg-opacity-50 bg-black flex items-center justify-center z-50 w-full h-full top-0 left-0">
          <OwlLoader text="Signing you up..." />
        </div>
      )}
    </div>
  );
};

export default Page;
