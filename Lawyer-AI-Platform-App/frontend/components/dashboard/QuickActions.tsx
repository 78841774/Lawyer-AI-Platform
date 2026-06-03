import Link from "next/link";
import { Card, CardBody } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";

export function QuickActions() {
  return (
    <Card>
      <CardBody>
        <h2 className="text-sm font-semibold text-ink">快捷操作</h2>
        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <ActionLink href="/cases/new" label="创建案件" helper="创建新的法律 AI 工作记录" />
          <ActionLink href="/runtime" label="查看运行状态" helper="检查提供方与模型配置" />
          <ActionLink href="/skills" label="查看技能" helper="打开已发布法律技能" />
          <div className="rounded-md border border-line p-3">
            <div className="flex items-center justify-between gap-2">
              <div className="text-sm font-medium text-ink">邀请成员</div>
              <Badge tone="muted">即将推出</Badge>
            </div>
            <div className="mt-1 text-xs text-muted">预留给工作空间成员管理。</div>
          </div>
        </div>
      </CardBody>
    </Card>
  );
}

function ActionLink({
  href,
  label,
  helper
}: {
  href: string;
  label: string;
  helper: string;
}) {
  return (
    <Link href={href} className="rounded-md border border-line p-3 hover:bg-slate-50">
      <div className="text-sm font-medium text-ink">{label}</div>
      <div className="mt-1 text-xs text-muted">{helper}</div>
    </Link>
  );
}
