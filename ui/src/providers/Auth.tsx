"use client";

import {
  createContext,
  useContext,
  ReactNode,
  useState,
  useEffect,
} from "react";

interface AuthSession {
  accessToken: string;
}

interface AuthContextType {
  session: AuthSession | null;
}

const AuthContext = createContext<AuthContextType>({ session: null });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(null);

  useEffect(() => {
    // Initialize with a default token or implement your auth logic
    setSession({
      accessToken: process.env.NEXT_PUBLIC_LANGSMITH_API_KEY || "demo-token",
    });
  }, []);

  return (
    <AuthContext.Provider value={{ session }}>{children}</AuthContext.Provider>
  );
}

export const useAuthContext = () => useContext(AuthContext);
