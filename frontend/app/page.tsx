import { AnimatedBackground } from "@/components/background";
import { Chat } from "@/components/chat";

export default function Home() {
  return (
    <main className="relative h-screen w-full overflow-hidden">
      <AnimatedBackground />
      <Chat />
    </main>
  );
}
