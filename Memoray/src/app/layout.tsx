// src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";
import { Inter, Playfair_Display } from "next/font/google";
import { UserProvider } from "@auth0/nextjs-auth0/client";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const playfair = Playfair_Display({ subsets: ["latin"], variable: "--font-playfair", style: ["italic", "normal"] });

export const metadata: Metadata = {
  title: "Memoray — Memory assistance for everyday life",
  description:
    "Memoray uses Ray-Ban Meta glasses to recognize familiar faces, give gentle prompts, and help practice memory.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${playfair.variable} bg-hero min-h-dvh`}>
        <UserProvider>
          {children}
        </UserProvider>
      </body>
    </html>
  );
}
