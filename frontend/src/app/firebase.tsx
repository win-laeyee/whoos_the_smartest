"use client";

import { useEffect, useCallback } from "react";
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, EmailAuthProvider } from "firebase/auth";
import * as firebaseui from "firebaseui";
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

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const FirebaseAuthUI: React.FC = () => {
  const loadFirebaseui = useCallback(async () => {
    const firebaseui = await import("firebaseui");
    const firebaseUi =
      firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);
    firebaseUi.start("#firebaseui-auth-container", {
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
  }, []);

  useEffect(() => {
    loadFirebaseui();
  }, []);

  return <div id="firebaseui-auth-container"></div>;
};
export default FirebaseAuthUI;
export { auth };
