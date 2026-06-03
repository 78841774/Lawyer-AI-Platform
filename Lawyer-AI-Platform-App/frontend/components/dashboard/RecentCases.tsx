import Link from "next/link";
import { Card, CardBody } from "@/components/ui/Card";
import type { Case } from "@/types";

export function RecentCases({ cases }: { cases: Case[] }) {
  return (
    <Card>
      <CardBody>
        <div className="flex items-center justify-between gap-4">
          <h2 className="text-sm font-semibold text-ink">Recent Cases</h2>
          <Link href="/cases" className="text-sm font-medium text-accent">
            View all
          </Link>
        </div>
        <div className="mt-4 space-y-3">
          {cases.slice(-4).reverse().map((item) => (
            <Link key={item.case_id} href={`/cases/${item.case_id}`} className="block rounded-md border border-line p-3 hover:bg-slate-50">
              <div className="text-sm font-medium text-ink">{item.title}</div>
              <div className="mt-1 text-xs text-muted">
                {item.case_id} · {item.status} · {item.workspace_id}
              </div>
            </Link>
          ))}
          {cases.length === 0 ? <div className="text-sm text-muted">No cases found.</div> : null}
        </div>
      </CardBody>
    </Card>
  );
}
