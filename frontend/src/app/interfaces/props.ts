import { NotesRequest } from "./interface";
import { QuestionType, LanguageType } from "./type";

export interface GeneratedTextProps {
  markdown?: string;
}

export interface QuestionTypeSelectorProps {
  questionTypes: QuestionType[];
  setQuestionTypes: (val: QuestionType[]) => void;
}

export interface LanguageSelectProps {
  language?: LanguageType;
  handleChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
}

export interface QuestionProps {
  index: number;
  totalQuestion: number;
  question: string;
  answer: string | number | Array<number>;
  explanation: string;
  choices?: Array<string>;
  handleNext: () => void;
  handleComplete: () => void;
}

export interface NoteFormProps {
  notesData: NotesRequest;
  handleChange: (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
}
