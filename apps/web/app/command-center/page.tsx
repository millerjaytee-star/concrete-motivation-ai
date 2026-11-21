import type { Metadata } from "next";
import { CommandCenter } from "@/components/CommandCenter";
import { commandAuthConfigured } from "@/lib/command-auth";
import "./command.css";

export const dynamic = "force-dynamic";
export const metadata: Metadata = {
  title: "Command Center",
  description: "Concrete Motivation owner workspace",
  robots: { index: false, follow: false }
};

export default function CommandCenterPage() {
  return <CommandCenter signInAvailable={commandAuthConfigured()} />;
}
