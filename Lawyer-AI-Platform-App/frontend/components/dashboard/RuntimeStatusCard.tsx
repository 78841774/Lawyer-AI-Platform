import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import type { RuntimeStatus } from "@/types";

export function RuntimeStatusCard({ runtime }: { runtime: RuntimeStatus | null }) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">运行状态</div>
        <div className="mt-2 text-lg font-semibold text-ink">{runtime?.provider ?? "-"}</div>
        <div className="mt-4 space-y-3">
          <InfoRow label="模型" value={runtime?.model ?? "-"} />
          <InfoRow label="已配置" value={formatBoolean(runtime?.configured)} />
          <InfoRow label="Base URL 已配置" value={formatBoolean(runtime?.base_url_configured)} />
          <InfoRow label="未来延迟指标" value="暂不可用" />
        </div>
      </CardBody>
    </Card>
  );
}

function formatBoolean(value: boolean | undefined) {
  if (typeof value !== "boolean") {
    return "-";
  }
  return value ? "是" : "否";
}
