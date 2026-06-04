import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import {
  getLegalSearchStatus,
  getLLMStatus,
  getLocalSandboxStatus,
  getOCRStatus,
  getSourceRefsStatus
} from "@/services/api";

export const dynamic = "force-dynamic";

export default async function RuntimePage() {
  const { runtime, ocr, legalSearch, sourceRefs, localSandbox, error } = await loadRuntime();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 运行状态"
          title="运行状态"
          description="运行状态用于确认模型、OCR、法律检索和 source refs foundation 的 mock / connected 边界。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <div className="grid gap-6 lg:grid-cols-5">
          <StatusCard
            title="模型状态"
            provider={runtime?.provider ?? "-"}
            connected={runtime?.configured ?? false}
            rows={[
              ["模型", runtime?.model ?? "-"],
              ["已配置", formatBoolean(runtime?.configured)],
              ["Base URL 已配置", formatBoolean(runtime?.base_url_configured)],
              ["llm_status", runtime?.configured ? "configured" : "not_configured"]
            ]}
          />
          <StatusCard
            title="OCR Adapter"
            provider={ocr?.provider ?? "mock_ocr"}
            connected={ocr?.connected ?? false}
            rows={[
              ["connected", formatBoolean(ocr?.connected)],
              ["mock_only", formatBoolean(ocr?.mock_only)],
              ["supports_pdf", formatBoolean(ocr?.supports_pdf)],
              ["supports_images", formatBoolean(ocr?.supports_images)],
              ["notes", ocr?.notes ?? "Real OCR provider not connected."]
            ]}
            actionHref="/ocr"
          />
          <StatusCard
            title="Legal Search Adapter"
            provider={legalSearch?.provider ?? "mock_legal_search"}
            connected={legalSearch?.connected ?? false}
            rows={[
              ["connected", formatBoolean(legalSearch?.connected)],
              ["mock_only", formatBoolean(legalSearch?.mock_only)],
              ["supports_case_law", formatBoolean(legalSearch?.supports_case_law)],
              ["supports_statutes", formatBoolean(legalSearch?.supports_statutes)],
              ["notes", legalSearch?.notes ?? "Real legal database not connected."]
            ]}
            actionHref="/legal-search"
          />
          <StatusCard
            title="Source Trace"
            provider="source_refs"
            connected={sourceRefs?.source_trace_enabled ?? false}
            rows={[
              ["source_refs_enabled", formatBoolean(sourceRefs?.source_refs_enabled)],
              ["citation_resolver_enabled", formatBoolean(sourceRefs?.citation_resolver_enabled)],
              ["source_trace_enabled", formatBoolean(sourceRefs?.source_trace_enabled)],
              ["mock_only", formatBoolean(sourceRefs?.mock_only)],
              ["real_material_reading_enabled", formatBoolean(sourceRefs?.real_material_reading_enabled)],
              ["real_ocr_connected", formatBoolean(sourceRefs?.real_ocr_connected)],
              ["real_legal_search_connected", formatBoolean(sourceRefs?.real_legal_search_connected)],
              ["notes", sourceRefs?.notes ?? "Source refs mock trace not loaded."]
            ]}
            actionHref="/source-refs"
          />
          <StatusCard
            title="Local Sandbox"
            provider={localSandbox?.mode ?? "local_only"}
            connected={localSandbox?.enabled ?? false}
            rows={[
              ["mode", localSandbox?.mode ?? "local_only"],
              ["real_case_processing_enabled", formatBoolean(localSandbox?.real_case_processing_enabled)],
              ["live_provider_enabled", formatBoolean(localSandbox?.live_provider_enabled)],
              ["deepseek_live_enabled", formatBoolean(localSandbox?.deepseek_live_enabled)],
              ["real_ocr_enabled", formatBoolean(localSandbox?.real_ocr_enabled)],
              ["real_legal_search_enabled", formatBoolean(localSandbox?.real_legal_search_enabled)],
              ["requires_manual_review", formatBoolean(localSandbox?.requires_manual_review)],
              ["mock_only", formatBoolean(localSandbox?.mock_only)]
            ]}
            actionHref="/local-sandbox"
          />
        </div>

        <Card>
          <CardBody>
            <h2 className="text-base font-semibold text-ink">Source Refs Foundation</h2>
            <div className="mt-4 space-y-3">
              <InfoRow label="source_ref_types" value="material / ocr / legal_search / skill_runtime / report / mock" />
              <InfoRow label="report.citations" value="prepared as optional array" />
              <InfoRow label="report.trace" value="prepared as optional object" />
              <InfoRow label="citation_summary" value="prepared as optional object" />
              <InfoRow label="citation_persistence" value="mock resolver only" />
            </div>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRuntime() {
  try {
    const [runtime, ocr, legalSearch, sourceRefs, localSandbox] = await Promise.all([
      getLLMStatus(),
      getOCRStatus(),
      getLegalSearchStatus(),
      getSourceRefsStatus(),
      getLocalSandboxStatus()
    ]);
    return { runtime, ocr, legalSearch, sourceRefs, localSandbox, error: null };
  } catch {
    return { runtime: null, ocr: null, legalSearch: null, sourceRefs: null, localSandbox: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function StatusCard({
  title,
  provider,
  connected,
  rows,
  actionHref
}: {
  title: string;
  provider: string;
  connected: boolean;
  rows: Array<[string, string]>;
  actionHref?: string;
}) {
  return (
    <Card>
      <CardBody>
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <div className="text-xs uppercase tracking-wide text-muted">{title}</div>
            <div className="mt-2 text-lg font-semibold text-ink">{provider}</div>
          </div>
          <Badge tone={connected ? "gold" : "muted"}>{connected ? "connected" : "not connected"}</Badge>
        </div>
        <div className="mt-5 space-y-3">
          {rows.map(([label, value]) => (
            <InfoRow key={label} label={label} value={value} />
          ))}
        </div>
        {actionHref ? (
          <Link href={actionHref} className="mt-5 inline-flex rounded-md border border-line bg-white px-3 py-2 text-sm text-ink">
            打开测试页
          </Link>
        ) : null}
      </CardBody>
    </Card>
  );
}

function formatBoolean(value: boolean | undefined) {
  if (typeof value !== "boolean") {
    return "-";
  }
  return value ? "true" : "false";
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
