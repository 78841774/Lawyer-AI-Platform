"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  getLegalSearchStatus,
  LegalSearchProviderStatus,
  LegalSearchResult,
  mockLegalSearch
} from "@/services/api";

export default function LegalSearchPage() {
  const [status, setStatus] = useState<LegalSearchProviderStatus | null>(null);
  const [result, setResult] = useState<LegalSearchResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    query: "payment dispute burden of proof",
    case_cause_code: "payment_dispute",
    jurisdiction: "CN"
  });

  useEffect(() => {
    getLegalSearchStatus().then(setStatus).catch(() => setError("Legal Search status 暂不可用，请确认后端服务已启动。"));
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      setResult(await mockLegalSearch(form));
    } catch {
      setError("Mock Legal Search 失败，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="Legal Search Adapter"
          description="仅 Mock Legal Search，不连接真实法律数据库，不抓取真实裁判文书。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Adapter Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="provider" value={status?.provider ?? "mock_legal_search"} />
              <InfoRow label="connected" value={String(status?.connected ?? false)} />
              <InfoRow label="mock_only" value={String(status?.mock_only ?? true)} />
              <InfoRow label="supports_case_law" value={String(status?.supports_case_law ?? true)} />
              <InfoRow label="supports_statutes" value={String(status?.supports_statutes ?? true)} />
              <InfoRow label="notes" value={status?.notes ?? "Real legal database not connected."} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Mock Search</h2>
            <form onSubmit={submit} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="query" value={form.query} onChange={(value) => setForm({ ...form, query: value })} />
              <Field label="case_cause_code" value={form.case_cause_code} onChange={(value) => setForm({ ...form, case_cause_code: value })} />
              <Field label="jurisdiction" value={form.jurisdiction} onChange={(value) => setForm({ ...form, jurisdiction: value })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading}>{loading ? "检索中..." : "运行 Mock Legal Search"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        {result ? (
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Mock Legal Search Result</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <InfoRow label="search_run_id" value={result.search_run_id} />
                <InfoRow label="status" value={result.status} />
                <InfoRow label="provider" value={result.provider} />
                <InfoRow label="provider_mode" value={result.provider_mode} />
              </div>
              <div className="mt-5 grid gap-3 md:grid-cols-2">
                {result.hits.map((hit) => (
                  <div key={hit.hit_id} className="rounded-md border border-line bg-paper p-3">
                    <div className="text-xs font-semibold uppercase tracking-wide text-muted">source ref</div>
                    <div className="mt-3 space-y-2">
                      <InfoRow label="source_ref_id" value={hit.source_ref.source_ref_id} />
                      <InfoRow label="citation" value={hit.source_ref.citation} />
                      <InfoRow label="source_type" value={hit.source_ref.source_type} />
                      <InfoRow label="quote" value={hit.source_ref.quote} />
                      <InfoRow label="provider" value={hit.source_ref.provider} />
                      <InfoRow label="provider_mode" value={hit.source_ref.provider_mode} />
                      <InfoRow label="mock_only" value={String(hit.source_ref.mock_only)} />
                    </div>
                  </div>
                ))}
              </div>
              <pre className="mt-4 overflow-auto rounded-md border border-line bg-paper p-4 text-xs text-slate-700">
                {JSON.stringify({ hits: result.hits, source_refs: result.hits.map((hit) => hit.source_ref), warnings: result.warnings }, null, 2)}
              </pre>
            </CardBody>
          </Card>
        ) : null}
      </div>
    </AppShell>
  );
}

function Field({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) {
  return (
    <label className="text-sm">
      <span className="text-muted">{label}</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="mt-2 w-full rounded-md border border-line bg-white px-3 py-2 text-ink"
      />
    </label>
  );
}

function StatusMessage({ message }: { message: string }) {
  return <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">{message}</div>;
}
