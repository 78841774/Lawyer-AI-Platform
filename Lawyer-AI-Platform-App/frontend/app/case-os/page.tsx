"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaCaseOSCaseListItem,
  PersonalAlphaCaseOSStatus,
  getPersonalAlphaCaseOSStatus,
  listPersonalAlphaCaseOSCases
} from "@/services/api";

export default function PersonalAlphaCaseOSPage() {
  const [status, setStatus] = useState<PersonalAlphaCaseOSStatus | null>(null);
  const [cases, setCases] = useState<PersonalAlphaCaseOSCaseListItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadCaseOS() {
    setLoading(true);
    setError("");
    try {
      const [nextStatus, nextCases] = await Promise.all([
        getPersonalAlphaCaseOSStatus(),
        listPersonalAlphaCaseOSCases()
      ]);
      setStatus(nextStatus);
      setCases(nextCases);
    } catch {
      setError("Personal Alpha Case OS API 暂不可用，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadCaseOS();
  }, []);

  const openCases = cases.filter((caseItem) => !caseItem.latest_lock_id).length;
  const lockedCases = cases.filter((caseItem) => Boolean(caseItem.latest_lock_id)).length;
  const blockedCases = cases.filter((caseItem) => caseItem.blocked).length;

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Case OS"
          description="个人 Alpha 案件操作系统：集中查看本地 controlled mock workflow 的案件状态、阶段健康度、下一步动作、审计时间线与安全边界。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div>
                <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
                <p className="mt-1 text-sm text-muted">
                  local-only / mock-first / controlled-first / metadata-only / redacted-only / advisory-only。
                </p>
              </div>
              <Button type="button" onClick={() => void loadCaseOS()} disabled={loading}>
                {loading ? "刷新中..." : "Refresh"}
              </Button>
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_case_os"} />
              <InfoRow label="case_os_enabled" value={String(status?.case_os_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="manual_review_required" value={String(status?.manual_review_required ?? true)} />
              <InfoRow label="lawyer_review_required" value={String(status?.lawyer_review_required ?? true)} />
              <InfoRow label="raw_content_included" value="false" />
              <InfoRow label="final_report_generation_enabled" value={String(status?.final_report_generation_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-4">
          <SummaryTile label="total cases" value={cases.length} />
          <SummaryTile label="open cases" value={openCases} />
          <SummaryTile label="locked cases" value={lockedCases} />
          <SummaryTile label="blocked cases" value={blockedCases} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Case List</h2>
            <div className="mt-4 grid gap-3">
              {cases.length ? (
                cases.map((caseItem) => (
                  <div
                    key={caseItem.case_id}
                    className="rounded-md border border-line bg-white p-4"
                  >
                    <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                      <div>
                        <div className="text-sm font-semibold text-ink">{caseItem.title}</div>
                        <div className="mt-1 text-xs text-muted">{caseItem.case_id}</div>
                      </div>
                      <div className="grid gap-2 text-xs text-muted md:grid-cols-4">
                        <span>status: {caseItem.latest_lock_id ? "locked" : "open"}</span>
                        <span>current_stage: {caseItem.current_stage}</span>
                        <span>next_action: {caseItem.next_action}</span>
                        <span>blocked: {String(caseItem.blocked)}</span>
                      </div>
                    </div>
                    {caseItem.blocked_reasons.length ? (
                      <div className="mt-3 rounded-md border border-rose-200 bg-rose-50 p-3 text-xs text-rose-800">
                        {caseItem.blocked_reasons.join(" / ")}
                      </div>
                    ) : null}
                    <div className="mt-3 grid gap-2 md:grid-cols-4">
                      <MiniMetric label="workspace run" value={caseItem.latest_workspace_run_id ? 1 : 0} />
                      <MiniMetric label="packet" value={caseItem.latest_packet_id ? 1 : 0} />
                      <MiniMetric label="lock" value={caseItem.latest_lock_id ? 1 : 0} />
                      <MiniMetric label="blocked" value={caseItem.blocked ? 1 : 0} />
                    </div>
                    <div className="mt-4 flex flex-wrap gap-2">
                      <Link href={`/case-os/${encodeURIComponent(caseItem.case_id)}`}>
                        <Button type="button">View Case OS</Button>
                      </Link>
                      <Link href={`/case-os/${encodeURIComponent(caseItem.case_id)}#next-action`}>
                        <Button type="button" variant="secondary">View Next Action</Button>
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <div className="rounded-md border border-dashed border-line p-5 text-sm text-muted">
                  尚未发现 Personal Alpha workspace metadata。Case OS 将保持 mock/redacted demo 状态，不读取真实材料。
                </div>
              )}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Status JSON</h2>
            <pre className="mt-4 max-h-80 overflow-auto rounded-md bg-slate-950 p-4 text-xs leading-5 text-slate-100">
              {JSON.stringify({ status, cases }, null, 2)}
            </pre>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

function SummaryTile({ label, value }: { label: string; value: number }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
        <div className="mt-2 text-2xl font-semibold text-ink">{value}</div>
      </CardBody>
    </Card>
  );
}

function MiniMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-md border border-line bg-paper px-3 py-2">
      <div className="text-[11px] uppercase tracking-wide text-muted">{label}</div>
      <div className="mt-1 text-sm font-semibold text-ink">{value}</div>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{message}</div>;
}
