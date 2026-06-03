import Link from "next/link";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export function QuickActions() {
  return (
    <Card>
      <CardBody>
        <h2 className="text-sm font-semibold text-ink">Quick Actions</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <ActionLink href="/cases/new" label="Create case" helper="Start a legal workspace record" />
          <ActionLink href="/runtime" label="Check runtime" helper="Inspect provider and model status" />
          <ActionLink href="/skills" label="Review skills" helper="Open published legal skills" />
          <div className="rounded-md border border-line p-3">
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm font-medium text-ink">Invite members</div>
              <Badge tone="muted">Soon</Badge>
            </div>
            <div className="mt-1 text-xs text-muted">Reserved for workspace membership.</div>
          </div>
        </div>
      </CardBody>
    </Card>
  );
}

function ActionLink({
  href,
  label,
  helper
}: {
  href: string;
  label: string;
  helper: string;
}) {
  return (
    <Link href={href} className="rounded-md border border-line p-3 hover:bg-slate-50">
      <div className="text-sm font-medium text-ink">{label}</div>
      <div className="mt-1 text-xs text-muted">{helper}</div>
    </Link>
  );
}
