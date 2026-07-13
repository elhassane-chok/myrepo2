import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../lib/api";

const DEFAULT_MODELS = [
  { id: "gpt-4o", name: "GPT-4o", description: "Fastest, most capable" },
  { id: "gpt-4.1", name: "GPT-4.1", description: "Latest generation" },
  { id: "gpt-4.1-mini", name: "GPT-4.1 Mini", description: "Fast and efficient" },
];

export default function AIPlayground() {
  const { logout } = useAuth();
  const [mode, setMode] = useState("chat");
  const [models, setModels] = useState(DEFAULT_MODELS);
  const [selectedModel, setSelectedModel] = useState("gpt-4o");

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const messagesEnd = useRef(null);

  const [prompt, setPrompt] = useState("");
  const [systemPrompt, setSystemPrompt] = useState("");
  const [playgroundResult, setPlaygroundResult] = useState("");
  const [playgroundLoading, setPlaygroundLoading] = useState(false);

  useEffect(() => {
    api.get("/ai/models").then((res) => {
      if (res.data.data?.length) setModels(res.data.data);
    });
  }, []);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendChat = async () => {
    if (!input.trim() || streaming) return;
    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setStreaming(true);

    try {
      const res = await fetch("/api/ai/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
          model: selectedModel,
          conversation_id: null,
        }),
      });

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantMsg = "";

      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                assistantMsg += data.content;
                setMessages((prev) => {
                  const updated = [...prev];
                  updated[updated.length - 1] = {
                    role: "assistant",
                    content: assistantMsg,
                  };
                  return updated;
                });
              }
            } catch {
              // skip malformed JSON
            }
          }
        }
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          role: "assistant",
          content: "Error: Failed to get response. Make sure your API key is configured.",
        },
      ]);
    } finally {
      setStreaming(false);
    }
  };

  const sendPlayground = async () => {
    if (!prompt.trim()) return;
    setPlaygroundLoading(true);
    setPlaygroundResult("");
    try {
      const res = await fetch("/api/ai/playground", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          system_prompt: systemPrompt || undefined,
          model: selectedModel,
        }),
      });
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let result = "";
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                result += data.content;
                setPlaygroundResult(result);
              }
            } catch {
              // skip
            }
          }
        }
      }
    } catch {
      setPlaygroundResult("Error: Failed to get response.");
    } finally {
      setPlaygroundLoading(false);
    }
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
          <Link to="/tasks" className="text-sm text-slate-400 hover:text-white transition">
            Tasks
          </Link>
          <Link to="/dashboard" className="text-sm text-slate-400 hover:text-white transition">
            Dashboard
          </Link>
          <button
            onClick={logout}
            className="px-3 py-1.5 text-sm border border-slate-600 rounded-lg hover:bg-slate-700 transition"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">AI Playground</h1>
          <div className="flex gap-2">
            <button
              onClick={() => setMode("chat")}
              className={`px-4 py-2 rounded-lg text-sm transition ${
                mode === "chat" ? "bg-purple-600" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              Chat with Tasks
            </button>
            <button
              onClick={() => setMode("playground")}
              className={`px-4 py-2 rounded-lg text-sm transition ${
                mode === "playground" ? "bg-purple-600" : "bg-slate-800 text-slate-400 hover:bg-slate-700"
              }`}
            >
              Playground
            </button>
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm text-slate-400 mb-2">Model</label>
          <div className="flex gap-2 flex-wrap">
            {models.map((m) => (
              <button
                key={m.id}
                onClick={() => setSelectedModel(m.id)}
                className={`px-4 py-2 rounded-lg text-sm transition ${
                  selectedModel === m.id
                    ? "bg-purple-600 text-white"
                    : "bg-slate-800 text-slate-400 hover:bg-slate-700"
                }`}
                title={m.description}
              >
                {m.name || m.id}
              </button>
            ))}
          </div>
        </div>

        {mode === "chat" ? (
          <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
            <div className="h-[500px] overflow-y-auto p-6 space-y-4">
              {messages.length === 0 && (
                <div className="text-center text-slate-500 py-20">
                  Ask anything about your tasks. The AI has access to your task data.
                </div>
              )}
              {messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[75%] px-4 py-3 rounded-2xl text-sm whitespace-pre-wrap ${
                      msg.role === "user"
                        ? "bg-purple-600 text-white"
                        : "bg-slate-700 text-slate-200"
                    }`}
                  >
                    {msg.content || (streaming && i === messages.length - 1 ? "..." : "")}
                  </div>
                </div>
              ))}
              <div ref={messagesEnd} />
            </div>
            <div className="border-t border-slate-700 p-4">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  sendChat();
                }}
                className="flex gap-3"
              >
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about your tasks..."
                  disabled={streaming}
                  className="flex-1 px-4 py-2.5 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-purple-500 disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={streaming || !input.trim()}
                  className="px-6 py-2.5 bg-purple-600 rounded-lg font-semibold hover:bg-purple-500 disabled:opacity-50 transition"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div>
              <label className="block text-sm text-slate-400 mb-2">System Prompt (optional)</label>
              <textarea
                value={systemPrompt}
                onChange={(e) => setSystemPrompt(e.target.value)}
                rows={3}
                placeholder="You are a helpful assistant..."
                className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-purple-500 resize-none"
              />
            </div>
            <div>
              <label className="block text-sm text-slate-400 mb-2">Prompt</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={5}
                placeholder="Write your prompt here..."
                className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-purple-500 resize-none"
              />
            </div>
            <button
              onClick={sendPlayground}
              disabled={playgroundLoading || !prompt.trim()}
              className="px-6 py-2.5 bg-purple-600 rounded-lg font-semibold hover:bg-purple-500 disabled:opacity-50 transition"
            >
              {playgroundLoading ? "Generating..." : "Run Prompt"}
            </button>
            {playgroundResult && (
              <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
                <div className="text-sm text-slate-400 mb-3">Output</div>
                <div className="text-sm whitespace-pre-wrap text-slate-200">
                  {playgroundResult}
                </div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
