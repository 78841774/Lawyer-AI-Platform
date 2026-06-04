"use client";

import { FormEvent, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getOCRStatus, mockOCRExtract, OCRProviderStatus, OCRResult } from "@/services/api";

export default function OCRPage() {
  const [status, setStatus] = useState<OCRProviderStatus | null>(null);
  const [result, setResult] = useState<OCRResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    material_id: "material_demo_001",
    filename: "demo.pdf",
    relative_path: "demo/demo.pdf"
  });

  useEffect(() => {
    getOCRStatus().then(setStatus).catch(() => setError("OCR status 暂不可用，请确认后端服务已启动。"));
  }, []);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      setResult(await mockOCRExtract(form));
    } catch {
      setError("Mock OCR 提取失败，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="Runtime Tools"
          title="OCR Adapter"
          description="仅 Mock OCR，不读取真实文件，不调用真实 OCR 服务。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Adapter Status</h2>
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              <InfoRow label="provider" value={status?.provider ?? "mock_ocr"} />
              <InfoRow label="connected" value={String(status?.connected ?? false)} />
              <InfoRow label="mock_only" value={String(status?.mock_only ?? true)} />
              <InfoRow label="supports_pdf" value={String(status?.supports_pdf ?? true)} />
              <InfoRow label="supports_images" value={String(status?.supports_images ?? true)} />
              <InfoRow label="notes" value={status?.notes ?? "Real OCR provider not connected."} />
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Mock Extract</h2>
            <form onSubmit={submit} className="mt-4 grid gap-4 md:grid-cols-3">
              <Field label="material_id" value={form.material_id} onChange={(value) => setForm({ ...form, material_id: value })} />
              <Field label="filename" value={form.filename} onChange={(value) => setForm({ ...form, filename: value })} />
              <Field label="relative_path" value={form.relative_path} onChange={(value) => setForm({ ...form, relative_path: value })} />
              <div className="md:col-span-3">
                <Button type="submit" disabled={loading}>{loading ? "处理中..." : "运行 Mock OCR"}</Button>
              </div>
            </form>
          </CardBody>
        </Card>

        {result ? (
          <Card>
            <CardBody>
              <h2 className="text-base font-semibold text-ink">Mock OCR Result</h2>
              <div className="mt-4 grid gap-3 md:grid-cols-2">
                <InfoRow label="ocr_run_id" value={result.ocr_run_id} />
                <InfoRow label="status" value={result.status} />
                <InfoRow label="provider" value={result.provider} />
                <InfoRow label="provider_mode" value={result.provider_mode} />
              </div>
              <pre className="mt-4 overflow-auto rounded-md border border-line bg-paper p-4 text-xs text-slate-700">
                {JSON.stringify({ pages: result.pages, source_refs: result.source_refs, warnings: result.warnings }, null, 2)}
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
