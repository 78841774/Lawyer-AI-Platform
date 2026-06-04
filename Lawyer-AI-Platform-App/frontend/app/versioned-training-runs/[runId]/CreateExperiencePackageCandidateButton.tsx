"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { createExperiencePackageCandidate, ExperiencePackageRecord } from "@/services/api";

export function CreateExperiencePackageCandidateButton({ runId }: { runId: string }) {
  const router = useRouter();
  const [candidate, setCandidate] = useState<ExperiencePackageRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function createCandidate() {
    setLoading(true);
    setError(null);
    try {
      const nextCandidate = await createExperiencePackageCandidate(runId);
      setCandidate(nextCandidate);
      const candidateId = nextCandidate.experience_package_id ?? nextCandidate.package_id;
      if (candidateId) {
        router.push(`/experience-packages/${encodeURIComponent(candidateId)}`);
      }
    } catch {
      setError("Experience Package Candidate 生成失败，请确认 mock training run 已完成。");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-3">
      <Button type="button" onClick={createCandidate} disabled={loading}>
        {loading ? "生成中..." : "生成 Experience Package Candidate"}
      </Button>
      <div className="text-sm text-muted">仅生成 Candidate，不发布 Skill Registry，不调用 LLM，不使用真实案件材料。</div>
      {error ? <div className="text-sm text-accent">{error}</div> : null}
      {candidate ? (
        <Link
          href={`/experience-packages/${encodeURIComponent(candidate.experience_package_id ?? candidate.package_id ?? "")}`}
          className="inline-flex rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink shadow-sm"
        >
          查看 Candidate
        </Link>
      ) : null}
    </div>
  );
}
