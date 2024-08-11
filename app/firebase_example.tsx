"use client";
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, EmailAuthProvider } from "firebase/auth";
import * as firebaseui from "firebaseui";
import { useEffect, useRef } from "react";
import "firebaseui/dist/firebaseui.css";

// Firebase configuration object
const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
};

// Initialize Firebase app
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and Google Auth Provider
const auth = getAuth(app);

const FirebaseAuthUI: React.FC = () => {
  const uiRef = useRef<firebaseui.auth.AuthUI | null>(null);

  useEffect(() => {
    if (!uiRef.current) {
      if (firebaseui.auth.AuthUI.getInstance()) {
        uiRef.current = firebaseui.auth.AuthUI.getInstance();
      } else {
        uiRef.current = new firebaseui.auth.AuthUI(auth);
      }

      if (uiRef.current) {
        uiRef.current.start("#firebaseui-auth-container", {
          signInSuccessUrl: "/upload",
          signInFlow: "popup",
          signInOptions: [
            {
              provider: GoogleAuthProvider.PROVIDER_ID,
            },
            {
              provider: EmailAuthProvider.PROVIDER_ID,
            },
          ],
          credentialHelper: firebaseui.auth.CredentialHelper.GOOGLE_YOLO,
        });
      }
    }
  }, []);

  return <div id="firebaseui-auth-container"></div>;
};

export default FirebaseAuthUI;
export { auth };
