import { useEffect, useState } from "react";
import { uploadPDF, addText, addYouTube, queryAPI, getSources } from "./api/api";

export default function App() {
  const [file, setFile] = useState(null);
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [sourceIds, setSourceIds] = useState([]);
  const [activeTab, setActiveTab] = useState("pdf");
  const [textTitle, setTextTitle] = useState("");
  const [textContent, setTextContent] = useState("");
  const [youtubeTitle, setYoutubeTitle] = useState("");
  const [youtubeUrl, setYoutubeUrl] = useState("");

  useEffect(() => {
    const loadSources = async () => {
      const data = await getSources();
      setSources(data);

      if (data.length > 0) {
        setSourceIds([data[data.length - 1].source_id]);
      }
    };

    loadSources();
  }, []);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);

    try {
      const res = await uploadPDF(file);

      setSources((prev) => 
        {
          const exists = prev.some((source) => source.source_id === res.source_id);
          return exists ? prev : [...prev, res];
        });
      setSourceIds([res.source_id]);
      setMessages([{ role: "system", text: `Uploaded: ${res.title}` }]);
      setFile(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAddText = async () => {

    if (!textTitle.trim() || !textContent.trim()) return;

    setLoading(true);

    try {
      const res = await addText(textTitle, textContent);

      setSources((prev) => [...prev, res]);
      setSourceIds([res.source_id]);
      setMessages([{ role: "system", text: `Added text source: ${res.title}` }]);

      setTextTitle("");
      setTextContent("");
    } finally {
      setLoading(false);
    }
  };

  const handleAddYouTube = async () => {
    if (!youtubeTitle.trim() || !youtubeUrl.trim()) return;

    setLoading(true);

    try {
      const res = await addYouTube(youtubeTitle, youtubeUrl);

      setSources((prev) => [...prev, res]);
      setSourceIds([res.source_id]);
      setMessages([{ role: "system", text: `Added YouTube source: ${res.title}` }]);

      setYoutubeTitle("");
      setYoutubeUrl("");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim() || sourceIds.length === 0) return;

    const currentQuestion = question;

    setMessages((prev) => [...prev, { role: "user", text: currentQuestion }]);
    setQuestion("");
    setLoading(true);

    try {
      const res = await queryAPI(currentQuestion, sourceIds);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: res.answer,
          sources: res.sources || [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-100">
      <aside className="flex h-screen w-80 shrink-0 flex-col overflow-hidden border-r border-slate-800 bg-slate-900/80 p-5">
        <div>
          <h1 className="text-xl font-semibold">AI Knowledge Assistant</h1>
          <p className="mt-1 text-sm text-slate-400">
            Upload sources and ask grounded questions.
          </p>
        </div>

        <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950 p-4">
          <div className="mb-4 grid grid-cols-3 rounded-lg bg-slate-900 p-1 text-xs">
            {["pdf", "text", "youtube"].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`rounded-md px-2 py-2 capitalize ${
                  activeTab === tab
                    ? "bg-blue-600 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {activeTab === "pdf" && (
            <div>
              <h2 className="mb-3 text-sm font-semibold text-slate-200">
                Upload PDF
              </h2>

              <input
                type="file"
                accept=".pdf"
                onChange={(e) => setFile(e.target.files[0])}
                className="block w-full cursor-pointer rounded-lg border border-slate-700 bg-slate-900 text-sm text-slate-300 file:mr-3 file:border-0 file:bg-blue-600 file:px-3 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-blue-500"
              />

              <button
                onClick={handleUpload}
                disabled={!file || loading}
                className="mt-3 w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Processing..." : "Upload & Index"}
              </button>
            </div>
          )}

          {activeTab === "text" && (
            <div>
              <h2 className="mb-3 text-sm font-semibold text-slate-200">
                Add Text Source
              </h2>

              <input
                value={textTitle}
                onChange={(e) => setTextTitle(e.target.value)}
                placeholder="Title"
                className="mb-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-500"
              />

              <textarea
                value={textContent}
                onChange={(e) => setTextContent(e.target.value)}
                placeholder="Paste text here..."
                rows={5}
                className="w-full resize-none rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-500"
              />

              <button
                onClick={handleAddText}
                disabled={!textTitle.trim() || !textContent.trim() || loading}
                className="mt-3 w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Processing..." : "Add & Index Text"}
              </button>
            </div>
          )}

          {activeTab === "youtube" && (
            <div>
              <h2 className="mb-3 text-sm font-semibold text-slate-200">
                Add YouTube Video
              </h2>

              <input
                value={youtubeTitle}
                onChange={(e) => setYoutubeTitle(e.target.value)}
                placeholder="Title"
                className="mb-2 w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-500"
              />

              <input
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="YouTube URL"
                className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-500"
              />

              <button
                onClick={handleAddYouTube}
                disabled={!youtubeTitle.trim() || !youtubeUrl.trim() || loading}
                className="mt-3 w-full rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Processing..." : "Add & Index Video"}
              </button>
            </div>
          )}
        </div>
        
      </aside>

      <main className="flex min-w-0 flex-1 flex-col overflow-hidden">
        <header className="shrink-0 border-b border-slate-800 px-6 py-4">
          <h2 className="text-lg font-semibold">Document Chat</h2>
          <p className="text-sm text-slate-400">
            Answers are generated only from indexed sources.
          </p>
        </header>

        <section className="min-h-0 flex-1 overflow-y-auto px-6 py-6">
          {messages.length === 0 ? (
            <div className="mx-auto mt-24 max-w-2xl text-center">
              <h2 className="text-3xl font-semibold text-slate-200">
                Ask questions over your documents
              </h2>
              <p className="mt-3 text-slate-400">
                Upload a PDF, then ask for summaries, skills, experience, risks,
                action items, or comparisons.
              </p>
            </div>
          ) : (
            <div className="mx-auto max-w-4xl space-y-5">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-2xl rounded-2xl px-4 py-3 text-sm leading-6 shadow-sm ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : msg.role === "system"
                        ? "border border-slate-800 bg-slate-900 text-slate-300"
                        : "border border-slate-800 bg-slate-900 text-slate-100"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{msg.text}</p>

                    {msg.sources?.length > 0 && (
                      <div className="mt-4 border-t border-slate-700 pt-3">
                        <div className="mb-2 text-xs font-semibold text-slate-400">
                          Sources
                        </div>
                        <div className="space-y-1">
                          {msg.sources.map((s, i) => (
                            <div
                              key={i}
                              className="rounded-md bg-slate-950 px-3 py-2 text-xs text-slate-400"
                            >
                              {s.title} · chunk {s.chunk_index}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm text-slate-400">
                    Thinking...
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        <footer className="shrink-0 border-t border-slate-800 p-4">
          <div className="mx-auto flex max-w-4xl gap-3">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleAsk();
              }}
              placeholder={
                sourceIds.length === 0
                  ? "Upload or select a source first..."
                  : "Ask anything about your selected source..."
              }
              className="flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-slate-100 outline-none placeholder:text-slate-500 focus:border-blue-500"
            />

            <button
              onClick={handleAsk}
              disabled={loading || !question.trim() || sourceIds.length === 0}
              className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </footer>
      </main>
    </div>
  );
}