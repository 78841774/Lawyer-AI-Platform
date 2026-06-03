import { StatCard } from "@/components/StatCard";
import type { DashboardStats } from "@/types";

export function StatsGrid({ stats }: { stats: DashboardStats | null }) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
      <StatCard label="案件" value={formatCount(stats?.cases)} helper="当前工作空间案件" />
      <StatCard label="材料" value={formatCount(stats?.materials)} helper="已上传证据材料" />
      <StatCard label="事实" value={formatCount(stats?.facts)} helper="已提炼事实记录" />
      <StatCard label="法律分析" value={formatCount(stats?.analyses)} helper="法律分析运行记录" />
      <StatCard label="报告" value={formatCount(stats?.reports)} helper="已生成报告" />
    </section>
  );
}

function formatCount(value: number | undefined) {
  return typeof value === "number" ? String(value) : "-";
}
