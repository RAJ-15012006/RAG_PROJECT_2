"use client";

import { useState, useRef, type KeyboardEvent } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 pb-6 pt-2">
      <div className="glass-strong rounded-2xl p-1.5 flex items-end gap-2 transition-all focus-within:border-indigo-500/30 focus-within:shadow-[0_0_30px_oklch(0.55_0.25_270_/_15%)]">
        <textarea
          ref={inputRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about the Transformer paper..."
          disabled={disabled}
          rows={1}
          className="flex-1 bg-transparent text-white/90 placeholder:text-white/30 text-sm px-4 py-3 resize-none outline-none min-h-[44px] max-h-[120px] overflow-y-auto"
          style={{ lineHeight: "1.5" }}
          id="chat-input"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          className="shrink-0 w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white flex items-center justify-center transition-all hover:scale-105 hover:shadow-[0_0_20px_oklch(0.55_0.25_270_/_40%)] disabled:opacity-30 disabled:hover:scale-100 disabled:hover:shadow-none mb-0.5"
          id="send-button"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22L11 13L2 9L22 2Z" />
          </svg>
        </button>
      </div>
      <p className="text-center text-[10px] text-white/20 mt-2">
        Powered by RAG &bull; DeepSeek R1 &bull; ChromaDB
      </p>
    </div>
  );
}
