"use client";
import { auth } from "@/app/firebase";
import { signOut } from "firebase/auth";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Layout({ children }: { children?: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [currentPath, setCurrentPath] = useState(pathname);

  useEffect(() => {
    setCurrentPath(pathname);
  }, [pathname]);

  const navigateTo = (path: string) => {
    if (path !== currentPath) {
      router.push(path);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      // Redirect the user to the login page or show a success message
      router.push("/");
      console.log("Successfully logged out");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="flex flex-row items-center">
      <Image
        src="/whoo_static.png"
        alt="whoo"
        width={50}
        height={50}
        className="ml-5"
      />
      <ul className="timeline flex  w-full">
        <li className="flex-auto">
          <div
            className="timeline-end cursor-pointer"
            onClick={() => navigateTo("/upload")}
          >
            Upload
          </div>

          <div className="timeline-middle">
            <svg
              width="30"
              height="30"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="bg-accent"
              className="text-secondary cursor-pointer"
              onClick={() => navigateTo("/upload")}
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <hr
            className={currentPath == "/upload" ? "bg-secondary" : "bg-accent"}
          />
        </li>
        <li className="flex-auto">
          <hr
            className={currentPath == "/upload" ? "bg-secondary" : "bg-accent"}
          />
          <div className="timeline-middle">
            <svg
              width="30"
              height="30"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill={currentPath == "/upload" ? "currentColor" : "bg-accent"}
              className="text-secondary cursor-pointer"
              onClick={() =>
                currentPath === "/quiz" ? navigateTo("/generate") : undefined
              }
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                clipRule="evenodd"
              />
            </svg>
          </div>
          <div
            className="timeline-end cursor-pointer"
            onClick={() =>
              currentPath === "/quiz" ? navigateTo("/generate") : undefined
            }
          >
            Generate
          </div>
          <hr
            className={currentPath != "/quiz" ? "bg-secondary" : "bg-accent"}
          />
        </li>
        <li className="flex-auto">
          <hr
            className={currentPath != "/quiz" ? "bg-secondary" : "bg-accent"}
          />
          <div className="timeline-end ">Quiz</div>
          <div className="timeline-middle">
            <svg
              width="30"
              height="30"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill={currentPath == "/quiz" ? "bg-accent" : "currentColor"}
              className="text-secondary"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
                clipRule="evenodd"
              />
            </svg>
          </div>
        </li>
      </ul>
      <button className="btn btn-secondary mr-5" onClick={handleLogout}>
        Logout
      </button>
    </div>
  );
}
