"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { deprecateSkillInRegistry, rollbackSkillInRegistry } from "@/services/api";

export function SkillRegistryActions({ skillId }: { skillId: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState("");
  const [message, setMessage] = useState("");

  async function run(action: "deprecate" | "rollback") {
    setLoading(action);
    setMessage("");
    try {
      if (action === "deprecate") {
        await deprecateSkillInRegistry(skillId, "local validation test");
      } else {
        await rollbackSkillInRegistry(skillId, "local rollback test");
      }
      setMessage("状态已更新，历史记录已保留。");
      router.refresh();
    } catch {
      setMessage("操作失败，请确认该 Skill Registry 记录存在。");
    } finally {
      setLoading("");
    }
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        <Button type="button" onClick={() => run("deprecate")} disabled={loading !== ""} variant="secondary">
          {loading === "deprecate" ? "处理中..." : "Deprecate"}
        </Button>
        <Button type="button" onClick={() => run("rollback")} disabled={loading !== ""} variant="secondary">
          {loading === "rollback" ? "处理中..." : "Rollback"}
        </Button>
      </div>
      <div className="text-sm text-muted">Deprecate / Rollback 不删除历史记录，只改变状态或追加事件。</div>
      {message ? <div className="text-sm text-muted">{message}</div> : null}
    </div>
  );
}
