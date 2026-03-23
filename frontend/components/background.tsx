"use client";

export function AnimatedBackground() {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      {/* Background image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/bg.jpg')" }}
      />

      {/* Dark overlay for readability */}
      <div className="absolute inset-0 bg-black/70" />

      {/* Grid overlay */}
      <div className="absolute inset-0 grid-pattern opacity-20" />

      {/* Floating orbs */}
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      {/* Radial vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_transparent_0%,_oklch(0.05_0.02_270_/_70%)_100%)]" />
    </div>
  );
}
