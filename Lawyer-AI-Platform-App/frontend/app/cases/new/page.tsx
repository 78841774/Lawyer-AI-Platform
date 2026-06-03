"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { ApiError, createCase, getCurrentUser, getWorkspace, getWorkspaces } from "@/services/api";
import type { CaseCreatePayload } from "@/services/api";
import type { User, Workspace } from "@/types";

type IntakeFormState = {
  title: string;
  client_name: string;
  counterparty_name: string;
  case_type: string;
  contract_type: string;
  dispute_amount: string;
  jurisdiction: string;
  objective: string;
  intake_notes: string;
};

const initialFormState: IntakeFormState = {
  title: "",
  client_name: "",
  counterparty_name: "",
  case_type: "",
  contract_type: "",
  dispute_amount: "",
  jurisdiction: "",
  objective: "",
  intake_notes: ""
};

export default function NewCasePage() {
  const router = useRouter();
  const [form, setForm] = useState<IntakeFormState>(initialFormState);
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

  function updateField(field: keyof IntakeFormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const title = form.title.trim();
    if (!title) {
      setStatus("error");
      setMessage("请输入案件标题。");
      return;
    }

    setStatus("loading");
    setMessage("正在创建案件...");
    try {
      const payload: CaseCreatePayload = {
        title,
        client_name: normalizeOptional(form.client_name),
        counterparty_name: normalizeOptional(form.counterparty_name),
        case_type: normalizeOptional(form.case_type),
        contract_type: normalizeOptional(form.contract_type),
        dispute_amount: normalizeOptional(form.dispute_amount),
        jurisdiction: normalizeOptional(form.jurisdiction),
        objective: normalizeOptional(form.objective),
        intake_notes: normalizeOptional(form.intake_notes)
      };
      const newCase = await createCase(payload);
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
          description="请录入案件的基础业务信息。材料上传、事实抽取、法律分析和报告生成可在案件详情页继续完成。"
          action={
            <Link
              href="/cases"
              className="rounded-md border border-line bg-white px-4 py-2 text-sm font-medium text-ink shadow-sm hover:border-accent"
            >
              返回案件列表
            </Link>
          }
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
            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid gap-4 md:grid-cols-2">
                <TextField
                  label="案件标题"
                  value={form.title}
                  onChange={(value) => updateField("title", value)}
                  placeholder="例如：买卖合同货款争议"
                  required
                />
                <TextField
                  label="案件类型"
                  value={form.case_type}
                  onChange={(value) => updateField("case_type", value)}
                  placeholder="例如：买卖合同纠纷"
                />
                <TextField
                  label="客户名称"
                  value={form.client_name}
                  onChange={(value) => updateField("client_name", value)}
                  placeholder="例如：测试客户A"
                />
                <TextField
                  label="对方名称"
                  value={form.counterparty_name}
                  onChange={(value) => updateField("counterparty_name", value)}
                  placeholder="例如：测试对方B"
                />
                <TextField
                  label="合同类型"
                  value={form.contract_type}
                  onChange={(value) => updateField("contract_type", value)}
                  placeholder="例如：货物买卖合同"
                />
                <TextField
                  label="争议金额"
                  value={form.dispute_amount}
                  onChange={(value) => updateField("dispute_amount", value)}
                  placeholder="例如：10万-50万"
                />
                <TextField
                  label="管辖地区"
                  value={form.jurisdiction}
                  onChange={(value) => updateField("jurisdiction", value)}
                  placeholder="例如：中国大陆"
                />
                <TextField
                  label="案件目标"
                  value={form.objective}
                  onChange={(value) => updateField("objective", value)}
                  placeholder="例如：追索货款并评估调解方案"
                />
              </div>
              <TextArea
                label="Intake 备注"
                value={form.intake_notes}
                onChange={(value) => updateField("intake_notes", value)}
                placeholder="记录案件来源、初步沟通重点或后续跟进事项。"
              />
              <div className="flex flex-wrap items-center gap-3">
                <Button type="submit" disabled={status === "loading"}>
                  {status === "loading" ? "创建中..." : "创建案件"}
                </Button>
                <Link href="/cases" className="text-sm font-medium text-muted hover:text-accent">
                  返回案件列表
                </Link>
              </div>
              {message ? (
                <div className="rounded-md border border-line bg-paper px-3 py-2 text-sm text-muted">
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

function TextField({
  label,
  value,
  onChange,
  placeholder,
  required = false
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  required?: boolean;
}) {
  return (
    <label className="block text-sm font-medium text-ink">
      {label}
      {required ? <span className="ml-1 text-accent">*</span> : null}
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-accent"
        placeholder={placeholder}
      />
    </label>
  );
}

function TextArea({
  label,
  value,
  onChange,
  placeholder
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}) {
  return (
    <label className="block text-sm font-medium text-ink">
      {label}
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 min-h-28 w-full rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-accent"
        placeholder={placeholder}
      />
    </label>
  );
}

function normalizeOptional(value: string) {
  const trimmed = value.trim();
  return trimmed ? trimmed : null;
}
