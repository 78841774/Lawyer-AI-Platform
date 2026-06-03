import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getCases } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function CaseListPage() {
  const { cases, error } = await loadCases();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law Cases"
          title="Case Workspace"
          description="Matter records with workspace ownership and legal AI workflow status."
          action={
            <Link
              href="/cases/new"
              className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white shadow-sm"
            >
              New Case
            </Link>
          }
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <div className="grid gap-3 border-b border-line bg-slate-50 px-4 py-3 text-xs font-semibold uppercase tracking-wide text-muted md:grid-cols-8">
            <span>Case ID</span>
            <span className="md:col-span-2">Title</span>
            <span>Status</span>
            <span>Workspace</span>
            <span>Owner</span>
            <span>Created</span>
            <span>Future</span>
          </div>
          {cases.length > 0 ? (
            cases.map((item) => (
              <Link
                key={item.case_id}
                href={`/cases/${item.case_id}`}
                className="grid gap-3 border-b border-line px-4 py-3 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-8"
              >
                <span className="break-words font-medium text-ink">{item.case_id}</span>
                <span className="break-words text-ink md:col-span-2">{item.title}</span>
                <span className="text-muted">{item.status}</span>
                <span className="break-words text-muted">{item.workspace_id}</span>
                <span className="break-words text-muted">{item.owner_user_id}</span>
                <span className="text-muted">{formatDate(item.created_at)}</span>
                <span className="flex flex-wrap gap-1">
                  <Badge tone="muted">priority</Badge>
                  <Badge tone="muted">stage</Badge>
                </span>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-muted">No cases found.</div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}

async function loadCases() {
  try {
    return { cases: await getCases(), error: null };
  } catch {
    return { cases: [], error: "Backend API is unavailable. Start the backend on port 8001." };
  }
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
