import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { getCases } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function CaseListPage() {
  const { cases, error } = await loadCases();

  return (
    <AppShell>
      <div className="space-y-6">
        <header className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-ink">Case List</h1>
            <p className="mt-2 text-sm text-slate-600">All cases returned by the Workspace API.</p>
          </div>
          <Link
            href="/cases/new"
            className="rounded-md bg-accent px-4 py-2 text-sm font-medium text-white"
          >
            New Case
          </Link>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        <section className="rounded-md border border-line bg-white">
          {cases.length > 0 ? (
            cases.map((item) => (
              <Link
                key={item.case_id}
                href={`/cases/${item.case_id}`}
                className="grid gap-3 border-b border-line px-4 py-3 text-sm last:border-b-0 md:grid-cols-4"
              >
                <span className="font-medium text-ink">{item.title}</span>
                <span className="text-slate-600">{item.case_type}</span>
                <span className="text-slate-600">{item.status}</span>
                <span className="text-slate-500">{formatDate(item.updated_at)}</span>
              </Link>
            ))
          ) : (
            <div className="p-5 text-sm text-slate-600">No cases found.</div>
          )}
        </section>
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
    <div className="rounded-md border border-line bg-white p-4 text-sm text-slate-600">
      {message}
    </div>
  );
}
