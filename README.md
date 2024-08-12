# Whoots: Your Ultimate Study Companion

Whoots is a revolutionary app designed to transform the way students learn. By _simplifying_ complex study materials and _tailoring_ them to individual needs, Whoots aims to reduce stress and maximize understanding. Whether it's summarizing notes, generating quizzes, or providing targeted feedback, Whoots is here to make learning more efficient and enjoyable.

## Login
<img width="1440" alt="login_page" src="https://github.com/user-attachments/assets/58910ce0-2e17-4137-8a37-ccee80c07d66">

## Generate Notes
<img width="1440" alt="notes_mp4_page" src="https://github.com/user-attachments/assets/c9ae467c-5300-482d-ae7a-98f84aea7382">

## Preview & Download Notes
<img width="1440" alt="notes_download_page" src="https://github.com/user-attachments/assets/843018e6-a6f5-4742-966e-c2e0748aa1c6">

## Download Notes as Markdown
<img width="1440" alt="notes_md" src="https://github.com/user-attachments/assets/5ab913a8-56e5-4e73-8bb0-3eae83f7c261">

## Generate Quiz
<img width="1440" alt="generate_quiz_page" src="https://github.com/user-attachments/assets/b564ff1f-d5e8-47ed-9f00-3f244c6cb1a6">

## Quiz MCQ
<img width="1440" alt="quiz_mcq_page" src="https://github.com/user-attachments/assets/4a3e3ba9-7e35-4dc7-b1f3-ce2e0711702a">

## Quiz Long Answer
<img width="1440" alt="quiz_long_answer_page" src="https://github.com/user-attachments/assets/f9e42cf1-a117-4147-ad3e-201cd45303e2">

## Score, Strength & Weakness
<img width="1440" alt="strength_and_weakness_page" src="https://github.com/user-attachments/assets/9cbac7cc-3fdc-4047-b3cd-848667823e0d">

## Query Bot
<img width="1440" alt="query_bot_popup" src="https://github.com/user-attachments/assets/3be7d038-7daf-4b6f-a77c-9ac42acee003">

## Loading...
<img width="1440" alt="loading_page" src="https://github.com/user-attachments/assets/db645ff4-c2ca-479b-a985-1d208656a074">

## 🔑 Setting Up Secrets

1. Fill up the .env file in the root directory:

- Types of credentials to include:
  - `Firebase SDK`
  - `Firebase Service Account Key`
  - `Google API Key`

2. Obtain Keys:

- **Firebase SDK**:
  - Follow [this guide](https://firebase.google.com/docs/web/setup) to get the `Firebase SDK` credentials.
- **Firebase Service Account Key**:
  - Follow [the guide](https://firebase.google.com/docs/admin/setup) here to get the `Firebase Service Account Key`.
- **Google Gemini API Key**:
  - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey) for `Google API Key`.

## 🖥️ Run Frontend

Install and run the development server:

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the frontend.

## 🔧 Run Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
brew install ffmpeg
```
Run the VSCode Python Debugger and open [http://localhost:8000](http://localhost:8000) with your browser to see the Swagger UI.


## 🚀 Features

**Summarized Notes**

- Upload & Summarize: Easily upload your study materials (PDFs, Word documents, PowerPoint slides, images, or videos) and get them instantly transformed into concise, customizable summaries.
- Customizable Summaries: Adjust focus, tone, emphasis, length, and language to fit your specific needs.

**Quiz Generation**

- Custom Quizzes: Generate quizzes based on your uploaded study materials, tailored to your individual learning style.
- Quiz Customization: Control the number of questions, types, difficulty levels, inclusion of explanations, and more.
- Personalized Learning: Quizzes are contextually accurate and adapted to your learning progress.

**Strengths and Weaknesses Evaluation**

- Performance Feedback: Evaluate your quiz performance with insights into your strengths and areas for improvement.
- LLM-Assisted Evaluation: Compare your free responses against ideal answers for a deeper understanding.
- Regenerate Quizzes: Create new quizzes based on your performance to target areas needing improvement.

**Query Bot**

- Get Help Instantly: Use our built-in query bot to ask specific questions and receive context-aware responses.

View our Figma mockup [here](https://www.figma.com/design/LpRss6wc9xIStvZCaUTMOn/Google-Hackathon-Mockup?node-id=0-1&t=UPdGNsf8OHFh6hqQ-1).

## 🛠️ Tech Stack

**Frontend:**

- Next.js
- Daisy UI
- Tailwind CSS
- React with TypeScript

**Backend:**

- FastAPI
- Firestore Database
- Firestore Vector Search
- Firebase Authentication

**AI/ML Models:**

- Gemini Generative Model
- Embedding Model

### 🎉 Whoots Whoots Whooray for Learning!
