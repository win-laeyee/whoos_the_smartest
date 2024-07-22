import Image from "next/image";
import Page from "./upload/page";
import Layout from "./ui/layout";

export default function Home() {
  return (
    <main className="flex flex-col min-h-screen min-w-screen bg-primary">
      <Layout />
      <Page />
    </main>
  );
}
