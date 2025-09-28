// src/components/site/Hero.tsx
"use client";

import Link from "next/link";
// import LoginButton from "@/components/auth/LoginButton";
import LoginButton from "../auth/LoginButton";


export function Hero() {
  return (
    <section className="section pt-24">
      <div className="flex flex-col gap-8">
        <div className="badge w-fit">Built for Ray-Ban Meta smart glasses</div>

        <h1 className="heading-hero">
          Gentle <span className="font-accent">memory</span> cues.
        </h1>

        <p className="text-lg/loose text-white/80 max-w-3xl">
          Face recognition and reminders—private by default. Optional speech check-ins to watch
          trends early.
        </p>

        <div className="flex items-center gap-4">
          {/* Primary CTA now drives Auth0 with animation */}
          <LoginButton variant="primary">Get Started</LoginButton>

          {/* Secondary link remains a simple anchor */}
          <Link
            href="#how-it-works"
            className="glass px-5 py-3 rounded-full text-white/90 hover:bg-white/10 transition"
          >
            How it works
          </Link>
        </div>
      </div>
    </section>
  );
}
