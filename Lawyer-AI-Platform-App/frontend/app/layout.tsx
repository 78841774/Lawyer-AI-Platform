import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Lawyer AI Platform",
  description: "MVP Workspace for AI-assisted legal case analysis"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
