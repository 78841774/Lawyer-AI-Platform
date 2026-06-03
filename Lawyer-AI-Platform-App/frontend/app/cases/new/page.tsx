"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { ApiError, createCase, getCurrentUser, getWorkspace, getWorkspaces } from "@/services/api";
import type { User, Workspace } from "@/types";

export default function NewCasePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadContext() {
      try {
        const [nextUser, workspaces] = await Promise.all([getCurrentUser(), getWorkspaces()]);
        const workspaceSummary = workspaces[0] ?? null;
        const nextWorkspace = workspaceSummary ? await getWorkspace(workspaceSummary.workspace_id) : null;
        setUser(nextUser);
        setWorkspace(nextWorkspace);
      } catch {
        setMessage("当前用户或工作空间暂不可用，请确认后端服务已启动。");
      }
    }
    void loadContext();
  }, []);

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
          description="创建后的案件将自动归属当前工作空间与当前用户。"
        />

        <Card>
          <CardBody>
            <div className="grid gap-4 md:grid-cols-2">
              <InfoRow label="当前用户" value={user ? `${user.display_name} / ${user.user_id}` : "-"} />
              <InfoRow label="当前工作空间" value={workspace ? `${workspace.name} / ${workspace.workspace_id}` : "-"} />
            </div>
          </CardBody>
        </Card>

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
