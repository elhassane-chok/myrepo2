import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <nav className="flex items-center justify-between px-6 py-4">
        <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
          TaskFlow AI
        </span>
        <div className="flex gap-3">
          {user ? (
            <Link
              to="/dashboard"
              className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-500 transition"
            >
              Dashboard
            </Link>
          ) : (
            <>
              <Link
                to="/login"
                className="px-4 py-2 border border-white/20 rounded-lg hover:bg-white/10 transition"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 bg-purple-600 rounded-lg hover:bg-purple-500 transition"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-24 text-center">
        <h1 className="text-5xl md:text-7xl font-bold mb-6">
          Manage Tasks with{" "}
          <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">
            AI Power
          </span>
        </h1>
        <p className="text-xl text-white/60 mb-10 max-w-2xl mx-auto">
          TaskFlow AI combines smart task management with AI assistants.
          Chat about your tasks, get insights, and boost your productivity.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/register"
            className="px-8 py-3 bg-purple-600 rounded-lg text-lg font-semibold hover:bg-purple-500 transition"
          >
            Start Free
          </Link>
          <a
            href="#features"
            className="px-8 py-3 border border-white/20 rounded-lg text-lg hover:bg-white/10 transition"
          >
            Learn More
          </a>
        </div>
      </main>

      <section id="features" className="max-w-5xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { title: "Task Management", desc: "Create, organize, and track tasks with priorities, statuses, and projects." },
            { title: "AI Chat", desc: "Talk to an AI assistant about your tasks. Get summaries, suggestions, and insights." },
            { title: "Model Playground", desc: "Choose between GPT-4o, GPT-4.1, and more. Write custom prompts and compare outputs." },
          ].map((f) => (
            <div
              key={f.title}
              className="p-6 bg-white/5 border border-white/10 rounded-xl hover:border-purple-500/50 transition"
            >
              <h3 className="text-xl font-semibold mb-3">{f.title}</h3>
              <p className="text-white/50">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
