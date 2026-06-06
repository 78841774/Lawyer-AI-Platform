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
      { href: "/experience-packages", label: "经验包" },
      { href: "/versioned-training-packages", label: "版本化训练包" },
      { href: "/versioned-training-runs", label: "训练运行" },
      { href: "/skill-registry", label: "技能注册表" },
      { href: "/runtime", label: "运行状态" },
      { href: "/ocr", label: "OCR" },
      { href: "/legal-search", label: "Legal Search" },
      { href: "/source-refs", label: "Source Refs" },
      { href: "/local-sandbox", label: "Local Sandbox" },
      { href: "/internal-alpha", label: "Internal Alpha" },
      { href: "/personal-alpha", label: "Personal Alpha" },
      { href: "/personal-alpha-workspace", label: "Personal Alpha Workspace" },
      { href: "/personal-alpha-dashboard", label: "Personal Alpha Dashboard" },
      { href: "/personal-alpha-source-review", label: "Personal Alpha Source Review" },
      { href: "/personal-alpha-final-readiness", label: "Personal Alpha Final Review Readiness" },
      { href: "/personal-alpha-final-gate", label: "Personal Alpha Final Gate" },
      { href: "/personal-alpha-final-packet", label: "Personal Alpha Final Packet" },
      { href: "/personal-alpha-lawyer-final-review", label: "Personal Alpha Lawyer Final Review" },
      { href: "/personal-alpha-final-lock", label: "Personal Alpha Final Lock" },
      { href: "/case-os", label: "Personal Alpha Case OS" },
      { href: "/controlled-material", label: "Controlled Material" },
      { href: "/controlled-ocr", label: "Controlled OCR" },
      { href: "/controlled-legal-search", label: "Controlled Legal Search" },
      { href: "/controlled-report-draft", label: "Controlled Report Draft" },
      { href: "/controlled-review", label: "Controlled Review" },
      { href: "/controlled-revision", label: "Controlled Revision" },
      { href: "/controlled-final-review", label: "Controlled Final Review" }
    ]
  },
  {
    label: "个人生产",
    items: [
      { href: "/personal-production", label: "个人生产总控台" },
      { href: "/personal-production-pilot", label: "个人生产实战 Pilot" },
      { href: "/personal-trial-readiness", label: "个人版实战试运行准备" },
      { href: "/personal-provider-readiness", label: "真实接口接入准备" },
      { href: "/personal-live-connection", label: "受控接口接入" },
      { href: "/personal-legal-enterprise", label: "法律与企业信息接口" },
      { href: "/personal-owner-output-center", label: "用户本人产出下载中心" },
      { href: "/personal-case-workspace", label: "个人案件与材料工作台" },
      { href: "/personal-showcase-pack", label: "个人生产试点与展示包" },
      { href: "/personal-delivery-packet", label: "个人生产交付包" },
      { href: "/personal-case-analysis", label: "受控案件分析 Runtime" },
      { href: "/personal-case-analysis/legal-drafts", label: "法律分析草稿工作台" },
      { href: "/personal-case-production", label: "受控案件生产工作流" },
      { href: "/personal-skill-studio", label: "经验包与技能工作室" },
      { href: "/personal-skill-studio/final-drafts", label: "Skill 最终稿工作台" },
      { href: "/personal-skill-studio/training-artifacts", label: "训练产物加载器" },
      { href: "/personal-intelligence", label: "法律与企业信息网关" },
      { href: "/personal-material-runtime", label: "材料解析与 OCR Runtime" },
      { href: "/personal-ai-gateway", label: "AI 网关与草稿 Runtime" }
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
              <div className="mt-1 text-xs text-slate-400">个人版生产验证</div>
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
            当前为模拟元数据展示与受控验证流程；团队版后置，外部交付后置。
          </div>
        </div>
      </aside>
      <section className="md:pl-72">
        <AppTopbar />
        <div className="border-b border-line bg-white px-5 py-4 md:hidden">
          <div className="text-base font-semibold text-ink">AIHome.law</div>
          <div className="mt-1 text-xs text-muted">个人版生产验证</div>
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
