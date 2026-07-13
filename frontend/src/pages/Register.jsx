import { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register, googleLogin } = useAuth();
  const navigate = useNavigate();
  const googleBtnRef = useRef(null);

  useEffect(() => {
    const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    if (!clientId || !googleBtnRef.current) return;

    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.onload = () => {
      if (window.google?.accounts?.id) {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: async (resp) => {
            setError("");
            try {
              await googleLogin(resp.credential);
              navigate("/dashboard");
            } catch (err) {
              setError(err.response?.data?.message || "Google login failed");
            }
          },
        });
        window.google.accounts.id.renderButton(googleBtnRef.current, {
          theme: "filled_black",
          size: "large",
          width: "100%",
          text: "continue_with",
        });
      }
    };
    document.head.appendChild(script);
  }, [googleLogin, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(email, password, name);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <Link
          to="/"
          className="block text-center text-2xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent mb-8"
        >
          TaskFlow AI
        </Link>
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-8">
          <h1 className="text-2xl font-bold text-white mb-6">Create Account</h1>
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg mb-4 text-sm">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm text-slate-400 mb-1">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500 transition"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-1">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500 transition"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-purple-600 rounded-lg text-white font-semibold hover:bg-purple-500 disabled:opacity-50 transition"
            >
              {loading ? "Creating account..." : "Create Account"}
            </button>
          </form>
          <div className="flex items-center gap-3 my-6">
            <div className="flex-1 border-t border-slate-600"></div>
            <span className="text-xs text-slate-500">OR</span>
            <div className="flex-1 border-t border-slate-600"></div>
          </div>
          <div ref={googleBtnRef} className="w-full"></div>
          <p className="text-center text-slate-400 text-sm mt-6">
            Already have an account?{" "}
            <Link to="/login" className="text-purple-400 hover:underline">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
