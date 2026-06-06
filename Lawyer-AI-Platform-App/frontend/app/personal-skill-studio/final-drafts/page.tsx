"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  SafeErrorNotice,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalSkillFinalDraftOwnerDownload,
  getPersonalSkillFinalDraftAudit,
  getPersonalSkillFinalDraftBaseline,
  getPersonalSkillFinalDraftGate,
  getPersonalSkillFinalDraftOptimization,
  getPersonalSkillFinalDraftQuality,
  getPersonalSkillFinalDraftSafety,
  getPersonalSkillFinalDraftSourceTraces,
  listPersonalSkillFinalDraftOwnerDownloads,
  listPersonalSkillFinalDrafts
} from "@/services/api";
import type { SkillStudioFinalDraft } from "@/types";

const skillIds = ["case_fact_extraction_skill", "case_legal_analysis_skill"];
const formats = ["Markdown", "JSON", "PDF draft metadata", "DOCX draft metadata"];

export default function SkillFinalDraftWorkbenchPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [selectedSkillId, setSelectedSkillId] = useState(skillIds[0]);
  const [downloadFormat, setDownloadFormat] = useState(formats[0]);
  const [error, setError] = useState("");

  const selectedDraft = useMemo(
    () => (data.finalDrafts?.final_drafts ?? []).find((draft: SkillStudioFinalDraft) => draft.skill_id === selectedSkillId),
    [data.finalDrafts, selectedSkillId]
  );

  async function loadWorkbench(skillId = selectedSkillId) {
    setError("");
    try {
      const [finalDrafts, baseline, quality, gate, optimization, traces, audit, downloads, safety] = await Promise.all([
        listPersonalSkillFinalDrafts(),
        getPersonalSkillFinalDraftBaseline(skillId),
        getPersonalSkillFinalDraftQuality(skillId),
        getPersonalSkillFinalDraftGate(skillId),
        getPersonalSkillFinalDraftOptimization(skillId),
        getPersonalSkillFinalDraftSourceTraces(skillId),
        getPersonalSkillFinalDraftAudit(skillId),
        listPersonalSkillFinalDraftOwnerDownloads(),
        getPersonalSkillFinalDraftSafety()
      ]);
      setData({ finalDrafts, baseline, quality, gate, optimization, traces, audit, downloads, safety });
    } catch {
      setError("两个 Skill 最终稿工作台 API 暂不可用，请确认后端服务已启动。");
    }
  }

  useEffect(() => {
    void loadWorkbench(selectedSkillId);
  }, [selectedSkillId]);

  async function createDownload(skillId: string) {
    await createPersonalSkillFinalDraftOwnerDownload(skillId, {
      requested_format: downloadFormat,
      explicit_owner_confirmation: true,
      explicit_no_public_link_confirmation: true,
      explicit_no_email_confirmation: true,
      explicit_no_external_delivery_confirmation: true,
      explicit_no_auto_publish_confirmation: true
    });
    await loadWorkbench(skillId);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}
        <section className="rounded-md border border-slate-800 bg-[#1f261f] p-8 text-white">
          <div className="text-xs font-semibold uppercase tracking-wide text-emerald-200">v7.22 Skill Final Draft & Optimization Workbench</div>
          <h1 className="mt-3 text-4xl font-semibold">两个 Skill 最终稿与优化工作台</h1>
          <p className="mt-4 max-w-4xl text-sm leading-7 text-slate-300">
            基于既有 Skill 和配套材料生成最终稿 metadata，不重新发明评价体系；仅用户本人下载，不自动发布 Skill，不自动训练未结案件。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["用户本人", "仅元数据", "草稿状态", "不自动发布 Skill", "不训练未结案件", "Gate 仅作参考"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <StatusCard label="Final Drafts" value={data.finalDrafts?.draft_count ?? 0} detail="两个 Skill metadata" tone="info" />
          <StatusCard label="Baseline" value={String(data.finalDrafts?.baseline_complete ?? false)} detail="不完整时返回缺失项" tone="warning" />
          <StatusCard label="Quality" value={data.quality?.quality_score ?? "--"} detail="参考评分，不保证结果" tone="safe" />
          <StatusCard label="Downloads" value={data.downloads?.download_count ?? 0} detail="仅 owner-only metadata" tone="info" />
        </section>

        <Panel title="Baseline Discovery / 基线发现">
          <div className="grid gap-4 lg:grid-cols-3">
            <Info title="已发现 Skill 文件" items={data.baseline?.source_skill_files ?? []} />
            <Info title="Evaluation / Gate / Test Case" items={[...(data.baseline?.source_evaluation_files ?? []), ...(data.baseline?.source_gate_files ?? []), ...(data.baseline?.source_test_case_files ?? [])]} />
            <Info title="缺失项" items={data.baseline?.missing_baseline_items ?? ["无"]} />
          </div>
          <p className="mt-4 rounded-md bg-amber-50 px-4 py-3 text-sm text-amber-900">
            若历史材料不完整，系统仅显示 placeholder lineage 与 missing_baseline_report，不伪造完整 Skill 基线。
          </p>
        </Panel>

        <Panel title="v7.30 训练产物加载器关联">
          <div className="grid gap-4 md:grid-cols-3">
            <Info title="关联内容" items={["Codex 训练方案 metadata", "多层级案由 taxonomy", "Experience Package manifest", "Skill Context dry-run"]} />
            <Info title="边界" items={["不执行模型微调", "不训练未结案件", "不自动发布 Skill", "不生成最终法律意见"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/training-artifacts">
              打开训练产物加载器
            </a>
          </div>
        </Panel>

        <section className="grid gap-6 xl:grid-cols-2">
          {(data.finalDrafts?.final_drafts ?? []).map((draft: SkillStudioFinalDraft) => (
            <Panel key={draft.skill_id} title={draft.skill_name}>
              <button
                type="button"
                className="mb-4 rounded-md border border-line px-3 py-2 text-sm font-semibold text-ink"
                onClick={() => setSelectedSkillId(draft.skill_id)}
              >
                查看最终稿
              </button>
              <div className="grid gap-3 text-sm text-muted">
                <Row label="skill_id" value={draft.skill_id} />
                <Row label="skill_type" value={draft.skill_type} />
                <Row label="source_skill_id" value={draft.source_skill_id} />
                <Row label="quality_score" value={String(draft.quality_score)} />
                <Row label="gate_status" value={draft.gate_status} />
                <Row label="baseline_complete" value={String(draft.baseline_complete)} />
              </div>
              <div className="mt-4 grid gap-2 text-sm">
                {(draft.optimization_suggestions ?? []).map((item) => (
                  <div key={item} className="rounded-md bg-slate-50 px-3 py-2 text-muted">{item}</div>
                ))}
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                <select className="rounded-md border border-line px-3 py-2 text-sm" value={downloadFormat} onChange={(event) => setDownloadFormat(event.target.value)}>
                  {formats.map((format) => <option key={format}>{format}</option>)}
                </select>
                <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createDownload(draft.skill_id)}>
                  生成 owner-only 下载 metadata
                </button>
              </div>
            </Panel>
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Evaluation / Gate">
            <div className="grid gap-2 text-sm text-muted">
              <Row label="selected_skill" value={selectedSkillId} />
              <Row label="quality_score" value={String(data.quality?.quality_score ?? "--")} />
              <Row label="score_status" value={String(data.quality?.score_status ?? "reference_only")} />
              <Row label="gate_status" value={String(data.gate?.gate_status ?? "reference_only")} />
              <Row label="blocks_next_stage" value={String(data.gate?.blocks_next_stage ?? false)} />
            </div>
            <p className="mt-4 rounded-md bg-emerald-50 px-4 py-3 text-sm text-emerald-900">
              门控仅作为质量评分与优化方向，不阻断下一步。
            </p>
          </Panel>
          <Panel title="Optimization Suggestions">
            <div className="grid gap-2">
              {(data.optimization?.optimization_suggestions ?? []).map((item: string) => <div key={item} className="rounded-md bg-white px-3 py-2 text-sm text-muted">{item}</div>)}
            </div>
          </Panel>
          <Panel title="Owner Download Boundary">
            <div className="grid gap-2 text-sm text-muted">
              {["仅用户本人下载", "不创建公开链接", "不发送邮件", "不自动对外交付", "不自动发布 Skill", "不生成最终法律意见"].map((item) => <span key={item}>✓ {item}</span>)}
            </div>
          </Panel>
        </section>

        <Panel title="Source Trace / Audit">
          <div className="grid gap-4 lg:grid-cols-2">
            <Info title="Source Trace" items={(data.traces?.source_traces ?? []).map((trace: any) => trace.source_trace_id)} />
            <Info title="Audit" items={(data.audit?.events ?? []).map((event: any) => `${event.action}:${event.object_type}`)} />
          </div>
        </Panel>

        <TrustSafetyPanel items={data.safety?.safety_checklist ?? []} title="信任与安全面板" />
        <DiagnosticsPanel data={{ selectedDraft, ...data }} />
      </div>
    </AppShell>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="rounded-md border border-line bg-paper p-5"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>;
}

function Info({ title, items }: { title: string; items: string[] }) {
  const display = items.length ? items.slice(0, 8) : ["暂无 metadata"];
  return <div className="rounded-md border border-line bg-white p-4"><div className="text-sm font-semibold text-ink">{title}</div><div className="mt-3 grid gap-2 text-xs text-muted">{display.map((item) => <span key={item}>{item}</span>)}</div></div>;
}

function Row({ label, value }: { label: string; value: string }) {
  return <div className="flex items-center justify-between gap-4 rounded-md bg-white px-3 py-2"><span>{label}</span><span className="font-mono text-xs text-ink">{value}</span></div>;
}
