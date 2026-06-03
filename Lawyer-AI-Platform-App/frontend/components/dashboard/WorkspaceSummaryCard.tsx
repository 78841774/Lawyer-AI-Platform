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
        <div className="text-xs uppercase tracking-wide text-muted">Current Workspace</div>
        <div className="mt-2 text-lg font-semibold text-ink">{workspace?.name ?? "-"}</div>
        <div className="mt-4 space-y-3">
          <InfoRow label="Workspace" value={workspace?.workspace_id ?? "workspace_local_001"} />
          <InfoRow label="Owner" value={workspace?.owner_user_id ?? "-"} />
          <InfoRow label="Status" value={workspace?.status ?? "-"} />
          <InfoRow label="Active cases" value={String(activeCases)} />
        </div>
      </CardBody>
    </Card>
  );
}
