import Layout from "../ui/layout";
import GeneratedText from "./GeneratedText";

const Page: React.FC = () => {
  return (
    <div className="flex h-full flex-col items-center bg-primary min-h-screen">
      <Layout />
      <GeneratedText />
    </div>
  );
};

export default Page;
