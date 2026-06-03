"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { AppShell } from "@/components/AppShell";
import { ApiError, createCase } from "@/services/api";

export default function NewCasePage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");
  const [message, setMessage] = useState("");

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const resolvedTitle = title.trim();
    if (!resolvedTitle) {
      setStatus("error");
      setMessage("Please enter a case title.");
      return;
    }

    setStatus("loading");
    setMessage("Creating case...");
    try {
      const newCase = await createCase(resolvedTitle);
      setMessage("Case created.");
      router.push(`/cases/${newCase.case_id}`);
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof ApiError ? error.message : "Failed to create case.");
    }
  }

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Create Case</h1>
          <p className="mt-2 text-sm text-slate-600">Start a new demo case in the workspace.</p>
        </header>

        <form onSubmit={handleSubmit} className="rounded-md border border-line bg-white p-5">
          <label htmlFor="title" className="text-sm font-medium text-ink">
            Case title
          </label>
          <input
            id="title"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            className="mt-2 w-full rounded-md border border-line px-3 py-2 text-sm outline-none focus:border-accent"
            placeholder="例如：演示合同纠纷案件"
          />
          <button
            type="submit"
            disabled={status === "loading"}
            className="mt-4 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
          >
            {status === "loading" ? "Creating..." : "Create Case"}
          </button>
          {message ? (
            <div className="mt-4 rounded-md border border-line bg-paper px-3 py-2 text-sm text-slate-600">
              {message}
            </div>
          ) : null}
        </form>
      </div>
    </AppShell>
  );
}
