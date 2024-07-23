"use client";

import Layout from "../ui/layout";
import { useRouter } from "next/navigation";

export default function Page() {
  const router = useRouter();

  const handleNavigate = () => {
    router.push("/generate");
  };

  return (
    <div className="flex h-full flex-col items-center bg-primary min-h-screen">
      <Layout />
      <div className="flex flex-row p-5 w-full">
        <div className="card bg-base-100 shadow-xl p-5 mx-5 w-1/2">
          <div className="card-body">
            <h2 className="card-title">Drag and drop files here</h2>
            <p>File type accepted: .mov, .mp4, .pdf, .pptx</p>

            <input
              type="file"
              className="file-input border-black flex-grow file-input-secondary"
            />
          </div>
        </div>
        <div className="flex flex-col w-1/2 justify-center">
          <input
            type="text"
            placeholder="Enter page numbers e.g. 2-5"
            className="input input-bordered rounded-full border-black border-2 w-full my-2"
          />
          <select className="select select-bordered rounded-full border-black border-2 w-full my-2">
            <option disabled selected>
              Note type
            </option>
            <option>Detailed</option>
            <option>Overview</option>
          </select>
          <select className="select select-bordered rounded-full border-black border-2 w-full my-2">
            <option disabled selected>
              Learning style
            </option>
            <option>Visual</option>
            <option>Auditory</option>
            <option>Reading/writing</option>
          </select>
        </div>
      </div>
      <button className="btn btn-secondary rounded-md" onClick={handleNavigate}>
        Generate
      </button>
    </div>
  );
}
