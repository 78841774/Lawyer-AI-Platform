import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getLLMStatus } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function RuntimePage() {
  const { runtime, error } = await loadRuntime();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law Runtime"
          title="Runtime"
          description="LLM provider health, model configuration, and future operating metrics."
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-wide text-muted">LLM Status</div>
                <div className="mt-2 text-lg font-semibold text-ink">{runtime?.provider ?? "-"}</div>
              </div>
              <Badge tone={runtime?.configured ? "gold" : "muted"}>
                {runtime?.configured ? "configured" : "not configured"}
              </Badge>
            </div>
            <div className="mt-5 space-y-3">
              <InfoRow label="provider" value={runtime?.provider ?? "-"} />
              <InfoRow label="model" value={runtime?.model ?? "-"} />
              <InfoRow label="configured" value={formatBoolean(runtime?.configured)} />
              <InfoRow label="base_url_configured" value={formatBoolean(runtime?.base_url_configured)} />
              <InfoRow label="future token usage" value="Not available" />
              <InfoRow label="future latency" value="Not available" />
              <InfoRow label="future cost" value="Not available" />
              <InfoRow label="future error logs" value="Coming soon" />
            </div>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRuntime() {
  try {
    return { runtime: await getLLMStatus(), error: null };
  } catch {
    return { runtime: null, error: "Backend API is unavailable. Start the backend on port 8001." };
  }
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
