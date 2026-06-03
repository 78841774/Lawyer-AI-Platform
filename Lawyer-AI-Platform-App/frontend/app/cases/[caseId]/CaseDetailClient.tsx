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
  getCaseSkills,
  getCaseDetail,
  getWorkspaceSkills,
  runLegalAnalysis,
  uploadMaterial,
  WorkspaceSkillRecord
} from "@/services/api";

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
    message: "Loading case..."
  });
  const [actionStatus, setActionStatus] = useState<ActionStatus>(initialActionStatus);
  const [availableSkills, setAvailableSkills] = useState<WorkspaceSkillRecord[]>([]);
  const [appliedSkills, setAppliedSkills] = useState<CaseSkillBinding[]>([]);

  useEffect(() => {
    void loadDetail();
  }, [caseId]);

  async function loadDetail() {
    setPageStatus({ loading: true, message: "Loading case...", kind: "idle" });
    try {
      const [nextDetail, nextAvailableSkills, nextAppliedSkills] = await Promise.all([
        getCaseDetail(caseId),
        getWorkspaceSkills(),
        getCaseSkills(caseId)
      ]);
      setDetail(nextDetail);
      setAvailableSkills(nextAvailableSkills);
      setAppliedSkills(nextAppliedSkills);
      setPageStatus(initialActionStatus);
    } catch (error) {
      setPageStatus({
        loading: false,
        message: error instanceof ApiError ? error.message : "Failed to load case.",
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
      setActionStatus({ loading: false, message: "Please select a material file.", kind: "error" });
      return;
    }
    await runAction("Upload Material", async () => {
      await uploadMaterial(caseId, selectedFile);
      setSelectedFile(null);
    });
  }

  async function handleApplySkill(skillId: string) {
    await runAction("Apply Skill", async () => {
      const binding = await applySkillToCase(caseId, skillId);
      return `Applied Skill: ${binding.skill_id} / Package: ${binding.package_id}`;
    });
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <Link href="/cases" className="text-sm text-accent">
            Back to cases
          </Link>
          <h1 className="mt-3 text-2xl font-semibold text-ink">
            {detail?.case.title ?? "Case Detail"}
          </h1>
          <p className="mt-2 text-sm text-slate-600">Case ID: {caseId}</p>
        </div>
        <Link
          href="/reports"
          className="rounded-md border border-line bg-white px-4 py-2 text-sm font-medium text-ink hover:border-accent"
        >
          View Reports
        </Link>
      </header>

      {pageStatus.message ? <StatusMessage status={pageStatus} /> : null}
      {actionStatus.message ? <StatusMessage status={actionStatus} /> : null}

      {detail ? (
        <>
          <section className="grid gap-4 md:grid-cols-4">
            <MetaCard label="Case Type" value={detail.case.case_type} />
            <MetaCard label="Status" value={detail.case.status} />
            <MetaCard label="Created" value={formatDate(detail.case.created_at)} />
            <MetaCard label="Updated" value={formatDate(detail.case.updated_at)} />
          </section>

          <section className="rounded-md border border-line bg-white p-5">
            <div className="flex flex-wrap items-end gap-3">
              <div className="min-w-64 flex-1">
                <label htmlFor="material" className="text-sm font-medium text-ink">
                  Upload Material
                </label>
                <input
                  id="material"
                  type="file"
                  accept=".txt,text/plain"
                  onChange={handleFileChange}
                  className="mt-2 block w-full rounded-md border border-line px-3 py-2 text-sm"
                />
              </div>
              <button
                type="button"
                onClick={handleUpload}
                disabled={actionStatus.loading}
                className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
              >
                Upload Material
              </button>
              <ActionButton
                label="Extract Facts"
                loading={actionStatus.loading}
                onClick={() =>
                  runAction("Extract Facts", async () => {
                    const result = await extractFacts(caseId);
                    if (result.skill_used && result.package_used) {
                      return `Fact Runtime used Skill: ${result.skill_used} / Package: ${result.package_used}`;
                    }
                  })
                }
              />
              <ActionButton
                label="Run Legal Analysis"
                loading={actionStatus.loading}
                onClick={() =>
                  runAction("Run Legal Analysis", async () => {
                    const result = await runLegalAnalysis(caseId);
                    if (result.skill_used && result.package_used) {
                      return `Legal Analysis used Skill: ${result.skill_used} / Package: ${result.package_used}`;
                    }
                  })
                }
              />
              <ActionButton
                label="Generate Report"
                loading={actionStatus.loading}
                onClick={() =>
                  runAction("Generate Report", async () => {
                    const result = await generateReport(caseId);
                    const skillId = result.source_refs.skill_id;
                    const packageId = result.source_refs.package_id;
                    if (skillId && packageId) {
                      return `Report generated with Skill: ${skillId} / Package: ${packageId}`;
                    }
                  })
                }
              />
            </div>
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <DataPanel title="Available Skills" empty="No published skills available.">
              {availableSkills.map((skill) => (
                <article key={skill.skill_id} className="border-b border-line py-3 last:border-b-0">
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-medium text-ink">{skill.skill_name}</div>
                      <div className="mt-1 text-xs text-slate-500">
                        {skill.skill_id} · {skill.domain} · {skill.package_id}
                      </div>
                    </div>
                    <button
                      type="button"
                      disabled={actionStatus.loading}
                      onClick={() => handleApplySkill(skill.skill_id)}
                      className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink hover:border-accent disabled:opacity-60"
                    >
                      Apply Skill
                    </button>
                  </div>
                </article>
              ))}
            </DataPanel>

            <DataPanel title="Applied Skills" empty="No skills applied to this case.">
              {appliedSkills.map((binding) => (
                <ListItem
                  key={binding.binding_id ?? `${binding.skill_id}-${binding.package_id}`}
                  title={binding.skill_id}
                  meta={`Package: ${binding.package_id} · Status: ${binding.status} · Applied: ${
                    binding.created_at ? formatDate(binding.created_at) : "n/a"
                  }`}
                />
              ))}
            </DataPanel>
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <DataPanel title="Materials" empty="No materials uploaded.">
              {detail.materials.map((material) => (
                <ListItem
                  key={material.material_id}
                  title={material.filename}
                  meta={`${material.material_id} · ${material.material_type} · ${material.status}`}
                />
              ))}
            </DataPanel>

            <DataPanel title="Facts" empty="No facts extracted.">
              {detail.facts.map((fact) => (
                <ListItem
                  key={fact.fact_id}
                  title={fact.content}
                  meta={`${fact.fact_id} · ${fact.fact_type} · confidence ${fact.confidence}`}
                />
              ))}
            </DataPanel>

            <DataPanel title="Legal Analysis" empty="No legal analysis runs.">
              {detail.analyses.map((analysis) => (
                <ListItem
                  key={analysis.analysis_id}
                  title={analysis.conclusion}
                  meta={`${analysis.analysis_id} · risk ${analysis.risk_level} · confidence ${analysis.confidence}`}
                />
              ))}
            </DataPanel>

            <DataPanel title="Reports" empty="No reports generated.">
              {detail.reports.map((report) => (
                <Link
                  key={report.report_id}
                  href={`/reports/${report.report_id}`}
                  className="block border-b border-line py-3 last:border-b-0 hover:text-accent"
                >
                  <div className="text-sm font-medium text-ink">{report.title}</div>
                  <div className="mt-1 text-xs text-slate-500">
                    {report.report_id} · version {report.version} · {report.status}
                  </div>
                </Link>
              ))}
            </DataPanel>
          </section>
        </>
      ) : null}
    </div>
  );
}

function ActionButton({
  label,
  loading,
  onClick
}: {
  label: string;
  loading: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={loading}
      className="rounded-md border border-line bg-white px-4 py-2 text-sm font-medium text-ink hover:border-accent disabled:opacity-60"
    >
      {label}
    </button>
  );
}

function MetaCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-ink">{value}</div>
    </div>
  );
}

function DataPanel({
  title,
  empty,
  children
}: {
  title: string;
  empty: string;
  children: React.ReactNode;
}) {
  const hasChildren = Array.isArray(children) ? children.length > 0 : Boolean(children);
  return (
    <section className="rounded-md border border-line bg-white p-5">
      <h2 className="text-sm font-semibold text-ink">{title}</h2>
      <div className="mt-3">
        {hasChildren ? children : <div className="text-sm text-slate-600">{empty}</div>}
      </div>
    </section>
  );
}

function ListItem({ title, meta }: { title: string; meta: string }) {
  return (
    <article className="border-b border-line py-3 last:border-b-0">
      <div className="text-sm font-medium text-ink">{title}</div>
      <div className="mt-1 text-xs text-slate-500">{meta}</div>
    </article>
  );
}

function StatusMessage({ status }: { status: ActionStatus }) {
  const color =
    status.kind === "error"
      ? "border-red-200 bg-red-50 text-red-700"
      : status.kind === "success"
        ? "border-green-200 bg-green-50 text-green-700"
        : "border-line bg-white text-slate-600";

  return <div className={`rounded-md border px-4 py-3 text-sm ${color}`}>{status.message}</div>;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
