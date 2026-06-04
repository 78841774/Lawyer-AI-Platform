"use client";

import { FormEvent, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  PersonalAlphaFinalLockCreateRequest,
  PersonalAlphaFinalLockCreateResult,
  PersonalAlphaFinalLockList,
  PersonalAlphaFinalLockReadiness,
  PersonalAlphaFinalLockRecord,
  PersonalAlphaFinalLockStatus,
  createPersonalAlphaFinalLock,
  getPersonalAlphaFinalLock,
  getPersonalAlphaFinalLockReadiness,
  getPersonalAlphaFinalLockStatus,
  listPersonalAlphaFinalLocks,
  listPersonalAlphaFinalLocksByPacket
} from "@/services/api";

const DEFAULT_CREATE_FORM: PersonalAlphaFinalLockCreateRequest = {
  reviewer_id: "local_demo_lawyer",
  manual_review_confirmed: true,
  lawyer_review_confirmed: true,
  metadata_only_confirmation: true,
  no_final_legal_opinion_confirmation: true,
  no_final_report_generation_confirmation: true
};

export default function PersonalAlphaFinalLockPage() {
  const router = useRouter();
  const [status, setStatus] = useState<PersonalAlphaFinalLockStatus | null>(null);
  const [readiness, setReadiness] = useState<PersonalAlphaFinalLockReadiness | null>(null);
  const [createResult, setCreateResult] = useState<PersonalAlphaFinalLockCreateResult | null>(null);
  const [allLocks, setAllLocks] = useState<PersonalAlphaFinalLockList | null>(null);
  const [packetLocks, setPacketLocks] = useState<PersonalAlphaFinalLockList | null>(null);
  const [lockDetail, setLockDetail] = useState<PersonalAlphaFinalLockRecord | null>(null);
  const [packetId, setPacketId] = useState("");
  const [lockId, setLockId] = useState("");
  const [createForm, setCreateForm] = useState(DEFAULT_CREATE_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadInitial() {
      try {
        const [nextStatus, nextLocks] = await Promise.all([
          getPersonalAlphaFinalLockStatus(),
          listPersonalAlphaFinalLocks()
        ]);
        setStatus(nextStatus);
        setAllLocks(nextLocks);
        const queryValue = new URLSearchParams(window.location.search).get("packet_id") ?? "";
        if (queryValue) {
          setPacketId(queryValue);
          await loadReadiness(queryValue);
        }
      } catch {
        setError("Personal Alpha Final Lock API 暂不可用，请确认后端服务已启动。");
      }
    }

    void loadInitial();
  }, []);

  async function loadReadiness(id: string) {
    const trimmed = id.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const [nextReadiness, nextPacketLocks, nextLocks] = await Promise.all([
        getPersonalAlphaFinalLockReadiness(trimmed),
        listPersonalAlphaFinalLocksByPacket(trimmed),
        listPersonalAlphaFinalLocks()
      ]);
      setReadiness(nextReadiness);
      setPacketLocks(nextPacketLocks);
      setAllLocks(nextLocks);
    } catch {
      setError("Final lock readiness 加载失败，请确认 packet_id 已完成 Lawyer Final Review approve_packet。");
    } finally {
      setLoading(false);
    }
  }

  async function loadLock(id: string) {
    const trimmed = id.trim();
    if (!trimmed) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const nextLock = await getPersonalAlphaFinalLock(trimmed);
      setLockDetail(nextLock);
      setLockId(trimmed);
    } catch {
      setError("Final lock detail 加载失败。");
    } finally {
      setLoading(false);
    }
  }

  async function submitReadiness(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = packetId.trim();
    if (!id) {
      return;
    }
    router.replace(`/personal-alpha-final-lock?packet_id=${encodeURIComponent(id)}`);
    await loadReadiness(id);
  }

  async function submitCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const id = packetId.trim();
    if (!id) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const result = await createPersonalAlphaFinalLock(id, createForm);
      const [nextReadiness, nextPacketLocks, nextLocks] = await Promise.all([
        getPersonalAlphaFinalLockReadiness(id),
        listPersonalAlphaFinalLocksByPacket(id),
        listPersonalAlphaFinalLocks()
      ]);
      setCreateResult(result);
      setReadiness(nextReadiness);
      setPacketLocks(nextPacketLocks);
      setAllLocks(nextLocks);
      if (result.lock_id) {
        setLockId(result.lock_id);
        setLockDetail(await getPersonalAlphaFinalLock(result.lock_id));
      }
    } catch {
      setError("Final lock 创建失败，请确认 latest lawyer action 为 approve_packet 且所有 confirmation 均已勾选。");
    } finally {
      setLoading(false);
    }
  }

  async function submitLockDetail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await loadLock(lockId);
  }

  const lockList = allLocks?.locks ?? [];

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Personal Alpha"
          title="Personal Alpha Controlled Final Lock"
          description="个人 Alpha 终审锁定：在律师终审复核 approve_packet 后，生成 metadata-only 的 controlled final lock。该页面不生成正式法律意见，不生成最终报告正文，不调用真实服务。"
        />
        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Safety Boundary</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="mode" value={status?.mode ?? "local_only_personal_alpha_final_lock"} />
              <InfoRow label="local-only" value="true" />
              <InfoRow label="mock_first_enabled" value={String(status?.mock_first_enabled ?? true)} />
              <InfoRow label="controlled_first_enabled" value={String(status?.controlled_first_enabled ?? true)} />
              <InfoRow label="metadata_only" value={String(status?.metadata_only ?? true)} />
              <InfoRow label="advisory_only" value={String(status?.advisory_only ?? true)} />
              <InfoRow label="requires_lawyer_final_review_approval" value={String(status?.requires_lawyer_final_review_approval ?? true)} />
              <InfoRow label="requires_lawyer_review" value={String(status?.requires_lawyer_review ?? true)} />
              <InfoRow label="final_report_generation_enabled" value={String(status?.final_report_generation_enabled ?? false)} />
              <InfoRow label="final_legal_opinion_enabled" value={String(status?.final_legal_opinion_enabled ?? false)} />
              <InfoRow label="llm_live_enabled" value={String(status?.llm_live_enabled ?? false)} />
              <InfoRow label="deepseek_live_enabled" value={String(status?.deepseek_live_enabled ?? false)} />
              <InfoRow label="ocr_live_enabled" value={String(status?.ocr_live_enabled ?? false)} />
              <InfoRow label="legal_search_live_enabled" value={String(status?.legal_search_live_enabled ?? false)} />
              <InfoRow label="runtime_storage_path" value={status?.runtime_storage_path ?? "storage/runtime/personal_alpha_final_lock/locks"} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Packet Input</h2>
            <form onSubmit={submitReadiness} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="packet_id" value={packetId} onChange={setPacketId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading}>{loading ? "加载中..." : "Load Final Lock Readiness"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
          <BooleanTile label="can create lock" value={readiness?.can_create_final_lock ?? false} />
          <BooleanTile label="requires lawyer approval" value={readiness?.requires_lawyer_final_review_approval ?? true} />
          <BooleanTile label="raw included" value={readiness?.raw_content_included ?? false} />
          <SummaryTile label="all locks" value={allLocks?.lock_count ?? 0} />
          <SummaryTile label="packet locks" value={packetLocks?.lock_count ?? 0} />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Lock Readiness</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="packet_id" value={(readiness?.packet_id ?? packetId) || "-"} />
              <InfoRow label="workspace_run_id" value={readiness?.workspace_run_id ?? "-"} />
              <InfoRow label="status" value={readiness?.status ?? "not_loaded"} />
              <InfoRow label="can_create_final_lock" value={String(readiness?.can_create_final_lock ?? false)} />
              <InfoRow label="latest_lawyer_review_action" value={readiness?.latest_lawyer_review_action ?? "-"} />
              <InfoRow label="final_legal_opinion_generated" value={String(readiness?.final_legal_opinion_generated ?? false)} />
              <InfoRow label="final_report_generated" value={String(readiness?.final_report_generated ?? false)} />
              <InfoRow label="mock_or_redacted_only" value={String(readiness?.mock_or_redacted_only ?? true)} />
            </div>
            <JsonPanel title="readiness_requirements" value={readiness?.readiness_requirements ?? {}} />
            <JsonPanel title="warnings" value={readiness?.warnings ?? []} />
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Create Final Lock Form</h2>
            <form onSubmit={submitCreate} className="mt-4 grid gap-4 md:grid-cols-2">
              <TextField label="reviewer_id" value={createForm.reviewer_id} onChange={(value) => setCreateForm((current) => ({ ...current, reviewer_id: value }))} />
              <div className="hidden md:block" />
              <CheckField label="manual_review_confirmed" checked={createForm.manual_review_confirmed} onChange={(checked) => setCreateForm((current) => ({ ...current, manual_review_confirmed: checked }))} />
              <CheckField label="lawyer_review_confirmed" checked={createForm.lawyer_review_confirmed} onChange={(checked) => setCreateForm((current) => ({ ...current, lawyer_review_confirmed: checked }))} />
              <CheckField label="metadata_only_confirmation" checked={createForm.metadata_only_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, metadata_only_confirmation: checked }))} />
              <CheckField label="no_final_legal_opinion_confirmation" checked={createForm.no_final_legal_opinion_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, no_final_legal_opinion_confirmation: checked }))} />
              <CheckField label="no_final_report_generation_confirmation" checked={createForm.no_final_report_generation_confirmation} onChange={(checked) => setCreateForm((current) => ({ ...current, no_final_report_generation_confirmation: checked }))} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !packetId.trim()}>{loading ? "创建中..." : "Create Final Lock"}</Button>
              </div>
            </form>
            {createResult ? <JsonPanel title="create_result" value={createResult} /> : null}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Final Lock List</h2>
            <div className="mt-4 grid gap-3">
              {lockList.length ? lockList.map((item) => (
                <div key={item.lock_id} className="grid gap-3 rounded-md border border-line bg-paper p-3 md:grid-cols-[1fr_1fr_auto_auto] md:items-center">
                  <InfoRow label="lock_id" value={item.lock_id} />
                  <InfoRow label="packet_id" value={item.packet_id} />
                  <InfoRow label="status" value={item.status} />
                  <button type="button" onClick={() => void loadLock(item.lock_id)} className="rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">Detail</button>
                </div>
              )) : (
                <StatusMessage message="暂无 final lock records。Final lock 只会在 create API 成功后写入 ignored runtime storage。" />
              )}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Final Lock Detail</h2>
            <form onSubmit={submitLockDetail} className="mt-4 grid gap-4 md:grid-cols-[1fr_auto]">
              <TextField label="lock_id" value={lockId} onChange={setLockId} />
              <div className="flex items-end">
                <Button type="submit" disabled={loading || !lockId.trim()}>{loading ? "加载中..." : "Load Final Lock Detail"}</Button>
              </div>
            </form>
            <JsonPanel title="lock_detail" value={lockDetail ?? {}} />
            <JsonPanel title="packet_locks" value={packetLocks ?? {}} />
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
