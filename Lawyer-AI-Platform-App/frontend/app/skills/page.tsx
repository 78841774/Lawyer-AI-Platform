import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card } from "@/components/ui/Card";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getWorkspaceSkills, WorkspaceSkillRecord } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function SkillsPage() {
  const { skills, error } = await loadSkills();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law Skills"
          title="Published Skills"
          description="Reusable legal skills available for case workspaces."
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          {skills.length > 0 ? (
            skills.map((skill) => <SkillRow key={skill.skill_id} skill={skill} />)
          ) : (
            <div className="p-5 text-sm text-muted">
              No published skills are available. Publish a validated skill from the Skill Registry first.
            </div>
          )}
        </Card>
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
    <article
      id={skill.skill_id}
      className="grid gap-3 border-b border-line px-4 py-4 text-sm last:border-b-0 hover:bg-slate-50 md:grid-cols-6"
    >
      <div className="md:col-span-2">
        <Link href={`/skills#${skill.skill_id}`} className="font-medium text-ink hover:text-accent">
          {skill.skill_name}
        </Link>
        <div className="mt-1 text-xs text-muted">{skill.skill_id}</div>
      </div>
      <Meta label="Domain" value={skill.domain} />
      <Meta label="Version" value={`v${skill.version}`} />
      <Meta label="Package" value={skill.package_id} />
      <div>
        <div className="text-xs text-muted">Status</div>
        <div className="mt-1">
          <Badge tone="gold">{skill.status}</Badge>
        </div>
      </div>
    </article>
  );
}

function Meta({ label, value }: { label: string; value: string }) {
  return (
    <div className="text-muted">
      <div className="text-xs text-muted">{label}</div>
      <div>{value}</div>
    </div>
  );
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
