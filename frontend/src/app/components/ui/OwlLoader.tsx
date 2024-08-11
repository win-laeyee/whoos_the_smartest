import Image from "next/image";
import owlImage1 from "../../../../public/whoo_walk_1.png";
import owlImage2 from "../../../../public/whoo_walk_2.png";

interface OwlLoaderProps {
  text?: string;
}

const OwlLoader: React.FC<OwlLoaderProps> = ({ text }) => {
  return (
    <div className="flex flex-col justify-center items-center prose">
      <div className="relative w-48 h-48">
        <Image
          src={owlImage1}
          alt="Owl 1"
          layout="fill"
          objectFit="contain"
          className="absolute inset-0 animate-walk1"
        />
        <Image
          src={owlImage2}
          alt="Owl 2"
          layout="fill"
          objectFit="contain"
          className="absolute inset-0 animate-walk2"
        />
      </div>
      <h3 className="text-white">{text}</h3>
    </div>
  );
};

export default OwlLoader;
