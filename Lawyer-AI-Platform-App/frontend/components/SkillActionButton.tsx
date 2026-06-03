"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import {
  buildExperiencePackage,
  deprecateSkillInRegistry,
  evaluateSkill,
  publishSkillToRegistry
} from "@/services/api";

type SkillAction = "evaluate" | "build-package" | "publish" | "deprecate";

const actionConfig: Record<SkillAction, { label: string; run: (skillId: string) => Promise<unknown> }> = {
  evaluate: {
    label: "评估",
    run: evaluateSkill
  },
  "build-package": {
    label: "构建经验包",
    run: buildExperiencePackage
  },
  publish: {
    label: "发布",
    run: publishSkillToRegistry
  },
  deprecate: {
    label: "废弃",
    run: deprecateSkillInRegistry
  }
};

export function SkillActionButton({
  skillId,
  action,
  variant = "secondary"
}: {
  skillId: string;
  action: SkillAction;
  variant?: "primary" | "secondary";
}) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const config = actionConfig[action];

  async function handleClick() {
    setLoading(true);
    setMessage("");
    try {
      await config.run(skillId);
      setMessage("已完成");
      router.refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "操作失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="inline-flex flex-col gap-1">
      <Button onClick={handleClick} disabled={loading} variant={variant} className="text-xs">
        {loading ? "处理中..." : config.label}
      </Button>
      {message ? <span className="max-w-36 text-xs text-muted">{message}</span> : null}
    </div>
  );
}
