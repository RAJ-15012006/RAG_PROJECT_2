"use client";

export function Header() {
  return (
    <div className="perspective-container w-full px-4 pt-6 pb-2">
      <div className="card-3d glass-strong rounded-2xl p-6 text-center max-w-2xl mx-auto glow-ring">
        {/* Glowing brain icon */}
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-br from-indigo-500/20 to-violet-500/20 border border-indigo-400/20 mb-3">
          <span className="text-3xl" role="img" aria-label="brain">🧠</span>
        </div>

        {/* Title */}
        <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-indigo-300 via-violet-300 to-purple-300 bg-clip-text text-transparent tracking-tight">
          Transformer Research Assistant
        </h1>

        {/* Subtitle */}
        <p className="mt-1.5 text-xs md:text-sm tracking-[0.25em] uppercase text-white/40 font-medium">
          Attention Is All You Need &bull; RAG System
        </p>

        {/* Status indicator */}
        <div className="mt-3 inline-flex items-center gap-2 px-3 py-1 rounded-full glass text-xs text-emerald-400/80">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          System Online
        </div>
      </div>
    </div>
  );
}
