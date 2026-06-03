"use client";

import Link from "next/link";
import { ChangeEvent, useEffect, useState } from "react";
import {
  ApiError,
  applySkillToCase,
  CaseDetail,
  CaseSkillBinding,
  extractFacts,
  generateReport,
  getCaseDetail,
  getCaseSkills,
  getLLMStatus,
  getWorkspaceSkills,
  runLegalAnalysis,
  uploadMaterial,
  WorkspaceSkillRecord
} from "@/services/api";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import type { RuntimeStatus } from "@/types";

type ActionStatus = {
  loading: boolean;
  message: string;
  kind: "idle" | "success" | "error";
};

const initialActionStatus: ActionStatus = {
  loading: false,
  message: "",
  kind: "idle"
};

export function CaseDetailClient({ caseId }: { caseId: string }) {
  const [detail, setDetail] = useState<CaseDetail | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pageStatus, setPageStatus] = useState<ActionStatus>({
    ...initialActionStatus,
    loading: true,
    message: "正在加载案件..."
  });
  const [actionStatus, setActionStatus] = useState<ActionStatus>(initialActionStatus);
  const [availableSkills, setAvailableSkills] = useState<WorkspaceSkillRecord[]>([]);
  const [appliedSkills, setAppliedSkills] = useState<CaseSkillBinding[]>([]);
  const [runtime, setRuntime] = useState<RuntimeStatus | null>(null);

  useEffect(() => {
    void loadDetail();
  }, [caseId]);

  async function loadDetail() {
    setPageStatus({ loading: true, message: "正在加载案件...", kind: "idle" });
    try {
      const [nextDetail, nextAvailableSkills, nextAppliedSkills] = await Promise.all([
        getCaseDetail(caseId),
        getWorkspaceSkills(),
        getCaseSkills(caseId)
      ]);
      const nextRuntime = await getLLMStatus().catch(() => null);
      setDetail(nextDetail);
      setAvailableSkills(nextAvailableSkills);
      setAppliedSkills(nextAppliedSkills);
      setRuntime(nextRuntime);
      setPageStatus(initialActionStatus);
    } catch (error) {
      setPageStatus({
        loading: false,
        message: error instanceof ApiError ? error.message : "加载案件失败。",
        kind: "error"
      });
    }
  }

  async function runAction(label: string, action: () => Promise<string | void>) {
    setActionStatus({ loading: true, message: `${label}...`, kind: "idle" });
    try {
      const resultMessage = await action();
      await loadDetail();
      setActionStatus({
        loading: false,
        message: resultMessage ?? `${label} completed.`,
        kind: "success"
      });
    } catch (error) {
      setActionStatus({
        loading: false,
        message: error instanceof ApiError ? error.message : `${label} failed.`,
        kind: "error"
      });
    }
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    setSelectedFile(event.target.files?.[0] ?? null);
  }

  async function handleUpload() {
    if (!selectedFile) {
      setActionStatus({ loading: false, message: "请选择案件材料文件。", kind: "error" });
      return;
    }
    await runAction("上传材料", async () => {
      await uploadMaterial(caseId, selectedFile);
      setSelectedFile(null);
    });
  }

  async function handleApplySkill(skillId: string) {
    await runAction("应用技能", async () => {
      const binding = await applySkillToCase(caseId, skillId);
      return `已应用技能: ${binding.skill_id} / Package: ${binding.package_id}`;
    });
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <Link href="/cases" className="text-sm font-medium text-accent">
            返回案件
          </Link>
          <div className="mt-3 text-xs uppercase tracking-wide text-gold">案件工作流</div>
          <h1 className="mt-2 text-2xl font-semibold text-ink">
            {detail?.case.title ?? "案件详情"}
          </h1>
          <p className="mt-2 text-sm text-muted">案件 ID: {caseId}</p>
        </div>
        <Link
          href="/reports"
          className="rounded-md border border-line bg-white px-4 py-2 text-sm font-medium text-ink shadow-sm hover:border-accent"
        >
          查看报告
        </Link>
      </header>

      {pageStatus.message ? <StatusMessage status={pageStatus} /> : null}
      {actionStatus.message ? <StatusMessage status={actionStatus} /> : null}

      {detail ? (
        <>
          <WorkflowSection title="案件归属">
            <div className="grid gap-4 md:grid-cols-3">
              <InfoRow label="workspace_id" value={detail.case.workspace_id} />
              <InfoRow label="owner_user_id" value={detail.case.owner_user_id} />
              <InfoRow label="created_at" value={formatDate(detail.case.created_at)} />
            </div>
          </WorkflowSection>

          <WorkflowSection title="案件概览">
            <div className="grid gap-4 md:grid-cols-3">
              <InfoRow label="案件类型" value={detail.case.case_type} />
              <InfoRow label="状态" value={detail.case.status} />
              <InfoRow label="工作空间 ID" value={detail.case.workspace_id} />
              <InfoRow label="所属用户 ID" value={detail.case.owner_user_id} />
              <InfoRow label="创建时间" value={formatDate(detail.case.created_at)} />
              <InfoRow label="更新时间" value={formatDate(detail.case.updated_at)} />
            </div>
          </WorkflowSection>

          <WorkflowSection title="材料">
            <div className="flex flex-wrap items-end gap-3">
              <div className="min-w-64 flex-1">
                <label htmlFor="material" className="text-sm font-medium text-ink">
                  上传材料
                </label>
                <input
                  id="material"
                  type="file"
                  accept=".txt,text/plain"
                  onChange={handleFileChange}
                  className="mt-2 block w-full rounded-md border border-line px-3 py-2 text-sm"
                />
              </div>
              <Button onClick={handleUpload} disabled={actionStatus.loading}>
                上传材料
              </Button>
              <Button
                variant="secondary"
                disabled={actionStatus.loading}
                onClick={() =>
                  runAction("抽取事实", async () => {
                    const result = await extractFacts(caseId);
                    if (result.skill_used && result.package_used) {
                      return `事实抽取使用技能: ${result.skill_used} / Package: ${result.package_used}`;
                    }
                  })
                }
              >
                抽取事实
              </Button>
            </div>
            <ListArea empty="暂无已上传材料。">
              {detail.materials.map((material) => (
                <ListItem
                  key={material.material_id}
                  title={material.filename}
                  meta={`${material.material_id} · ${material.material_type} · ${material.status}`}
                />
              ))}
            </ListArea>
          </WorkflowSection>

          <WorkflowSection title="事实">
            <ListArea empty="暂无已提炼事实。">
              {detail.facts.map((fact) => (
                <ListItem
                  key={fact.fact_id}
                  title={fact.content}
                  meta={`${fact.fact_id} · ${fact.fact_type} · 置信度 ${fact.confidence}`}
                />
              ))}
            </ListArea>
          </WorkflowSection>

          <WorkflowSection title="法律分析">
            <Button
              variant="secondary"
              disabled={actionStatus.loading}
              onClick={() =>
                runAction("运行法律分析", async () => {
                  const result = await runLegalAnalysis(caseId);
                  if (result.skill_used && result.package_used) {
                    return `法律分析使用技能: ${result.skill_used} / Package: ${result.package_used}`;
                  }
                })
              }
            >
              运行法律分析
            </Button>
            <ListArea empty="暂无法律分析记录。">
              {detail.analyses.map((analysis) => (
                <ListItem
                  key={analysis.analysis_id}
                  title={analysis.conclusion}
                  meta={`${analysis.analysis_id} · 风险 ${analysis.risk_level} · 置信度 ${analysis.confidence}`}
                />
              ))}
            </ListArea>
          </WorkflowSection>

          <WorkflowSection title="报告">
            <Button
              variant="secondary"
              disabled={actionStatus.loading}
              onClick={() =>
                runAction("生成报告", async () => {
                  const result = await generateReport(caseId);
                  const skillId = result.source_refs.skill_id;
                  const packageId = result.source_refs.package_id;
                  if (skillId && packageId) {
                    return `报告已生成，使用技能: ${skillId} / Package: ${packageId}`;
                  }
                })
              }
            >
              生成报告
            </Button>
            <ListArea empty="暂无已生成报告。">
              {detail.reports.map((report) => (
                <Link
                  key={report.report_id}
                  href={`/reports/${report.report_id}`}
                  className="block border-b border-line py-3 last:border-b-0 hover:text-accent"
                >
                  <div className="text-sm font-medium text-ink">{report.title}</div>
                  <div className="mt-1 text-xs text-muted">
                    {report.report_id} · 版本 {report.version} · {report.status}
                  </div>
                </Link>
              ))}
            </ListArea>
          </WorkflowSection>

          <WorkflowSection title="技能">
            <div className="grid gap-4 lg:grid-cols-2">
              <div>
                <h3 className="text-sm font-semibold text-ink">可用技能</h3>
                <ListArea empty="暂无已发布技能。">
                  {availableSkills.map((skill) => (
                    <article key={skill.skill_id} className="border-b border-line py-3 last:border-b-0">
                      <div className="flex flex-wrap items-start justify-between gap-3">
                        <div>
                          <div className="text-sm font-medium text-ink">{skill.skill_name}</div>
                          <div className="mt-1 text-xs text-muted">
                            {skill.skill_id} · {skill.domain} · {skill.package_id}
                          </div>
                        </div>
                        <Button
                          variant="secondary"
                          disabled={actionStatus.loading}
                          onClick={() => handleApplySkill(skill.skill_id)}
                          className="text-xs"
                        >
                          应用技能
                        </Button>
                      </div>
                    </article>
                  ))}
                </ListArea>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-ink">已应用技能</h3>
                <ListArea empty="本案件暂未应用技能。">
                  {appliedSkills.map((binding) => (
                    <ListItem
                      key={binding.binding_id ?? `${binding.skill_id}-${binding.package_id}`}
                      title={binding.skill_id}
                      meta={`Package: ${binding.package_id} · 状态: ${binding.status} · 应用时间: ${
                        binding.created_at ? formatDate(binding.created_at) : "n/a"
                      }`}
                    />
                  ))}
                </ListArea>
              </div>
            </div>
          </WorkflowSection>

          <section className="grid gap-4 lg:grid-cols-2">
            <RuntimeTraceSection detail={detail} runtime={runtime} />
            <AuditTrailSection />
          </section>
        </>
      ) : null}
    </div>
  );
}

function WorkflowSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card>
      <CardBody>
        <div className="mb-4 flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">{title}</h2>
          <Badge tone="muted">工作流</Badge>
        </div>
        <div className="space-y-4">{children}</div>
      </CardBody>
    </Card>
  );
}

function AuditTrailSection() {
  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">审计轨迹</h2>
          <Badge tone="muted">audit trail</Badge>
        </div>
        <p className="mt-3 text-sm text-muted">
          暂无运行记录。当前后端暂未返回独立审计日志字段。
        </p>
      </CardBody>
    </Card>
  );
}

function RuntimeTraceSection({
  detail,
  runtime
}: {
  detail: CaseDetail;
  runtime: RuntimeStatus | null;
}) {
  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between gap-3">
          <h2 className="text-sm font-semibold text-ink">运行轨迹</h2>
          <Badge tone="muted">runtime trace</Badge>
        </div>

        <div className="mt-4 space-y-5">
          <section>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">运行状态</h3>
            <div className="mt-3 space-y-3">
              <InfoRow label="模型提供方" value={runtime?.provider ?? "暂无"} />
              <InfoRow label="模型" value={runtime?.model ?? "暂无"} />
              <InfoRow label="已配置" value={formatBoolean(runtime?.configured)} />
              <InfoRow label="Base URL 已配置" value={formatBoolean(runtime?.base_url_configured)} />
            </div>
          </section>

          <section>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">事实抽取记录</h3>
            <TraceList empty="暂无事实抽取记录。可以先上传材料并运行事实抽取。">
              {detail.facts.map((fact) => (
                <TraceItem
                  key={fact.fact_id}
                  title={fact.fact_id}
                  rows={[
                    ["source_material_id", fact.material_id],
                    ["confidence", String(fact.confidence)],
                    ["created_at", formatDate(fact.created_at)],
                    ["source_refs", "暂无"]
                  ]}
                />
              ))}
            </TraceList>
          </section>

          <section>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">法律分析记录</h3>
            <TraceList empty="暂无法律分析记录。可以先运行法律分析。">
              {detail.analyses.map((analysis) => (
                <TraceItem
                  key={analysis.analysis_id}
                  title={analysis.analysis_id}
                  rows={[
                    ["case_id", analysis.case_id],
                    ["analysis_type / status", analysis.status ?? "暂无"],
                    ["llm_provider", analysis.llm_provider ?? "暂无"],
                    ["skill_used", analysis.skill_used ?? "暂无"],
                    ["created_at", formatDate(analysis.created_at)]
                  ]}
                />
              ))}
            </TraceList>
          </section>

          <section>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted">报告记录</h3>
            <TraceList empty="暂无运行记录。">
              {detail.reports.map((report) => (
                <TraceItem
                  key={report.report_id}
                  title={report.report_id}
                  rows={[
                    ["report_type", report.report_type],
                    ["llm_provider", report.llm_provider ?? report.source_refs.llm_provider ?? "暂无"],
                    ["llm_status", report.llm_status ?? report.source_refs.llm_status ?? "暂无"],
                    ["skill_used", report.skill_used ?? report.source_refs.skill_id ?? "暂无"],
                    ["package_used", report.package_used ?? report.source_refs.package_id ?? "暂无"],
                    ["source_refs", formatSourceRefs(report.source_refs)],
                    ["created_at", formatDate(report.created_at)]
                  ]}
                />
              ))}
            </TraceList>
          </section>
        </div>
      </CardBody>
    </Card>
  );
}

function TraceList({ empty, children }: { empty: string; children: React.ReactNode }) {
  const hasChildren = Array.isArray(children) ? children.length > 0 : Boolean(children);
  return <div className="mt-3 space-y-3">{hasChildren ? children : <div className="text-sm text-muted">{empty}</div>}</div>;
}

function TraceItem({
  title,
  rows
}: {
  title: string;
  rows: Array<[string, string]>;
}) {
  return (
    <article className="rounded-md border border-line p-3">
      <div className="text-sm font-medium text-ink">{title}</div>
      <div className="mt-2 space-y-2">
        {rows.map(([label, value]) => (
          <div key={label} className="flex items-start justify-between gap-4 text-xs">
            <span className="text-muted">{label}</span>
            <span className="max-w-[70%] break-words text-right font-medium text-ink">{value || "暂无"}</span>
          </div>
        ))}
      </div>
    </article>
  );
}

function ListArea({ empty, children }: { empty: string; children: React.ReactNode }) {
  const hasChildren = Array.isArray(children) ? children.length > 0 : Boolean(children);
  return (
    <div className="mt-3">
      {hasChildren ? children : <div className="text-sm text-muted">{empty}</div>}
    </div>
  );
}

function ListItem({ title, meta }: { title: string; meta: string }) {
  return (
    <article className="border-b border-line py-3 last:border-b-0">
      <div className="text-sm font-medium text-ink">{title}</div>
      <div className="mt-1 text-xs text-muted">{meta}</div>
    </article>
  );
}

function StatusMessage({ status }: { status: ActionStatus }) {
  const color =
    status.kind === "error"
      ? "border-red-200 bg-red-50 text-red-700"
      : status.kind === "success"
        ? "border-green-200 bg-green-50 text-green-700"
        : "border-line bg-white text-muted";

  return <div className={`rounded-md border px-4 py-3 text-sm shadow-sm ${color}`}>{status.message}</div>;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function formatBoolean(value: boolean | undefined) {
  if (typeof value !== "boolean") {
    return "暂无";
  }
  return value ? "是" : "否";
}

function formatSourceRefs(value: unknown) {
  if (!value) {
    return "暂无引用来源";
  }
  if (typeof value === "string") {
    return value || "暂无引用来源";
  }
  if (Array.isArray(value)) {
    return value.length > 0 ? value.join(", ") : "暂无引用来源";
  }
  if (typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>);
    if (entries.length === 0) {
      return "暂无引用来源";
    }
    return entries
      .map(([key, entryValue]) => `${key}: ${Array.isArray(entryValue) ? entryValue.join(", ") : String(entryValue ?? "暂无")}`)
      .join(" / ");
  }
  return String(value);
}
