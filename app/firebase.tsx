"use client";

import { useEffect, useCallback } from "react";
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, EmailAuthProvider } from "firebase/auth";
import * as firebaseui from "firebaseui";
import "firebaseui/dist/firebaseui.css";

// Firebase configuration object
const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_APP_ID,
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const FirebaseAuthUI: React.FC<{ onLoginSuccess: () => void }> = ({
  onLoginSuccess,
}) => {
  const loadFirebaseui = useCallback(async () => {
    const firebaseui = await import("firebaseui");
    const firebaseUi =
      firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
    firebaseUi.start("#firebaseui-auth-container", {
      signInFlow: "popup",
      signInOptions: [
        {
          provider: GoogleAuthProvider.PROVIDER_ID,
        },
        {
          provider: EmailAuthProvider.PROVIDER_ID,
        },
      ],
      callbacks: {
        signInSuccessWithAuthResult: (authResult, redirectUrl) => {
          if (onLoginSuccess) {
            onLoginSuccess();
          }
          return false; // Prevent automatic redirect
        },
      },
      credentialHelper: firebaseui.auth.CredentialHelper.GOOGLE_YOLO,
    });
  }, [onLoginSuccess]);

  useEffect(() => {
    loadFirebaseui();
  }, [loadFirebaseui]);

  return <div id="firebaseui-auth-container"></div>;
};
export default FirebaseAuthUI;
export { auth };
