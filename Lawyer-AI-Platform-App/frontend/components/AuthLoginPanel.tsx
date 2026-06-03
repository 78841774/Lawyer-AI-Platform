"use client";

import { useState } from "react";
import {
  ApiError,
  AuthStatus,
  clearAccessToken,
  getAuthStatus,
  loginWithDevToken,
  storeAccessToken
} from "@/services/api";

type PanelState = {
  status: AuthStatus | null;
  message: string;
  loading: boolean;
};

export function AuthLoginPanel() {
  const [state, setState] = useState<PanelState>({
    status: null,
    message: "",
    loading: false
  });

  async function handleLogin() {
    setState((current) => ({ ...current, loading: true, message: "Logging in..." }));
    try {
      const login = await loginWithDevToken();
      storeAccessToken(login.access_token);
      const status = await getAuthStatus();
      setState({
        status,
        message: `JWT expires at ${formatDate(login.expires_at)}`,
        loading: false
      });
    } catch (error) {
      setState({
        status: null,
        message: error instanceof ApiError ? error.message : "Login failed.",
        loading: false
      });
    }
  }

  async function handleClear() {
    clearAccessToken();
    setState({ status: null, message: "Local JWT cleared.", loading: false });
  }

  return (
    <section className="rounded-md border border-line bg-white p-4">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <div className="text-xs text-slate-500">Local Login</div>
          <div className="mt-2 text-sm font-semibold text-ink">
            {state.status ? state.status.auth_mode : "Dev Token Login"}
          </div>
          <div className="mt-1 text-xs text-slate-500">
            {state.status ? state.status.user_id : "user_local_001"}
          </div>
        </div>
        <div className="flex gap-2">
          <button
            type="button"
            onClick={handleLogin}
            disabled={state.loading}
            className="rounded-md bg-accent px-3 py-2 text-xs font-medium text-white disabled:opacity-60"
          >
            Local Login
          </button>
          <button
            type="button"
            onClick={handleClear}
            disabled={state.loading}
            className="rounded-md border border-line bg-white px-3 py-2 text-xs font-medium text-ink disabled:opacity-60"
          >
            Clear
          </button>
        </div>
      </div>
      {state.message ? (
        <div className="mt-3 rounded-md border border-line bg-paper px-3 py-2 text-xs text-slate-600">
          {state.message}
        </div>
      ) : null}
    </section>
  );
}

function formatDate(value: string) {
  return new Date(value).toLocaleString();
}
