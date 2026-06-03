"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { ApiError, createCase } from "@/services/api";

export default function NewCasePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const resolvedTitle = title.trim();
    if (!resolvedTitle) {
      setStatus("error");
      setMessage("请输入新案件标题。");
      return;
    }

    setStatus("loading");
    setMessage("正在创建案件...");
    try {
      const newCase = await createCase(resolvedTitle);
      setMessage("案件已创建。");
      router.push(`/cases/${newCase.case_id}`);
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof ApiError ? error.message : "创建案件失败。");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 案件"
          title="创建案件"
          description="创建新的法律 AI 工作空间记录。"
        />

        <Card>
          <CardBody>
            <form onSubmit={handleSubmit}>
              <label htmlFor="title" className="text-sm font-medium text-ink">
                新案件标题
              </label>
              <input
                id="title"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                className="mt-2 w-full rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-accent"
                placeholder="例如：演示合同纠纷案件"
              />
              <Button type="submit" disabled={status === "loading"} className="mt-4">
                {status === "loading" ? "正在创建..." : "创建案件"}
              </Button>
              {message ? (
                <div className="mt-4 rounded-md border border-line bg-paper px-3 py-2 text-sm text-muted">
                  {message}
                </div>
              ) : null}
            </form>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}
