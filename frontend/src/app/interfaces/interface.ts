import { LanguageType, QuestionType } from "./type";

export interface QuizGenerationOptions {
  number_of_questions: number; // Optional, defaults to 10
  question_types: QuestionType[];
  difficulty_level: "" | "easy" | "medium" | "hard" | "mix";
  include_explanations: boolean; // Optional, defaults to false
  emphasis: "" | "key_points" | "details" | "definitions" | "other";
  emphasis_custom?: string;
  language: LanguageType;
}

export interface NotesRequest {
  focus?:
    | ""
    | "general"
    | "specific_concepts"
    | "examples"
    | "summary"
    | "other";
  focus_custom?: string;
  tone?: "" | "formal" | "informal" | "conversational" | "other";
  tone_custom?: string;
  emphasis?: "" | "key_points" | "details" | "definitions" | "other";
  emphasis_custom?: string;
  length?: "" | "concise" | "moderate" | "detailed" | "other";
  length_custom?: string;
  language?: LanguageType;
}

export interface Evaluation {
  score: number;
  strength: string;
  weakness: string;
}
