import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../lib/api";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, todo: 0, in_progress: 0, done: 0 });

  useEffect(() => {
    api.get("/tasks").then((res) => {
      const all = res.data.data;
      setTasks(all);
      setStats({
        total: all.length,
        todo: all.filter((t) => t.status === "todo").length,
        in_progress: all.filter((t) => t.status === "in_progress").length,
        done: all.filter((t) => t.status === "done").length,
      });
    });
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <nav className="flex items-center justify-between px-6 py-4 border-b border-slate-700">
        <Link
          to="/"
          className="text-xl font-bold bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent"
        >
          TaskFlow AI
        </Link>
        <div className="flex items-center gap-4">
          <span className="text-sm text-slate-400">{user?.name}</span>
          <button
            onClick={logout}
            className="px-3 py-1.5 text-sm border border-slate-600 rounded-lg hover:bg-slate-700 transition"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-10">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          {[
            { label: "Total", value: stats.total, color: "text-white" },
            { label: "To Do", value: stats.todo, color: "text-blue-400" },
            { label: "In Progress", value: stats.in_progress, color: "text-yellow-400" },
            { label: "Done", value: stats.done, color: "text-green-400" },
          ].map((s) => (
            <div key={s.label} className="bg-slate-800 border border-slate-700 rounded-xl p-5">
              <div className={`text-3xl font-bold ${s.color}`}>{s.value}</div>
              <div className="text-sm text-slate-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold">Recent Tasks</h2>
          <Link
            to="/tasks"
            className="px-4 py-2 bg-purple-600 rounded-lg text-sm hover:bg-purple-500 transition"
          >
            View All
          </Link>
        </div>

        <div className="space-y-3">
          {tasks.slice(0, 5).map((task) => (
            <div
              key={task.id}
              className="flex items-center justify-between bg-slate-800 border border-slate-700 rounded-xl px-5 py-4"
            >
              <div>
                <div className="font-medium">{task.title}</div>
                <div className="text-sm text-slate-400 mt-0.5">
                  {task.priority} priority
                </div>
              </div>
              <span
                className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                  task.status === "done"
                    ? "bg-green-500/20 text-green-400"
                    : task.status === "in_progress"
                    ? "bg-yellow-500/20 text-yellow-400"
                    : "bg-blue-500/20 text-blue-400"
                }`}
              >
                {task.status.replace("_", " ")}
              </span>
            </div>
          ))}
          {tasks.length === 0 && (
            <div className="text-center text-slate-500 py-10">
              No tasks yet. Create your first task!
            </div>
          )}
        </div>

        <div className="mt-10">
          <Link
            to="/ai"
            className="inline-flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-purple-600 to-cyan-600 rounded-xl font-semibold hover:opacity-90 transition"
          >
            Open AI Playground
          </Link>
        </div>
      </main>
    </div>
  );
}
