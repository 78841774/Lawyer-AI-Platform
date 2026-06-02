import { AppShell } from "@/components/AppShell";

export default function MaterialUploadPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Material Upload</h1>
          <p className="mt-2 text-sm text-slate-600">Upload and parse materials for {params.caseId}.</p>
        </header>
        <section className="rounded-md border border-dashed border-line bg-white p-8">
          <div className="text-sm font-medium text-ink">Upload Area</div>
          <p className="mt-2 text-sm text-slate-600">
            PDF, Word, image, and text uploads will connect to Material Service.
          </p>
        </section>
      </div>
    </AppShell>
  );
}
