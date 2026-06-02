import Link from "next/link";
import { AppShell } from "@/components/AppShell";

export default function CaseDetailPage({ params }: { params: { caseId: string } }) {
  const links = [
    { href: `/cases/${params.caseId}/materials`, label: "Material Upload" },
    { href: `/cases/${params.caseId}/facts`, label: "Fact View" },
    { href: `/cases/${params.caseId}/legal`, label: "Legal Analysis View" },
    { href: `/cases/${params.caseId}/reports`, label: "Report View" }
  ];

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Case Detail</h1>
          <p className="mt-2 text-sm text-slate-600">Case ID: {params.caseId}</p>
        </header>
        <section className="grid gap-4 md:grid-cols-2">
          {links.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="rounded-md border border-line bg-white p-4 text-sm font-medium text-ink hover:border-accent"
            >
              {item.label}
            </Link>
          ))}
        </section>
      </div>
    </AppShell>
  );
}
