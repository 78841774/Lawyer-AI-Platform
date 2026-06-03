import { AppShell } from "@/components/AppShell";
import { CaseDetailClient } from "./CaseDetailClient";

export default function CaseDetailPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <CaseDetailClient caseId={params.caseId} />
    </AppShell>
  );
}
