"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaFinalPacketCreateRequest,
  PersonalAlphaFinalPacketCreateResult,
  PersonalAlphaFinalPacketList,
  PersonalAlphaFinalPacketPreview,
  PersonalAlphaFinalPacketRecord,
  PersonalAlphaFinalPacketStatus,
  createPersonalAlphaFinalPacket,
  getPersonalAlphaFinalPacket,
  getPersonalAlphaFinalPacketPreview,
  getPersonalAlphaFinalPacketStatus,
  listPersonalAlphaFinalPackets,
  listPersonalAlphaFinalPacketsByRun
} from "@/services/api";

const DEFAULT_CREATE_FORM: PersonalAlphaFinalPacketCreateRequest = {
  reviewer_id: "local_demo_reviewer",
  manual_review_confirmed: true,
  metadata_only_confirmation: true,
  no_final_legal_opinion_confirmation: true,
  no_final_report_generation_confirmation: true
};

export default function PersonalAlphaFinalPacketPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaFinalPacketStatus | null>(null);
  const [preview, setPreview] = useState<PersonalAlphaFinalPacketPreview | null>(null);
  const [createResult, setCreateResult] = useState<PersonalAlphaFinalPacketCreateResult | null>(null);
  const [allPackets, setAllPackets] = useState<PersonalAlphaFinalPacketList | null>(null);
  const [runPackets, setRunPackets] = useState<PersonalAlphaFinalPacketList | null>(null);
  const [packetDetail, setPacketDetail] = useState<PersonalAlphaFinalPacketRecord | null>(null);
  const [workspaceRunId, setWorkspaceRunId] = useState("");
  const [packetId, setPacketId] = useState("");
  const [createForm, setCreateForm] = useState(DEFAULT_CREATE_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadInitial() {
      try {
        const [nextStatus, nextPackets] = await Promise.all([
          getPersonalAlphaFinalPacketStatus(),
          listPersonalAlphaFinalPackets()
        ]);
        setStatus(nextStatus);
        setAllPackets(nextPackets);
        const queryValue = new URLSearchParams(window.location.search).get("workspace_run_id") ?? "";
        if (queryValue) {
          setWorkspaceRunId(queryValue);
          await loadPreview(queryValue);
        }
      } catch {
        setError("Personal Alpha Final Packet API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadInitial();
  }, []);

  async function loadPreview(id: string) {
    setLoading(true);
    setError("");
    try {
      const [nextPreview, nextRunPackets, nextPackets] = await Promise.all([
        getPersonalAlphaFinalPacketPreview(id),
        listPersonalAlphaFinalPacketsByRun(id),
        listPersonalAlphaFinalPackets()
      ]);
      setPreview(nextPreview);
      setRunPackets(nextRunPackets);
      setAllPackets(nextPackets);
    } catch {
      setError("Packet preview 加载失败，请确认 workspace_run_id 存在且后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  async function loadPacket(id: string) {
    const trimmed = id.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const nextPacket = await getPersonalAlphaFinalPacket(trimmed);
      setPacketDetail(nextPacket);
      setPacketId(trimmed);
    } catch {
      setError("Packet detail 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  async function submitPreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = workspaceRunId.trim();
    if (!id) {
      return;
    }
    router.replace(`/personal-alpha-final-packet?workspace_run_id=${encodeURIComponent(id)}`);
    await loadPreview(id);
  }

  async function submitCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = workspaceRunId.trim();
    if (!id) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await createPersonalAlphaFinalPacket(id, createForm);
      const [nextPreview, nextRunPackets, nextPackets] = await Promise.all([
        getPersonalAlphaFinalPacketPreview(id),
        listPersonalAlphaFinalPacketsByRun(id),
        listPersonalAlphaFinalPackets()
      ]);
      setCreateResult(result);
      setPreview(nextPreview);
      setRunPackets(nextRunPackets);
      setAllPackets(nextPackets);
      if (result.packet_id) {
        setPacketId(result.packet_id);
        setPacketDetail(await getPersonalAlphaFinalPacket(result.packet_id));
      }
    } catch {
      setError("Packet 创建失败，请确认 Final Gate 已 approve 且所有 confirmation 均已勾选。");
    } finally {
      setLoading(false);
    }
  }

  async function submitPacketDetail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await loadPacket(packetId);
  }

  const sections = preview?.packet_preview?.packet_sections ?? [];
  const packetList = allPackets?.packets ?? [];

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Controlled Final Review Packet"
          description="个人 Alpha 终审材料包：在 Final Gate 通过后生成 metadata-only 的 controlled final review packet。该页面不生成正式法律意见，不生成最终报告正文，不调用真实服务。"
        />
        <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
          Final Lock requires Lawyer Final Review approval first. Use the Lawyer Final Review page before creating any controlled final lock.
        </div>
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_final_packet"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="requires_final_gate_approval" value={String(status?.requires_final_gate_approval ?? true)} />
              <InfoRow label="requires_manual_review" value={String(status?.requires_manual_review ?? true)} />
              <InfoRow label="final_report_generation_enabled" value={String(status?.final_report_generation_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/personal_alpha_final_packet/packets"} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Workspace Run Input</h2>
            <form onSubmit={submitPreview} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="workspace_run_id" value={workspaceRunId} onChange={setWorkspaceRunId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Packet Preview"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <BooleanTile label="can create packet" value={preview?.can_create_packet ?? false} />
          <BooleanTile label="requires gate" value={preview?.requires_final_gate_approval ?? true} />
          <BooleanTile label="raw included" value={preview?.raw_content_included ?? false} />
          <SummaryTile label="sections" value={sections.length} />
          <SummaryTile label="run packets" value={runPackets?.packet_count ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Preview</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="workspace_run_id" value={(preview?.workspace_run_id ?? workspaceRunId) || "-"} />
              <InfoRow label="status" value={preview?.status ?? "not_loaded"} />
              <InfoRow label="can_create_packet" value={String(preview?.can_create_packet ?? false)} />
              <InfoRow label="title" value={preview?.packet_preview?.title ?? "-"} />
              <InfoRow label="case_id" value={preview?.packet_preview?.case_id ?? "-"} />
              <InfoRow label="workspace_id" value={preview?.packet_preview?.workspace_id ?? "-"} />
              <InfoRow label="workflow_mode" value={preview?.packet_preview?.workflow_mode ?? "-"} />
              <InfoRow label="final_report_generated" value={String(preview?.final_report_generated ?? false)} />
            </div>
            <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-5">
              {sections.map((section) => (
                <div key={section.section_id} className="rounded-md border border-line bg-paper p-3">
                  <div className="text-sm font-semibold text-ink">{section.title}</div>
                  <div className="mt-2 text-xs text-muted">{section.section_id}</div>
                  <div className="mt-2 text-xs text-muted">items: {section.items.length}</div>
                </div>
              ))}
            </div>
            <JsonPanel title="packet_preview" value={preview ?? {}} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Create Packet Form</h2>
            <form onSubmit={submitCreate} className="mt-4 grid gap-4 md:grid-cols-2">
              <TextField label="reviewer_id" value={createForm.reviewer_id} onChange={(value) => setCreateForm((current) => ({ ...current, reviewer_id: value }))} />
              <div className="hidden md:block" />
              <CheckField label="manual_review_confirmed" checked={createForm.manual_review_confirmed} onChange={(checked) => setCreateForm((current) => ({ ...current, manual_review_confirmed: checked }))} />
              <CheckField label="metadata_only_confirmation" checked={createForm.metadata_only_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, metadata_only_confirmation: checked }))} />
              <CheckField label="no_final_legal_opinion_confirmation" checked={createForm.no_final_legal_opinion_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, no_final_legal_opinion_confirmation: checked }))} />
              <CheckField label="no_final_report_generation_confirmation" checked={createForm.no_final_report_generation_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, no_final_report_generation_confirmation: checked }))} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !workspaceRunId.trim()}>{loading ? "创建中..." : "Create Packet"}</Button>
              </div>
            </form>
            {createResult ? <JsonPanel title="create_result" value={createResult} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet List</h2>
            <div className="mt-4 grid gap-3">
              {packetList.length ? packetList.map((item) => (
                <div key={item.packet_id} className="grid gap-3 rounded-md border border-line bg-paper p-3 md:grid-cols-[1fr_1fr_auto_auto] md:items-center">
                  <InfoRow label="packet_id" value={item.packet_id} />
                  <InfoRow label="workspace_run_id" value={item.workspace_run_id} />
                  <InfoRow label="status" value={item.status} />
                  <div className="flex gap-2">
                    <button type="button" onClick={() => void loadPacket(item.packet_id)} className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">Detail</button>
                    <Link href={`/personal-alpha-lawyer-final-review?packet_id=${encodeURIComponent(item.packet_id)}`} className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
                      View Lawyer Final Review
                    </Link>
                  </div>
                </div>
              )) : (
                <StatusMessage message="暂无 packet records。Packet 只会在 create API 成功后写入 ignored runtime storage。" />
              )}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Detail</h2>
            <form onSubmit={submitPacketDetail} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="packet_id" value={packetId} onChange={setPacketId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !packetId.trim()}>{loading ? "加载中..." : "Load Packet Detail"}</Button>
              </div>
            </form>
            {packetDetail?.packet_id && packetDetail.status !== "not_found" ? (
              <div className="mt-4">
                <Link href={`/personal-alpha-lawyer-final-review?packet_id=${encodeURIComponent(packetDetail.packet_id)}`} className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
                  View Lawyer Final Review
                </Link>
              </div>
            ) : null}
            <JsonPanel title="packet_detail" value={packetDetail ?? {}} />
            <JsonPanel title="run_packets" value={runPackets ?? {}} />
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

function BooleanTile({ label, value }: { label: string; value: boolean }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">{label}</div>
        <div className="mt-2 text-xl font-semibold text-ink">{String(value)}</div>
      </CardBody>
    </Card>
  );
}

function TextField({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="text-sm">
      <span className="text-muted">{label}</span>
      <input value={value} onChange={(event) => onChange(event.target.value)} className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink" />
    </label>
  );
}

function CheckField({ label, checked, onChange }: { label: string; checked: boolean; onChange: (checked: boolean) => void }) {
  return (
    <label className="flex items-center gap-2 rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}

function JsonPanel({ title, value }: { title: string; value: unknown }) {
  return (
    <div className="mt-4">
      <div className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</div>
      <pre className="mt-2 max-h-96 overflow-auto rounded-md border border-line bg-paper p-3 text-xs text-slate-700">{JSON.stringify(value ?? {}, null, 2)}</pre>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
