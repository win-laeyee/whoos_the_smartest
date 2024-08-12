# Whoots: Your Ultimate Study Companion

Whoots is a revolutionary app designed to transform the way students learn. By _simplifying_ complex study materials and _tailoring_ them to individual needs, Whoots aims to reduce stress and maximize understanding. Whether it's summarizing notes, generating quizzes, or providing targeted feedback, Whoots is here to make learning more efficient and enjoyable.

[screenshots of app]
[change readme accordingly after deployment]

## 🖥️ Run Frontend

Install and run the development server:

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the frontend.

### 🔑 Setting Up Firebase

1. Replace the firebaseConfig in `firebase.tsx` with actual values after setting up your Firebase SDK.

- Refer to [🔑 Setting Up Secrets](https://github.com/win-laeyee/whoos_the_smartest/edit/main/README.md#-setting-up-secrets-1) for the set up.

## 🔧 Run Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
brew install ffmpeg
```

Run the VSCode Python Debugger and open [http://localhost:8000](http://localhost:8000) with your browser to see the Swagger UI.

### 🔑 Setting Up Secrets

1. Create a secrets folder:

- Path: `backend/secrets/`
- Files to include:
  - `firebase_sdk.json`
  - `firebase_service_account_key.json`
  - `google_gemini_credentials.json`

2. Obtain Keys:

- **Firebase SDK**:
  - Follow [this guide](https://firebase.google.com/docs/web/setup) to get the `firebase_sdk.json`.
- **Firebase Service Account Key**:
  - Follow [the guide](https://firebase.google.com/docs/admin/setup) here to download the `firebase_service_account_key.json`.
- **Google Gemini API Key**:
  - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey) and put it in `google_gemini_credentials.json`.

Make sure these files are placed correctly in the `backend/secrets/` directory before running the backend.

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

🎉 Whoots Whoots Whooray for Learning!
