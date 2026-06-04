"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  CitationResolutionResult,
  SourceRefsStatus,
  SourceTrace,
  getMockSourceTrace,
  getSourceRefsStatus,
  resolveCitation
} from "@/services/api";

export default function SourceRefsPage() {
  const [status, setStatus] = useState<SourceRefsStatus | null>(null);
  const [trace, setTrace] = useState<SourceTrace | null>(null);
  const [resolution, setResolution] = useState<CitationResolutionResult | null>(null);
  const [reportId, setReportId] = useState("report_demo_001");
  const [citationId, setCitationId] = useState("citation_mock_001");
  const [error, setError] = useState("");
  const [traceLoading, setTraceLoading] = useState(false);
  const [citationLoading, setCitationLoading] = useState(false);

  useEffect(() => {
    getSourceRefsStatus().then(setStatus).catch(() => setError("Source Refs status 暂不可用，请确认后端服务已启动。"));
  }, []);

  async function submitTrace(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setTraceLoading(true);
    setError("");
    try {
      setTrace(await getMockSourceTrace(reportId));
    } catch {
      setError("Mock Source Trace 加载失败，请确认后端服务已启动。");
    } finally {
      setTraceLoading(false);
    }
  }

  async function submitCitation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setCitationLoading(true);
    setError("");
    try {
      setResolution(await resolveCitation(citationId));
    } catch {
      setError("Citation Resolver 加载失败，请确认后端服务已启动。");
    } finally {
      setCitationLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Source Refs"
          description="仅展示 mock/local 引用链，不读取真实材料，不调用真实 OCR、法律数据库或 LLM。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Refs Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="source_refs_enabled" value={String(status?.source_refs_enabled ?? true)} />
              <InfoRow label="citation_resolver_enabled" value={String(status?.citation_resolver_enabled ?? true)} />
              <InfoRow label="source_trace_enabled" value={String(status?.source_trace_enabled ?? true)} />
              <InfoRow label="mock_only" value={String(status?.mock_only ?? true)} />
              <InfoRow label="real_material_reading_enabled" value={String(status?.real_material_reading_enabled ?? false)} />
              <InfoRow label="real_ocr_connected" value={String(status?.real_ocr_connected ?? false)} />
              <InfoRow label="real_legal_search_connected" value={String(status?.real_legal_search_connected ?? false)} />
              <InfoRow label="notes" value={status?.notes ?? "Source refs mock trace foundation."} />
            </div>
          </CardBody>
        </Card>

        <div className="grid gap-6 lg:grid-cols-2">
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Mock Trace</h2>
              <form onSubmit={submitTrace} className="mt-4 space-y-4">
                <Field label="report_id" value={reportId} onChange={setReportId} />
                <Button type="submit" disabled={traceLoading}>
                  {traceLoading ? "加载中..." : "加载 Mock Trace"}
                </Button>
              </form>
              {trace ? (
                <div className="mt-5 space-y-4">
                  <InfoRow label="trace_id" value={trace.trace_id} />
                  <InfoRow label="mock_only" value={String(trace.mock_only)} />
                  <TraceList title="nodes" items={trace.nodes} />
                  <TraceList title="edges" items={trace.edges} />
                  <TraceList title="warnings" items={trace.warnings} />
                </div>
              ) : null}
            </CardBody>
          </Card>

          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Citation Resolver</h2>
              <form onSubmit={submitCitation} className="mt-4 space-y-4">
                <Field label="citation_id" value={citationId} onChange={setCitationId} />
                <Button type="submit" disabled={citationLoading}>
                  {citationLoading ? "解析中..." : "解析 Citation"}
                </Button>
              </form>
              {resolution ? (
                <div className="mt-5 space-y-4">
                  <InfoRow label="citation_id" value={resolution.citation_id} />
                  <InfoRow label="resolved" value={String(resolution.resolved)} />
                  <InfoRow label="mock_only" value={String(resolution.mock_only)} />
                  <TraceList title="source_ref" items={resolution.source_ref ? [resolution.source_ref] : []} />
                  <TraceList title="warnings" items={resolution.warnings} />
                </div>
              ) : null}
            </CardBody>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="block text-sm">
      <span className="text-muted">{label}</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
      />
    </label>
  );
}

function TraceList({ title, items }: { title: string; items: unknown[] }) {
  return (
    <div>
      <div className="text-xs font-semibold uppercase tracking-wide text-muted">{title}</div>
      {items.length > 0 ? (
        <pre className="mt-2 max-h-80 overflow-auto rounded-md border border-line bg-paper p-3 text-xs text-slate-700">
          {JSON.stringify(items, null, 2)}
        </pre>
      ) : (
        <div className="mt-2 rounded-md border border-line bg-paper p-3 text-sm text-muted">暂无引用溯源数据</div>
      )}
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
