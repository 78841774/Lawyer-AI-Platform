"use client";

import { useEffect, useState } from "react";
import {
  ApiError,
  AuthStatus,
  getAuthStatus,
  getCurrentUser,
  getWorkspace,
  getWorkspaces,
  loginLocal,
  logoutLocal,
  storeAccessToken
} from "@/services/api";
import type { User, Workspace } from "@/types";

type PanelState = {
  status: AuthStatus | null;
  user: User | null;
  workspace: Workspace | null;
  message: string;
  loading: boolean;
};

export function AuthLoginPanel() {
  const [state, setState] = useState<PanelState>({
    status: null,
    user: null,
    workspace: null,
    message: "",
    loading: false
  });

  useEffect(() => {
    void refreshStatus("");
  }, []);

  async function refreshStatus(message: string) {
    try {
      const [status, user, workspaces] = await Promise.all([
        getAuthStatus(),
        getCurrentUser(),
        getWorkspaces()
      ]);
      const workspaceSummary = workspaces[0] ?? null;
      const workspace = workspaceSummary ? await getWorkspace(workspaceSummary.workspace_id) : null;
      setState({ status, user, workspace, message, loading: false });
    } catch (error) {
      setState({
        status: null,
        user: null,
        workspace: null,
        message: error instanceof ApiError ? error.message : "认证状态暂不可用。",
        loading: false
      });
    }
  }

  async function handleLogin() {
    setState((current) => ({ ...current, loading: true, message: "正在登录..." }));
    try {
      const login = await loginLocal();
      storeAccessToken(login.access_token);
      await refreshStatus(`JWT 过期时间：${formatDate(login.expires_at)}`);
    } catch (error) {
      setState({
        status: null,
        user: null,
        workspace: null,
        message: error instanceof ApiError ? error.message : "登录失败。",
        loading: false
      });
    }
  }

  async function handleClear() {
    logoutLocal();
    setState((current) => ({ ...current, loading: true, message: "正在退出登录..." }));
    await refreshStatus("本地 JWT 已清除。");
  }

  return (
    <section className="rounded-md border border-line bg-white p-5 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-xs uppercase tracking-wide text-muted">认证状态</div>
          <div className="mt-2 text-lg font-semibold text-ink">
            {state.status ? formatAuthMode(state.status.auth_mode) : "检查中"}
          </div>
          <div className="mt-1 text-sm text-muted">
            当前用户：{state.user?.display_name ?? state.status?.user_id ?? "user_local_001"}
          </div>
          <div className="mt-1 text-xs text-muted">
            当前工作空间：{state.workspace?.name ?? state.workspace?.workspace_id ?? "workspace_local_001"}
          </div>
          <div className="mt-1 text-xs text-muted">
            {state.status?.expires_at ? `过期时间 ${formatDate(state.status.expires_at)}` : "本地模式仍可使用 local_fallback。"}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={handleLogin}
            disabled={state.loading}
            className="rounded-md bg-accent px-3 py-2 text-xs font-medium text-white disabled:opacity-60"
          >
            本地登录
          </button>
          <button
            type="button"
            onClick={() => refreshStatus("已刷新认证状态。")}
            disabled={state.loading}
            className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink disabled:opacity-60"
          >
            刷新
          </button>
          <button
            type="button"
            onClick={handleClear}
            disabled={state.loading}
            className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink disabled:opacity-60"
          >
            退出登录
          </button>
        </div>
      </div>
      {state.message ? (
        <div className="mt-3 rounded-md border border-line bg-paper px-3 py-2 text-xs text-muted">
          {state.message}
        </div>
      ) : null}
    </section>
  );
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}

function formatAuthMode(mode: AuthStatus["auth_mode"]) {
  if (mode === "jwt") {
    return "JWT";
  }
  if (mode === "local_fallback") {
    return "local";
  }
  return mode;
}
