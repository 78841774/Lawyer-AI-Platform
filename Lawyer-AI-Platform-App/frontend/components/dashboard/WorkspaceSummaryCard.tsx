import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import type { Workspace } from "@/types";

export function WorkspaceSummaryCard({
  workspace,
  activeCases
}: {
  workspace: Workspace | null;
  activeCases: number;
}) {
  return (
    <Card>
      <CardBody>
        <div className="text-xs uppercase tracking-wide text-muted">工作空间概览</div>
        <div className="mt-2 text-lg font-semibold text-ink">{workspace?.name ?? "-"}</div>
        <div className="mt-4 space-y-3">
          <InfoRow label="工作空间 ID" value={workspace?.workspace_id ?? "workspace_local_001"} />
          <InfoRow label="所有人 ID" value={workspace?.owner_user_id ?? "-"} />
          <InfoRow label="状态" value={workspace?.status ?? "-"} />
          <InfoRow label="活跃案件" value={String(activeCases)} />
        </div>
      </CardBody>
    </Card>
  );
}
