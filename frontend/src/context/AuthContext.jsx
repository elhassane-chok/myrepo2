import { createContext, useContext, useState, useEffect } from "react";
import api from "../lib/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("session_token");
    if (token) {
      api
        .get("/auth/me")
        .then((res) => setUser(res.data.data))
        .catch(() => localStorage.removeItem("session_token"))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    const res = await api.post("/auth/login", { email, password });
    const data = res.data.data;
    localStorage.setItem("session_token", "session");
    setUser(data);
    return data;
  };

  const register = async (email, password, name) => {
    const res = await api.post("/auth/register", { email, password, name });
    const data = res.data.data;
    localStorage.setItem("session_token", "session");
    setUser(data);
    return data;
  };

  const logout = async () => {
    await api.post("/auth/logout").catch(() => {});
    localStorage.removeItem("session_token");
    setUser(null);
  };

  const googleLogin = async (credential) => {
    const res = await api.post("/auth/google", { token: credential });
    const data = res.data.data;
    localStorage.setItem("session_token", "session");
    setUser(data);
    return data;
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, googleLogin, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
