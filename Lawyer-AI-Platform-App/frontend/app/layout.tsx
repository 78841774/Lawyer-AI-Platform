import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AIHome.law",
  description: "法律 AI 工作空间"
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
