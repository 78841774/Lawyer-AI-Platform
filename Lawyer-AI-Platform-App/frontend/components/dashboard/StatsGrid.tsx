import { StatCard } from "@/components/StatCard";
import type { DashboardStats } from "@/types";

export function StatsGrid({ stats }: { stats: DashboardStats | null }) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      <StatCard label="Cases" value={formatCount(stats?.cases)} helper="Active workspace cases" />
      <StatCard label="Materials" value={formatCount(stats?.materials)} helper="Uploaded evidence files" />
      <StatCard label="Facts" value={formatCount(stats?.facts)} helper="Extracted fact records" />
      <StatCard label="Analyses" value={formatCount(stats?.analyses)} helper="Legal analysis runs" />
      <StatCard label="Reports" value={formatCount(stats?.reports)} helper="Generated reports" />
    </section>
  );
}

function formatCount(value: number | undefined) {
  return typeof value === "number" ? String(value) : "-";
}
