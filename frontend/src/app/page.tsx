"use client";

import Image from "next/image";
import FirebaseAuthUI from "./firebase";
import { useRouter } from "next/navigation";
import dynamic from "next/dynamic";

const FirebaseAuthUISSR = dynamic(() => import("./firebase"), {
  ssr: false,
});

const Home = () => {
  const router = useRouter();

  const handleSignUp = () => {
    router.push("/signup");
  };
  return (
    <main className="flex flex-col min-h-screen min-w-screen bg-primary justify-center items-center">
      <div className="prose flex flex-col items-center text-center mb-5">
        <h1>Welcome to whoo</h1>
        <Image
          src="/whoo_static.png"
          alt="whoo"
          width={150}
          height={150}
          priority
        />
      </div>
      <FirebaseAuthUISSR />
      <a className="link link-neutral mt-2" onClick={handleSignUp}>
        Click here to sign up
      </a>
    </main>
  );
};

export default Home;
