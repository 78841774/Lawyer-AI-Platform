"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import {
  ExperiencePackageRecord,
  publishExperiencePackageToSkillRegistry,
  reviewExperiencePackage
} from "@/services/api";

export function ExperiencePackageActions({ packageRecord }: { packageRecord: ExperiencePackageRecord }) {
  const router = useRouter();
  const [item, setItem] = useState(packageRecord);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState("");
  const packageId = item.experience_package_id ?? item.package_id ?? "";
  const reviewStatus = item.review?.review_status ?? "暂无";
  const canPublish =
    reviewStatus === "approved" &&
    item.safety?.can_publish_to_skill_registry === true &&
    item.skill_registry_published !== true;

  async function review(status: string) {
    setLoading(status);
    setMessage("");
    try {
      const nextItem = await reviewExperiencePackage(packageId, status, "local_demo_user");
      setItem(nextItem);
      setMessage("审核状态已更新。审核通过只代表允许后续受控发布，不会自动发布 Skill。");
      router.refresh();
    } catch {
      setMessage("审核失败，请确认 Candidate 存在。");
    } finally {
      setLoading("");
    }
  }

  async function publish() {
    setLoading("publish");
    setMessage("");
    try {
      const skill = await publishExperiencePackageToSkillRegistry(packageId, "local_demo_workspace");
      router.push(`/skill-registry/${encodeURIComponent(skill.skill_id)}`);
    } catch {
      setMessage("受控发布失败，请确认已人工审核通过，且 Candidate 未发布过。");
    } finally {
      setLoading("");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        <Button type="button" onClick={() => review("approved")} disabled={loading !== ""}>
          {loading === "approved" ? "处理中..." : "审核通过"}
        </Button>
        <Button type="button" onClick={() => review("rejected")} disabled={loading !== ""} variant="secondary">
          驳回
        </Button>
        <Button type="button" onClick={() => review("needs_revision")} disabled={loading !== ""} variant="secondary">
          需要修改
        </Button>
      </div>
      <div className="text-sm text-muted">审核通过只代表允许后续受控发布，不会自动发布 Skill。</div>
      <div className="flex flex-wrap items-center gap-3">
        <Button type="button" onClick={publish} disabled={!canPublish || loading !== ""}>
          {loading === "publish" ? "发布中..." : "受控发布到 Skill Registry"}
        </Button>
        <span className="text-sm text-muted">
          需要人工审核通过。发布后不会自动启用 Workspace Runtime，仍需后续手动启用。
        </span>
      </div>
      {message ? <div className="text-sm text-muted">{message}</div> : null}
    </div>
  );
}
