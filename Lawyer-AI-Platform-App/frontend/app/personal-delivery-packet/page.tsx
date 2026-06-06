"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  SafeErrorNotice,
  ShowcaseStepper,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  DeliveryPacketList,
  DeliveryPacketRecord,
  DeliveryPacketRuntimeList,
  DeliveryPacketSafetyStatus,
  ExportReadiness,
  FinalLockList,
  PacketItemList,
  PersonalDeliveryPacketStatus,
  ReviewSummary,
  SourceBundleList,
  personalDeliveryPacketApi
} from "@/services/api";

const stepper = [
  { label: "交付包草案", detail: "仅元数据" },
  { label: "交付项清单", detail: "draft item" },
  { label: "来源追踪", detail: "Source Trace" },
  { label: "律师复核", detail: "review required" },
  { label: "最终锁定", detail: "no real export" }
];

const safetyChecks = [
  "未读取案件正文",
  "未读取真实案件材料",
  "未调用真实 provider",
  "不展示密钥值",
  "未生成最终法律意见",
  "未生成最终报告",
  "未自动对外交付",
  "未发送邮件",
  "未生成真实 PDF/DOCX",
  "律师复核必需",
  "最终锁定必需",
  "来源追踪必需",
  "仅返回交付包 metadata"
];

const itemTypes = [
  "case_metadata_summary",
  "material_processing_summary",
  "ai_draft_summary",
  "intelligence_summary",
  "skill_studio_summary",
  "lawyer_review_summary",
  "source_trace_summary",
  "export_placeholder"
];

const lockActions = [
  { action: "lock_for_controlled_export", label: "锁定用于受控导出" },
  { action: "request_revision", label: "请求修订" },
  { action: "reject", label: "驳回" },
  { action: "mark_not_ready", label: "标记未准备好" },
  { action: "mark_low_confidence", label: "标记低置信度" }
];

export default function PersonalDeliveryPacketPage() {
  const [status, setStatus] = useState<PersonalDeliveryPacketStatus | null>(null);
  const [runtimes, setRuntimes] = useState<DeliveryPacketRuntimeList | null>(null);
  const [packets, setPackets] = useState<DeliveryPacketList | null>(null);
  const [items, setItems] = useState<PacketItemList | null>(null);
  const [bundles, setBundles] = useState<SourceBundleList | null>(null);
  const [readiness, setReadiness] = useState<ExportReadiness | null>(null);
  const [finalLocks, setFinalLocks] = useState<FinalLockList | null>(null);
  const [reviewSummary, setReviewSummary] = useState<ReviewSummary | null>(null);
  const [safety, setSafety] = useState<DeliveryPacketSafetyStatus | null>(null);
  const [selectedPacketId, setSelectedPacketId] = useState("");
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState("");
  const [error, setError] = useState("");

  const [packetForm, setPacketForm] = useState({
    production_case_id: "case_v55_approve_all",
    workflow_run_id: "workflow_run_demo",
    packet_title: "个人生产交付包草案",
    packet_scope: "律师复核前 metadata 汇总",
    client_alias: "client_demo",
    delivery_purpose: "受控导出准备度检查"
  });
  const [packetConfirmed, setPacketConfirmed] = useState(true);

  const [itemForm, setItemForm] = useState({
    item_title: "来源追踪包草案",
    item_type: "source_trace_summary",
    linked_object_type: "source_bundle",
    linked_object_id: "source_trace_demo",
    source_trace_ids: "trace_case_demo,trace_material_demo"
  });
  const [itemConfirmed, setItemConfirmed] = useState(true);

  const [bundleForm, setBundleForm] = useState({
    bundle_scope: "交付包来源追踪 metadata",
    source_trace_ids: "trace_case_demo,trace_material_demo,trace_review_demo"
  });
  const [bundleConfirmed, setBundleConfirmed] = useState(true);
  const [lockConfirmed, setLockConfirmed] = useState(true);

  async function loadConsole(nextPacketId?: string) {
    setLoading(true);
    setError("");
    try {
      const [statusData, runtimeData, packetData, itemData, bundleData, lockData, safetyData] = await Promise.all([
        personalDeliveryPacketApi.getStatus(),
        personalDeliveryPacketApi.listRuntimes(),
        personalDeliveryPacketApi.listPackets(),
        personalDeliveryPacketApi.listPacketItems(),
        personalDeliveryPacketApi.listSourceBundles(),
        personalDeliveryPacketApi.listFinalLocks(),
        personalDeliveryPacketApi.getSafety()
      ]);
      setStatus(statusData);
      setRuntimes(runtimeData);
      setPackets(packetData);
      setItems(itemData);
      setBundles(bundleData);
      setFinalLocks(lockData);
      setSafety(safetyData);

      const preferredPacketId = nextPacketId || selectedPacketId || packetData.delivery_packets?.[0]?.delivery_packet_id || "";
      setSelectedPacketId(preferredPacketId);
      if (preferredPacketId) {
        const [readinessData, reviewData] = await Promise.all([
          personalDeliveryPacketApi.getExportReadiness(preferredPacketId),
          personalDeliveryPacketApi.getReviewSummary(preferredPacketId)
        ]);
        setReadiness(readinessData);
        setReviewSummary(reviewData);
      } else {
        setReadiness(null);
        setReviewSummary(null);
      }
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "无法加载个人生产交付包控制台");
    } finally {
      setLoading(false);
    }
  }

  async function loadPacketDetails(deliveryPacketId: string) {
    if (!deliveryPacketId) {
      setReadiness(null);
      setReviewSummary(null);
      return;
    }
    try {
      const [readinessData, reviewData] = await Promise.all([
        personalDeliveryPacketApi.getExportReadiness(deliveryPacketId),
        personalDeliveryPacketApi.getReviewSummary(deliveryPacketId)
      ]);
      setReadiness(readinessData);
      setReviewSummary(reviewData);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "无法加载交付包详情");
    }
  }

  useEffect(() => {
    void loadConsole();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const selectedPacket = useMemo<DeliveryPacketRecord | null>(
    () => packets?.delivery_packets?.find((packet) => packet.delivery_packet_id === selectedPacketId) ?? null,
    [packets, selectedPacketId]
  );

  const statusCards = [
    { label: "交付包状态", value: selectedPacket?.packet_status ?? "draft_pending", tone: "preview" },
    { label: "交付项清单", value: `${items?.packet_items?.length ?? 0} 项`, tone: "safe" },
    { label: "来源追踪包", value: `${bundles?.source_bundles?.length ?? 0} 个`, tone: "safe" },
    { label: "导出准备度", value: String(readiness?.export_readiness_status ?? "not_ready"), tone: "blocked" },
    { label: "最终锁定", value: String(selectedPacket?.final_locked ?? false), tone: selectedPacket?.final_locked ? "safe" : "preview" },
    { label: "审核摘要", value: String(reviewSummary?.lawyer_review_status ?? "pending"), tone: "preview" }
  ];

  async function createPacket(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setActionMessage("");
    const packet = await personalDeliveryPacketApi.createPacket({
      ...packetForm,
      workflow_run_id: packetForm.workflow_run_id || null,
      explicit_mock_confirmation: packetConfirmed,
      explicit_lawyer_review_confirmation: packetConfirmed,
      explicit_no_raw_content_confirmation: packetConfirmed,
      explicit_no_final_opinion_confirmation: packetConfirmed,
      explicit_no_external_delivery_confirmation: packetConfirmed
    });
    setActionMessage(`已创建交付包草案：${packet.delivery_packet_id}`);
    await loadConsole(packet.delivery_packet_id);
  }

  async function createPacketItem(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedPacketId) {
      setError("请先创建或选择交付包草案");
      return;
    }
    const item = await personalDeliveryPacketApi.createPacketItem({
      delivery_packet_id: selectedPacketId,
      item_title: itemForm.item_title,
      item_type: itemForm.item_type,
      linked_object_type: itemForm.linked_object_type,
      linked_object_id: itemForm.linked_object_id,
      source_trace_ids: splitIds(itemForm.source_trace_ids),
      explicit_mock_confirmation: itemConfirmed,
      explicit_no_raw_content_confirmation: itemConfirmed,
      explicit_no_final_opinion_confirmation: itemConfirmed
    });
    setActionMessage(`已添加交付项草案：${item.packet_item_id}`);
    await loadConsole(selectedPacketId);
  }

  async function createSourceBundle(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!selectedPacketId) {
      setError("请先创建或选择交付包草案");
      return;
    }
    const bundle = await personalDeliveryPacketApi.createSourceBundle({
      delivery_packet_id: selectedPacketId,
      bundle_scope: bundleForm.bundle_scope,
      source_trace_ids: splitIds(bundleForm.source_trace_ids),
      explicit_mock_confirmation: bundleConfirmed,
      explicit_source_trace_confirmation: bundleConfirmed,
      explicit_no_raw_content_confirmation: bundleConfirmed
    });
    setActionMessage(`已生成来源追踪包：${bundle.source_bundle_id}`);
    await loadConsole(selectedPacketId);
  }

  async function submitLockAction(action: string) {
    if (!selectedPacketId) {
      setError("请先创建或选择交付包草案");
      return;
    }
    const result = await personalDeliveryPacketApi.submitFinalLockAction(selectedPacketId, {
      action,
      reviewer_id: "lawyer_reviewer_demo",
      reviewer_note: "仅确认 metadata 状态，不触发真实导出。",
      explicit_lawyer_confirmation: lockConfirmed,
      explicit_final_lock_confirmation: lockConfirmed,
      explicit_no_real_export_confirmation: lockConfirmed,
      explicit_no_email_confirmation: lockConfirmed,
      explicit_no_final_opinion_confirmation: lockConfirmed,
      explicit_no_final_report_confirmation: lockConfirmed,
      explicit_no_external_delivery_confirmation: lockConfirmed
    });
    setActionMessage(`已提交最终锁定队列动作：${result.action}`);
    await loadConsole(selectedPacketId);
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <SafeErrorNotice message={error} /> : null}
        {actionMessage ? <div className="rounded-md border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">{actionMessage}</div> : null}

        <section className="overflow-hidden rounded-md border border-slate-800 bg-[#111827] text-white shadow-sm">
          <div className="grid gap-6 p-6 lg:grid-cols-[1.2fr_0.8fr] lg:p-8">
            <div>
              <div className="flex flex-wrap gap-2">
                {["仅模拟结果", "仅元数据", "律师复核必需", "Final Lock 不触发真实导出", "不自动对外交付"].map((badge) => (
                  <DarkSafetyBadge key={badge} label={badge} />
                ))}
              </div>
              <h1 className="mt-5 text-3xl font-semibold leading-tight md:text-5xl">个人生产交付包</h1>
              <p className="mt-4 max-w-3xl text-sm leading-6 text-slate-300 md:text-base">
                把 v7.5 受控案件生产工作流 metadata 汇总成受控交付包草案。交付包草案不是最终交付文件，Final Lock 不触发真实导出，仅用于律师复核后的 metadata 门禁展示。
              </p>
              <div className="mt-5 grid gap-2 text-sm text-slate-300 sm:grid-cols-2">
                <span>不生成最终法律意见</span>
                <span>不生成最终报告</span>
                <span>不发送邮件</span>
                <span>不生成真实 PDF/DOCX</span>
                <span>不自动对外交付</span>
                <span>外部交付后置</span>
              </div>
            </div>
            <div className="rounded-md border border-white/10 bg-white/5 p-4">
              <div className="text-xs font-semibold uppercase tracking-wide text-cyan-100">Runtime Status</div>
              <div className="mt-4 grid gap-3">
                <Metric label="version" value={String(status?.version ?? "v7.6")} />
                <Metric label="runtime_count" value={String(runtimes?.runtime_count ?? 0)} />
                <Metric label="live_provider_call_executed" value={String(status?.live_provider_call_executed ?? false)} />
                <Metric label="external_delivery_triggered" value={String(status?.external_delivery_triggered ?? false)} />
              </div>
            </div>
          </div>
        </section>

        <section className="rounded-md border border-line bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between gap-3">
            <h2 className="text-lg font-semibold text-ink">交付流程 Stepper</h2>
            <span className="text-xs text-muted">草案 · 交付项 · 来源追踪 · 律师复核 · 最终锁定</span>
          </div>
          <ShowcaseStepper steps={stepper.map((step) => ({ label: step.label, detail: step.detail, status: "draft metadata" }))} columns="md:grid-cols-3 xl:grid-cols-5" />
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-6">
          {statusCards.map((card) => (
            <div key={card.label} className="rounded-md border border-line bg-white p-4 shadow-sm">
              <div className="text-xs text-muted">{card.label}</div>
              <div className="mt-2 break-words text-lg font-semibold text-ink">{card.value}</div>
              <StatusBadge tone={card.tone} />
            </div>
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <Panel title="创建交付包草案">
            <form className="grid gap-4" onSubmit={createPacket}>
              <Field label="Production Case ID" value={packetForm.production_case_id} onChange={(value) => setPacketForm({ ...packetForm, production_case_id: value })} />
              <Field label="Workflow Run ID" value={packetForm.workflow_run_id} onChange={(value) => setPacketForm({ ...packetForm, workflow_run_id: value })} />
              <Field label="交付包标题" value={packetForm.packet_title} onChange={(value) => setPacketForm({ ...packetForm, packet_title: value })} />
              <Field label="交付范围" value={packetForm.packet_scope} onChange={(value) => setPacketForm({ ...packetForm, packet_scope: value })} />
              <Field label="客户代号" value={packetForm.client_alias} onChange={(value) => setPacketForm({ ...packetForm, client_alias: value })} />
              <Field label="交付目的" value={packetForm.delivery_purpose} onChange={(value) => setPacketForm({ ...packetForm, delivery_purpose: value })} />
              <Confirm checked={packetConfirmed} onChange={setPacketConfirmed} label="我确认当前仅创建交付包 metadata 草案，不读取原文、不生成最终法律意见、不对外交付。" />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-300" disabled={!packetConfirmed || loading}>
                创建交付包草案
              </button>
            </form>
          </Panel>

          <Panel title="当前交付包">
            <div className="grid gap-3">
              <label className="grid gap-2 text-sm">
                <span className="font-medium text-ink">Delivery Packet ID</span>
                <select
                  className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink"
                  value={selectedPacketId}
                  onChange={(event) => {
                    setSelectedPacketId(event.target.value);
                    void loadPacketDetails(event.target.value);
                  }}
                >
                  <option value="">未选择</option>
                  {(packets?.delivery_packets ?? []).map((packet) => (
                    <option key={packet.delivery_packet_id} value={packet.delivery_packet_id}>
                      {packet.delivery_packet_id}
                    </option>
                  ))}
                </select>
              </label>
              <InfoRows
                rows={[
                  ["packet_title", selectedPacket?.packet_title],
                  ["packet_status", selectedPacket?.packet_status],
                  ["final_locked", selectedPacket?.final_locked],
                  ["export_ready", selectedPacket?.export_ready],
                  ["raw_content_included", selectedPacket?.raw_content_included],
                  ["external_delivery_triggered", selectedPacket?.external_delivery_triggered]
                ]}
              />
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="添加交付项草案">
            <form className="grid gap-4" onSubmit={createPacketItem}>
              <Field label="交付项标题" value={itemForm.item_title} onChange={(value) => setItemForm({ ...itemForm, item_title: value })} />
              <label className="grid gap-2 text-sm">
                <span className="font-medium text-ink">交付项类型</span>
                <select className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink" value={itemForm.item_type} onChange={(event) => setItemForm({ ...itemForm, item_type: event.target.value })}>
                  {itemTypes.map((type) => (
                    <option key={type} value={type}>{type}</option>
                  ))}
                </select>
              </label>
              <Field label="Linked Object Type" value={itemForm.linked_object_type} onChange={(value) => setItemForm({ ...itemForm, linked_object_type: value })} />
              <Field label="Linked Object ID" value={itemForm.linked_object_id} onChange={(value) => setItemForm({ ...itemForm, linked_object_id: value })} />
              <Field label="Source Trace IDs" value={itemForm.source_trace_ids} onChange={(value) => setItemForm({ ...itemForm, source_trace_ids: value })} />
              <Confirm checked={itemConfirmed} onChange={setItemConfirmed} label="我确认该交付项仅为草案元数据，不包含原始内容，不生成最终意见。" />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-300" disabled={!itemConfirmed || !selectedPacketId}>
                添加交付项草案
              </button>
            </form>
          </Panel>

          <Panel title="生成来源追踪包">
            <form className="grid gap-4" onSubmit={createSourceBundle}>
              <Field label="Source Trace IDs" value={bundleForm.source_trace_ids} onChange={(value) => setBundleForm({ ...bundleForm, source_trace_ids: value })} />
              <Field label="bundle_scope" value={bundleForm.bundle_scope} onChange={(value) => setBundleForm({ ...bundleForm, bundle_scope: value })} />
              <Confirm checked={bundleConfirmed} onChange={setBundleConfirmed} label="我确认来源追踪必需，当前仅生成来源 metadata，不返回案件原文。" />
              <button className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:bg-slate-300" disabled={!bundleConfirmed || !selectedPacketId}>
                生成来源追踪包
              </button>
            </form>
            <div className="mt-5 grid gap-2 text-xs text-muted">
              <span>原始内容已排除：true</span>
              <span>source trace required: true</span>
              <span>confirmed / unconfirmed source count: {String(bundles?.source_bundles?.[0]?.confirmed_source_count ?? 0)} / {String(bundles?.source_bundles?.[0]?.unconfirmed_source_count ?? 0)}</span>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
          <Panel title="导出准备度">
            <InfoRows
              rows={[
                ["export_readiness_status", readiness?.export_readiness_status],
                ["required_item_count", readiness?.required_item_count],
                ["included_item_count", readiness?.included_item_count],
                ["missing_item_types", Array.isArray(readiness?.missing_item_types) ? readiness?.missing_item_types.join(", ") : ""],
                ["source_trace_complete", readiness?.source_trace_complete],
                ["lawyer_review_complete", readiness?.lawyer_review_complete],
                ["final_lock_ready", readiness?.final_lock_ready],
                ["export_ready", readiness?.export_ready],
                ["external_delivery_ready", readiness?.external_delivery_ready]
              ]}
            />
          </Panel>

          <Panel title="最终锁定队列">
            <Confirm checked={lockConfirmed} onChange={setLockConfirmed} label="我确认 final lock 仅更新 metadata，不触发真实导出、不发送邮件、不生成最终法律意见或最终报告。" />
            <div className="mt-4 grid gap-2 md:grid-cols-2">
              {lockActions.map((item) => (
                <button
                  key={item.action}
                  className="rounded-md border border-line bg-white px-3 py-2 text-sm font-semibold text-ink hover:bg-slate-50 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-400"
                  disabled={!lockConfirmed || !selectedPacketId}
                  onClick={() => void submitLockAction(item.action)}
                >
                  {item.label}
                </button>
              ))}
            </div>
            <div className="mt-5 grid gap-2 text-xs text-muted">
              <span>final lock 不触发真实导出</span>
              <span>final lock 不发送邮件</span>
              <span>final lock 不生成最终法律意见</span>
              <span>final lock 不生成最终报告</span>
              <span>queue_count: {String(finalLocks?.final_locks?.length ?? 0)}</span>
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="律师复核摘要">
            <InfoRows
              rows={[
                ["lawyer_review_status", reviewSummary?.lawyer_review_status],
                ["revision_required", reviewSummary?.revision_required],
                ["risk_flags", Array.isArray(reviewSummary?.risk_flags) ? reviewSummary?.risk_flags.join(", ") : ""],
                ["final_lock_ready", reviewSummary?.final_lock_ready],
                ["raw_content_included", reviewSummary?.raw_content_included]
              ]}
            />
          </Panel>

          <TrustSafetyPanel items={safety?.safety_checklist?.length ? safety.safety_checklist : safetyChecks} title="安全检查清单" />
        </section>

        <Panel title="开发诊断（默认折叠）">
          <DiagnosticsPanel data={{ status, runtimes, selectedPacket, readiness, reviewSummary, finalLocks, safety }} />
        </Panel>
      </div>
    </AppShell>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="grid gap-2 text-sm">
      <span className="font-medium text-ink">{label}</span>
      <input className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink" value={value} onChange={(event) => onChange(event.target.value)} />
    </label>
  );
}

function Confirm({ checked, label, onChange }: { checked: boolean; label: string; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex items-start gap-3 rounded-md border border-cyan-200 bg-cyan-50 px-3 py-2 text-sm text-cyan-900">
      <input className="mt-1" type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-md border border-line bg-white p-5 shadow-sm">
      <h2 className="text-lg font-semibold text-ink">{title}</h2>
      <div className="mt-4">{children}</div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between gap-3 rounded-md border border-white/10 bg-white/5 px-3 py-2">
      <span className="text-xs text-slate-300">{label}</span>
      <span className="break-all text-sm font-semibold text-white">{value}</span>
    </div>
  );
}

function StatusBadge({ tone }: { tone: string }) {
  const styles = tone === "safe" ? "bg-emerald-50 text-emerald-700" : tone === "blocked" ? "bg-amber-50 text-amber-700" : "bg-cyan-50 text-cyan-700";
  const label = tone === "safe" ? "受控" : tone === "blocked" ? "未就绪" : "草案";
  return <div className={`mt-3 inline-flex rounded-md px-2 py-1 text-xs font-semibold ${styles}`}>{label}</div>;
}

function InfoRows({ rows }: { rows: Array<[string, unknown]> }) {
  return (
    <div className="grid gap-2">
      {rows.map(([label, value]) => (
        <div key={label} className="grid gap-1 rounded-md border border-line bg-slate-50 px-3 py-2 text-sm md:grid-cols-[220px_1fr]">
          <span className="font-medium text-muted">{label}</span>
          <span className="break-words text-ink">{String(value ?? "pending")}</span>
        </div>
      ))}
    </div>
  );
}

function splitIds(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}
