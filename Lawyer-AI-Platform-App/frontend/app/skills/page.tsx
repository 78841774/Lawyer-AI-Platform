import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { getWorkspaceSkills, WorkspaceSkillRecord } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const { skills, error } = await loadSkills();

  return (
    <AppShell>
      <div className="space-y-6">
        <header>
          <h1 className="text-2xl font-semibold text-ink">Workspace Skills</h1>
          <p className="mt-2 text-sm text-slate-600">
            Published skills available for case workspaces.
          </p>
        </header>

        {error ? <StatusMessage message={error} /> : null}

        <section className="rounded-md border border-line bg-white">
          {skills.length > 0 ? (
            skills.map((skill) => <SkillRow key={skill.skill_id} skill={skill} />)
          ) : (
            <div className="p-5 text-sm text-slate-600">
              No published skills are available. Publish a validated skill from the Skill Registry first.
            </div>
          )}
        </section>
      </div>
    </AppShell>
  );
}

async function loadSkills() {
  try {
    return { skills: await getWorkspaceSkills(), error: null };
  } catch {
    return { skills: [], error: "Backend API is unavailable. Start the backend on port 8001." };
  }
}

function SkillRow({ skill }: { skill: WorkspaceSkillRecord }) {
  return (
    <article className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 md:grid-cols-5">
      <div className="md:col-span-2">
        <div className="font-medium text-ink">{skill.skill_name}</div>
        <div className="mt-1 text-xs text-slate-500">{skill.skill_id}</div>
      </div>
      <div className="text-slate-600">{skill.domain}</div>
      <div className="text-slate-600">v{skill.version}</div>
      <div className="text-slate-600">
        <div>{skill.status}</div>
        <div className="mt-1 text-xs text-slate-500">{skill.package_id}</div>
      </div>
      <Link
        href={`/cases`}
        className="rounded-md border border-line px-3 py-2 text-center text-xs font-medium text-ink hover:border-accent"
      >
        Apply in Case
      </Link>
    </article>
  );
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-slate-600">
      {message}
    </div>
  );
}
