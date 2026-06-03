import { AppShell } from "@/components/AppShell";

export default function MaterialUploadPage({ params }: { params: { caseId: string } }) {
  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">上传材料</h1>
          <p className="mt-2 text-sm text-slate-600">为 {params.caseId} 上传并解析案件材料。</p>
        </header>
        <section className="rounded-md border border-dashed border-line bg-white p-8">
          <div className="text-sm font-medium text-ink">上传区域</div>
          <p className="mt-2 text-sm text-slate-600">
            PDF、Word、图片与文本上传后续将接入 Material Service。
          </p>
        </section>
      </div>
    </AppShell>
  );
}
