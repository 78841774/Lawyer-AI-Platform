"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { createMockVersionedTrainingRun, VersionedSkillTrainingRun } from "@/services/api";

export function CreateMockTrainingRunButton({ packageId }: { packageId: string }) {
  const [run, setRun] = useState<VersionedSkillTrainingRun | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function createRun() {
    setLoading(true);
    setError(null);
    try {
      setRun(await createMockVersionedTrainingRun(packageId));
    } catch {
      setError("Mock training run 创建失败，请确认后端服务已启动。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <Button type="button" onClick={createRun} disabled={loading}>
        {loading ? "Creating..." : "Create Mock Training Run"}
      </Button>
      {error ? <div className="text-sm text-accent">{error}</div> : null}
      {run ? (
        <div className="rounded-md border border-line bg-slate-50 p-4 text-sm text-muted">
          <div className="font-medium text-ink">{run.run_id}</div>
          <div className="mt-2">LLM Called: {run.llm_called ? "是" : "否"} / Skill Published: {run.outputs.skill_registry_published ? "是" : "否"}</div>
          <Link
            href={`/versioned-training-runs/${encodeURIComponent(run.run_id)}`}
            className="mt-3 inline-flex rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink shadow-sm"
          >
            查看 mock run 详情
          </Link>
        </div>
      ) : null}
    </div>
  );
}
