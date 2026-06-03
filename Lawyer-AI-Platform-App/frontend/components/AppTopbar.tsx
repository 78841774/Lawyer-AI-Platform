"use client";

import { useEffect, useState } from "react";
import { authApi, runtimeApi, workspaceApi } from "@/services/api";
import type { AuthStatus, RuntimeStatus, Workspace } from "@/types";
import { Badge } from "@/components/ui/Badge";

type TopbarState = {
  auth: AuthStatus | null;
  runtime: RuntimeStatus | null;
  workspace: Workspace | null;
};

export function AppTopbar() {
  const [state, setState] = useState<TopbarState>({
    auth: null,
    runtime: null,
    workspace: null
  });

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        const [auth, runtime, workspaces] = await Promise.all([
          authApi.status(),
          runtimeApi.llmStatus(),
          workspaceApi.list()
        ]);
        if (active) {
          setState({ auth, runtime, workspace: workspaces[0] ?? null });
        }
      } catch {
        if (active) {
          setState({ auth: null, runtime: null, workspace: null });
        }
      }
    }
    void load();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="sticky top-0 z-10 hidden border-b border-line bg-white/95 px-6 py-3 backdrop-blur md:block">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-xs uppercase tracking-wide text-muted">当前工作空间</div>
          <div className="mt-1 text-sm font-semibold text-ink">
            {state.workspace?.name ?? "Local Demo Workspace"}
          </div>
        </div>
        <div className="flex flex-wrap items-center justify-end gap-2">
          <Badge tone="blue">{state.auth?.auth_mode ?? "认证检查中"}</Badge>
          <Badge tone={state.runtime?.configured ? "gold" : "muted"}>
            {state.runtime?.provider ?? "运行状态检查中"}
          </Badge>
          <Badge tone="muted">{state.auth?.user_id ?? "用户检查中"}</Badge>
        </div>
      </div>
    </div>
  );
}
