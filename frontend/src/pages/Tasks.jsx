import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../lib/api";

const STATUSES = ["todo", "in_progress", "done"];
const PRIORITIES = ["low", "medium", "high"];

export default function Tasks() {
  const { logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", priority: "medium", status: "todo" });

  const loadTasks = () => {
    const params = filter ? { status: filter } : {};
    api.get("/tasks", { params }).then((res) => setTasks(res.data.data));
  };

  useEffect(loadTasks, [filter]);

  const createTask = async (e) => {
    e.preventDefault();
    if (!form.title.trim()) return;
    await api.post("/tasks", form);
    setForm({ title: "", description: "", priority: "medium", status: "todo" });
    setShowForm(false);
    loadTasks();
  };

  const updateStatus = async (task, newStatus) => {
    await api.put(`/tasks/${task.id}`, { status: newStatus });
    loadTasks();
  };

  const deleteTask = async (task) => {
    await api.delete(`/tasks/${task.id}`);
    loadTasks();
  };

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
          <Link to="/dashboard" className="text-sm text-slate-400 hover:text-white transition">
            Dashboard
          </Link>
          <Link to="/ai" className="text-sm text-slate-400 hover:text-white transition">
            AI Chat
          </Link>
          <button
            onClick={logout}
            className="px-3 py-1.5 text-sm border border-slate-600 rounded-lg hover:bg-slate-700 transition"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Tasks</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="px-4 py-2 bg-purple-600 rounded-lg text-sm hover:bg-purple-500 transition"
          >
            {showForm ? "Cancel" : "+ New Task"}
          </button>
        </div>

        {showForm && (
          <form
            onSubmit={createTask}
            className="bg-slate-800 border border-slate-700 rounded-xl p-6 mb-8 space-y-4"
          >
            <input
              type="text"
              placeholder="Task title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              required
              className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500"
            />
            <textarea
              placeholder="Description (optional)"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              rows={2}
              className="w-full px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500 resize-none"
            />
            <div className="flex gap-4">
              <select
                value={form.priority}
                onChange={(e) => setForm({ ...form, priority: e.target.value })}
                className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500"
              >
                {PRIORITIES.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </select>
              <select
                value={form.status}
                onChange={(e) => setForm({ ...form, status: e.target.value })}
                className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500"
              >
                {STATUSES.map((s) => (
                  <option key={s} value={s}>
                    {s.replace("_", " ")}
                  </option>
                ))}
              </select>
            </div>
            <button
              type="submit"
              className="px-6 py-2.5 bg-purple-600 rounded-lg font-semibold hover:bg-purple-500 transition"
            >
              Create Task
            </button>
          </form>
        )}

        <div className="flex gap-2 mb-6 flex-wrap">
          {["", ...STATUSES].map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`px-3 py-1.5 text-sm rounded-lg transition ${
                filter === s
                  ? "bg-purple-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              {s ? s.replace("_", " ") : "All"}
            </button>
          ))}
        </div>

        <div className="space-y-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="bg-slate-800 border border-slate-700 rounded-xl px-5 py-4"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="font-medium text-lg">{task.title}</div>
                  {task.description && (
                    <div className="text-sm text-slate-400 mt-1">{task.description}</div>
                  )}
                  <div className="flex gap-2 mt-3">
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
                    <span
                      className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                        task.priority === "high"
                          ? "bg-red-500/20 text-red-400"
                          : task.priority === "medium"
                          ? "bg-orange-500/20 text-orange-400"
                          : "bg-slate-500/20 text-slate-400"
                      }`}
                    >
                      {task.priority}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2 ml-4">
                  {STATUSES.filter((s) => s !== task.status).map((s) => (
                    <button
                      key={s}
                      onClick={() => updateStatus(task, s)}
                      className="text-xs px-2 py-1 border border-slate-600 rounded hover:bg-slate-700 transition"
                      title={`Move to ${s.replace("_", " ")}`}
                    >
                      {s === "todo" ? "TODO" : s === "in_progress" ? "IP" : "Done"}
                    </button>
                  ))}
                  <button
                    onClick={() => deleteTask(task)}
                    className="text-xs px-2 py-1 border border-red-600/50 text-red-400 rounded hover:bg-red-500/10 transition"
                  >
                    Del
                  </button>
                </div>
              </div>
            </div>
          ))}
          {tasks.length === 0 && (
            <div className="text-center text-slate-500 py-10">
              {filter ? "No tasks with this status" : "No tasks yet"}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
