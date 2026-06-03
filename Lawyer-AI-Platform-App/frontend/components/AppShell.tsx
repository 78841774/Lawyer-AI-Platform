import Link from "next/link";
import { AppTopbar } from "@/components/AppTopbar";
import { Badge } from "@/components/ui/Badge";

const navGroups = [
  {
    label: "主导航",
    items: [
      { href: "/", label: "工作台" },
      { href: "/cases", label: "案件" },
      { href: "/reports", label: "报告" }
    ]
  },
  {
    label: "智能能力",
    items: [
      { href: "/skills", label: "技能" },
      { href: "#experience-packages", label: "经验包", disabled: true },
      { href: "/runtime", label: "运行状态" }
    ]
  },
  {
    label: "工作空间",
    items: [
      { href: "/workspaces", label: "工作空间" },
      { href: "#users", label: "用户", disabled: true },
      { href: "#audit-logs", label: "审计日志", disabled: true }
    ]
  },
  {
    label: "系统",
    items: [{ href: "#settings", label: "设置", disabled: true }]
  }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-paper">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-800 bg-navy px-5 py-6 text-white md:block">
        <div className="border-b border-slate-800 pb-5">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-md border border-gold bg-surface text-sm font-semibold text-gold">
              AI
            </div>
            <div>
              <div className="text-lg font-semibold tracking-wide">AIHome.law</div>
              <div className="mt-1 text-xs text-slate-400">法律 AI 工作空间</div>
            </div>
          </div>
        </div>
        <nav className="mt-6 space-y-6">
          {navGroups.map((group) => (
            <div key={group.label}>
              <div className="px-3 text-xs uppercase tracking-wide text-slate-500">{group.label}</div>
              <div className="mt-2 space-y-1">
                {group.items.map((item) =>
                  item.disabled ? (
                    <div
                      key={item.href}
                      className="flex items-center justify-between rounded-md px-3 py-2 text-sm text-slate-500"
                    >
                      <span>{item.label}</span>
                      <span className="text-[10px] uppercase tracking-wide">即将推出</span>
                    </div>
                  ) : (
                    <Link
                      key={item.href}
                      href={item.href}
                      className="block rounded-md px-3 py-2 text-sm text-slate-300 hover:bg-surface hover:text-white"
                    >
                      {item.label}
                    </Link>
                  )
                )}
              </div>
            </div>
          ))}
        </nav>
        <div className="absolute bottom-6 left-5 right-5 rounded-md border border-slate-800 bg-surface p-4">
          <div className="text-xs uppercase tracking-wide text-gold">内测版本</div>
          <div className="mt-2 text-xs leading-5 text-slate-400">
            面向案件、报告与可复用技能的法律 AI 工作空间基础。
          </div>
        </div>
      </aside>
      <section className="md:pl-72">
        <AppTopbar />
        <div className="border-b border-line bg-white px-5 py-4 md:hidden">
          <div className="text-base font-semibold text-ink">AIHome.law</div>
          <div className="mt-1 text-xs text-muted">法律 AI 工作空间</div>
          <nav className="mt-4 flex gap-2 overflow-x-auto text-sm text-muted">
            {navGroups.flatMap((group) =>
              group.items
                .filter((item) => !item.disabled)
                .map((item) => (
                  <Link key={item.href} href={item.href} className="rounded-md border border-line px-3 py-2">
                    {item.label}
                  </Link>
                ))
            )}
          </nav>
          <div className="mt-3">
            <Badge tone="gold">AIHome.law 内测版本</Badge>
          </div>
        </div>
        <div className="mx-auto max-w-7xl px-5 py-8">{children}</div>
      </section>
    </main>
  );
}
