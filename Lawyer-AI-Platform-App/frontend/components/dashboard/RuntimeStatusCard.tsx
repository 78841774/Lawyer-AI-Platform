import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import type { RuntimeStatus } from "@/types";

export function RuntimeStatusCard({ runtime }: { runtime: RuntimeStatus | null }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">Runtime Status</div>
        <div className="mt-2 text-lg font-semibold text-ink">{runtime?.provider ?? "-"}</div>
        <div className="mt-4 space-y-3">
          <InfoRow label="Model" value={runtime?.model ?? "-"} />
          <InfoRow label="Configured" value={formatBoolean(runtime?.configured)} />
          <InfoRow label="Base URL configured" value={formatBoolean(runtime?.base_url_configured)} />
          <InfoRow label="Future latency" value="Not available" />
        </div>
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
