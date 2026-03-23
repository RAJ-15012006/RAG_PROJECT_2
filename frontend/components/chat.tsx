"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { Header } from "./header";
import { ChatInput } from "./chat-input";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources: number[];
}

const BACKEND_URL = "http://localhost:8002/api/chat";

export function Chat() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hello! I'm your **Transformer Research Assistant**. I've analyzed the *Attention Is All You Need* paper. Ask me anything about it! 🚀",
      sources: [],
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const handleSend = async (question: string) => {
    const userMsg: Message = { role: "user", content: question, sources: [] };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const response = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) throw new Error("Backend error");
      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullAnswer = "";
      let sources: number[] = [];
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (!line.startsWith("data: ")) continue;
          const dataStr = line.slice(6).trim();
          if (dataStr === "[DONE]") break;

          try {
            const data = JSON.parse(dataStr);
            if (data.type === "answer") {
              fullAnswer += data.content;
            } else if (data.type === "sources") {
              sources = data.content;
            }
          } catch {
            continue;
          }
        }
      }

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: fullAnswer, sources },
      ]);
    } catch (err) {
      const errorMsg =
        err instanceof Error && err.message.includes("Failed to fetch")
          ? "Cannot connect to the backend. Make sure the FastAPI server is running on port 8002."
          : `Error: ${err instanceof Error ? err.message : "Unknown error"}`;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `❌ ${errorMsg}`, sources: [] },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen w-full">
      {/* Header */}
      <Header />

      {/* Messages */}
      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto px-4 py-4 space-y-4"
        id="chat-messages"
      >
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`msg-animate flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
              style={{ animationDelay: `${i * 0.05}s` }}
            >
              {msg.role === "user" ? (
                <UserBubble content={msg.content} />
              ) : (
                <AssistantBubble content={msg.content} sources={msg.sources} />
              )}
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start msg-animate">
              <div className="glass-message rounded-2xl rounded-bl-sm px-5 py-4 max-w-[85%]">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-white/60 font-medium">Thinking</span>
                  <span className="typing-dot" />
                  <span className="typing-dot" />
                  <span className="typing-dot" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading} />
    </div>
  );
}

/* ── User Bubble ──────────────────────────────────────────── */
function UserBubble({ content }: { content: string }) {
  return (
    <div className="max-w-[80%] px-5 py-3 rounded-2xl rounded-br-sm bg-gradient-to-br from-indigo-500 to-violet-700 text-white text-[15px] font-medium leading-relaxed shadow-[0_8px_32px_oklch(0.5_0.25_270_/_35%)] border border-white/10">
      {content}
    </div>
  );
}

/* ── Assistant Bubble ─────────────────────────────────────── */
function AssistantBubble({
  content,
  sources,
}: {
  content: string;
  sources: number[];
}) {
  // Simple markdown bold/italic rendering
  const rendered = content
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");

  return (
    <div className="max-w-[85%] glass-message rounded-2xl rounded-bl-sm px-6 py-5">
      <div
        className="text-[15px] leading-relaxed text-white/95 font-normal"
        dangerouslySetInnerHTML={{ __html: rendered }}
      />
      {sources.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {sources.map((page) => (
            <span
              key={page}
              className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-indigo-500/15 border border-indigo-400/20 text-indigo-300"
            >
              📄 Page {page}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
