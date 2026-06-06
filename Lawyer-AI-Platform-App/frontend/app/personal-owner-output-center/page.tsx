"use client";

import { useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  InfoRows,
  Panel,
  RuntimeCard,
  SafeErrorNotice,
  StatusCard,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalOwnerOutputCenterDownload,
  getPersonalOwnerOutputCenterAudit,
  getPersonalOwnerOutputCenterOutput,
  getPersonalOwnerOutputCenterOutputGate,
  getPersonalOwnerOutputCenterOutputOptimization,
  getPersonalOwnerOutputCenterOutputQuality,
  getPersonalOwnerOutputCenterOutputSourceTraces,
  getPersonalOwnerOutputCenterSafety,
  getPersonalOwnerOutputCenterStatus,
  listPersonalOwnerOutputCenterDownloads,
  listPersonalOwnerOutputCenterOutputs
} from "@/services/api";
import type { OwnerOutputRecord } from "@/types";

const downloadFormats = [
  ["markdown", "仅用户本人下载 Markdown"],
  ["json", "仅用户本人下载 JSON"],
  ["pdf_draft_metadata", "仅用户本人下载 PDF Draft Metadata"],
  ["docx_draft_metadata", "仅用户本人下载 DOCX Draft Metadata"]
];

export default function PersonalOwnerOutputCenterPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [selectedOutputId, setSelectedOutputId] = useState("");
  const [downloadFormat, setDownloadFormat] = useState(downloadFormats[0][0]);
  const [error, setError] = useState("");

  const outputs = (data.outputs?.outputs ?? []) as OwnerOutputRecord[];
  const selectedOutput = useMemo(
    () => outputs.find((output) => output.output_id === selectedOutputId) ?? outputs[0],
    [outputs, selectedOutputId]
  );

  async function loadCenter(nextOutputId = selectedOutputId) {
    setError("");
    try {
      const [status, outputsResponse, downloads, audit, safety] = await Promise.all([
        getPersonalOwnerOutputCenterStatus(),
        listPersonalOwnerOutputCenterOutputs(),
        listPersonalOwnerOutputCenterDownloads(),
        getPersonalOwnerOutputCenterAudit(),
        getPersonalOwnerOutputCenterSafety()
      ]);
      const firstOutputId = nextOutputId || outputsResponse.outputs?.[0]?.output_id || "";
      const [detail, quality, gate, optimization, sourceTraces] = firstOutputId
        ? await Promise.all([
            getPersonalOwnerOutputCenterOutput(firstOutputId),
            getPersonalOwnerOutputCenterOutputQuality(firstOutputId),
            getPersonalOwnerOutputCenterOutputGate(firstOutputId),
            getPersonalOwnerOutputCenterOutputOptimization(firstOutputId),
            getPersonalOwnerOutputCenterOutputSourceTraces(firstOutputId)
          ])
        : [null, null, null, null, null];
      setSelectedOutputId(firstOutputId);
      setData({ status, outputs: outputsResponse, detail, quality, gate, optimization, sourceTraces, downloads, audit, safety });
    } catch {
      setError("用户本人产出下载中心 API 暂不可用。页面保持安全 fallback，不调用真实 provider，不读取真实案件材料，不展示原始内容。");
    }
  }

  useEffect(() => {
    void loadCenter();
  }, []);

  async function selectOutput(outputId: string) {
    setSelectedOutputId(outputId);
    await loadCenter(outputId);
  }

  async function createDownload() {
    if (!selectedOutput?.output_id) return;
    await createPersonalOwnerOutputCenterDownload(selectedOutput.output_id, {
      owner_user_id: "local_owner",
      requested_format: downloadFormat,
      explicit_owner_confirmation: true,
      explicit_no_public_link_confirmation: true,
      explicit_no_email_confirmation: true,
      explicit_no_external_delivery_confirmation: true
    });
    await loadCenter(selectedOutput.output_id);
  }

  const dimensionScores = Object.entries(data.quality?.dimension_scores ?? selectedOutput?.dimension_scores ?? {});
  const formatOptions = selectedOutput?.format_options ?? {};

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}

        <section className="rounded-md border border-slate-800 bg-[#14202a] p-8 text-white shadow-sm">
          <div className="text-sm font-medium text-cyan-200">v7.23 Owner-only Output Center</div>
          <h1 className="mt-3 text-4xl font-semibold">用户本人产出下载中心</h1>
          <p className="mt-4 max-w-4xl text-sm leading-6 text-slate-300">
            集中管理个人版产出材料，仅用户本人查看和下载；不自动外发，不创建公开链接，不自动标记最终法律意见。
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {["集中管理个人版产出材料", "仅用户本人查看和下载", "不自动外发", "不创建公开链接", "不自动标记最终法律意见"].map((badge) => (
              <DarkSafetyBadge key={badge} label={badge} />
            ))}
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          <StatusCard label="Skill 最终稿" value={data.outputs?.skill_final_draft_count ?? 0} detail="两个核心 Skill metadata" tone="info" />
          <StatusCard label="事实产出" value={data.outputs?.fact_output_count ?? 0} detail="预览 / 纠正 / 来源 / 质量" tone="safe" />
          <StatusCard label="法律分析草稿" value={data.outputs?.legal_draft_count ?? 0} detail="争议 / 请求权 / 抗辩 / 风险" tone="info" />
          <StatusCard label="Pilot / Delivery" value={data.outputs?.pilot_delivery_count ?? 0} detail="Pilot 摘要与交付草稿" tone="warning" />
          <StatusCard label="Owner Download" value={String(data.status?.owner_only_download_ready ?? true)} detail="仅用户本人下载" tone="safe" />
          <StatusCard label="External Delivery" value="disabled" detail="public_link=false / email=false" tone="safe" />
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.95fr_1.05fr]">
          <Panel title="Output List" eyebrow="产出清单">
            <div className="grid gap-3">
              {outputs.map((output) => (
                <button
                  key={output.output_id}
                  type="button"
                  className={`rounded-md border px-4 py-3 text-left transition ${selectedOutput?.output_id === output.output_id ? "border-cyan-400 bg-cyan-50" : "border-line bg-white hover:bg-slate-50"}`}
                  onClick={() => void selectOutput(output.output_id)}
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <div className="text-sm font-semibold text-ink">{output.output_title}</div>
                      <div className="mt-1 text-xs text-muted">{output.output_type} / {output.source_runtime}</div>
                    </div>
                    <div className="rounded-md bg-slate-900 px-2 py-1 text-xs font-semibold text-white">{output.quality_score}</div>
                  </div>
                  <div className="mt-3 grid gap-2 text-xs text-muted md:grid-cols-3">
                    <span>gate: {output.gate_status}</span>
                    <span>source trace: {output.source_trace_count}</span>
                    <span>review: {output.review_status}</span>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2 text-xs">
                    {Object.entries(output.format_options).filter(([, available]) => available).map(([format]) => (
                      <span key={format} className="rounded-md border border-line bg-slate-50 px-2 py-1 text-muted">{format}</span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </Panel>

          <Panel title="Output Detail Panel" eyebrow="产出详情">
            <div className="grid gap-4">
              <InfoRows
                rows={[
                  ["output_id", selectedOutput?.output_id],
                  ["output_type", selectedOutput?.output_type],
                  ["source_runtime", selectedOutput?.source_runtime],
                  ["source_module", selectedOutput?.source_module],
                  ["source_id", selectedOutput?.source_id],
                  ["case_id", selectedOutput?.case_id ?? "not_required"],
                  ["skill_id", selectedOutput?.skill_id ?? "not_required"],
                  ["review_status", selectedOutput?.review_status],
                  ["owner_only", selectedOutput?.owner_only ?? true],
                  ["downloadable_by_owner_only", selectedOutput?.downloadable_by_owner_only ?? true]
                ]}
              />
              <div className="grid gap-3 md:grid-cols-2">
                <RuntimeCard
                  title="Quality / Gate"
                  category="reference-only"
                  status={String(data.gate?.gate_status ?? selectedOutput?.gate_status ?? "reference_only")}
                  items={[
                    ["quality_score", data.quality?.quality_score ?? selectedOutput?.quality_score],
                    ["gate_score", data.gate?.gate_score ?? "pending"],
                    ["gate_reference_only", data.gate?.gate_reference_only ?? true],
                    ["blocks_next_stage", data.gate?.blocks_next_stage ?? false],
                    ["quality_reference_only", data.quality?.quality_reference_only ?? true]
                  ]}
                />
                <RuntimeCard
                  title="Owner-only Boundary"
                  category="download metadata"
                  status="external delivery disabled"
                  items={[
                    ["public_link_created", selectedOutput?.public_link_created ?? false],
                    ["email_sent", selectedOutput?.email_sent ?? false],
                    ["external_delivery_triggered", selectedOutput?.external_delivery_triggered ?? false],
                    ["final_legal_opinion_auto_generated", selectedOutput?.final_legal_opinion_auto_generated ?? false],
                    ["final_report_auto_generated", selectedOutput?.final_report_auto_generated ?? false]
                  ]}
                />
              </div>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Download Panel" eyebrow="仅用户本人下载">
            <div className="grid gap-3">
              <select className="rounded-md border border-line px-3 py-2 text-sm" value={downloadFormat} onChange={(event) => setDownloadFormat(event.target.value)}>
                {downloadFormats.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
              </select>
              <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={() => void createDownload()}>
                {downloadFormats.find(([value]) => value === downloadFormat)?.[1] ?? "仅用户本人下载"}
              </button>
              <div className="grid gap-2 text-xs text-muted">
                <span>markdown_available: {String(formatOptions.markdown_available ?? true)}</span>
                <span>json_available: {String(formatOptions.json_available ?? true)}</span>
                <span>pdf_draft_metadata_available: {String(formatOptions.pdf_draft_metadata_available ?? true)}</span>
                <span>docx_draft_metadata_available: {String(formatOptions.docx_draft_metadata_available ?? true)}</span>
              </div>
            </div>
          </Panel>

          <Panel title="Quality / Gate / Optimization Panel">
            <div className="grid gap-2">
              {dimensionScores.map(([label, value]) => (
                <div key={label} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-sm">
                  <div className="flex items-center justify-between gap-3">
                    <span>{label}</span>
                    <span className="font-semibold text-cyan-800">{String(value)}</span>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-xs leading-5 text-cyan-900">
              门控仅作为质量参考，不阻断下载或下一步。
            </div>
          </Panel>

          <Panel title="Optimization Suggestions">
            <div className="grid gap-2">
              {(data.optimization?.optimization_suggestions ?? selectedOutput?.optimization_suggestions ?? []).map((item: string) => (
                <div key={item} className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-xs leading-5 text-amber-900">{item}</div>
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Source Trace">
            <div className="grid gap-2">
              {(data.sourceTraces?.source_traces ?? []).map((trace: Record<string, any>) => (
                <div key={String(trace.source_trace_id)} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-xs text-muted">
                  <div className="font-semibold text-ink">{String(trace.source_trace_id)}</div>
                  <div className="mt-1">{String(trace.source_label)}</div>
                </div>
              ))}
            </div>
          </Panel>
          <Panel title="Audit Metadata">
            <InfoRows rows={[["event_count", data.audit?.event_count ?? 0], ["download_count", data.downloads?.download_count ?? 0], ["audit_required", data.audit?.audit_required ?? true]]} />
          </Panel>
          <Panel title="Recent Downloads">
            <div className="grid gap-2">
              {(data.downloads?.owner_downloads ?? []).slice(0, 6).map((download: Record<string, any>) => (
                <div key={String(download.download_id)} className="rounded-md border border-line bg-slate-50 px-3 py-2 text-xs text-muted">
                  <div className="font-semibold text-ink">{String(download.requested_format)}</div>
                  <div className="mt-1">{String(download.download_status)}</div>
                </div>
              ))}
              {(data.downloads?.owner_downloads ?? []).length === 0 ? <div className="text-sm text-muted">暂无下载 metadata</div> : null}
            </div>
          </Panel>
        </section>

        <TrustSafetyPanel
          items={data.safety?.safety_checklist ?? []}
          title="信任与安全面板"
          note="产出中心仅展示用户本人草稿元数据，不展示原始内容、本地路径或密钥值。"
        />
        <DiagnosticsPanel data={{ selectedOutput, ...data }} />
      </div>
    </AppShell>
  );
}
