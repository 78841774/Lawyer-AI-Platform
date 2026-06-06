import Link from "next/link";

export function BrandHero() {
  return (
    <header className="rounded-md border border-slate-800 bg-navy p-6 text-white shadow-sm">
      <div className="text-xs uppercase tracking-wide text-gold">AIHome.law · Personal Production Pilot</div>
      <h1 className="mt-3 text-3xl font-semibold">个人版生产验证与公开演示准备</h1>
      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-300">
        mock-first、provider-gated、律师复核必需的受控流程展示。当前仅展示 mock metadata，不生成最终法律意见，不自动对外交付；团队版后置，外部交付后置。
      </p>
      <div className="mt-5 flex flex-wrap gap-2 text-xs">
        {["个人生产试点", "来源可追踪", "最终锁定不触发真实导出", "AI Provider Live Gateway 后续受控接入"].map((item) => (
          <span key={item} className="rounded-md border border-white/20 bg-white/10 px-3 py-1 text-slate-100">
            {item}
          </span>
        ))}
      </div>
      <div className="mt-5 flex flex-wrap gap-3">
        <Link href="/personal-production" className="rounded-md bg-gold px-4 py-2 text-sm font-semibold text-navy">
          进入个人生产总控台
        </Link>
        <Link href="/personal-showcase-pack" className="rounded-md border border-slate-600 px-4 py-2 text-sm font-semibold text-slate-100">
          查看公开演示入口
        </Link>
      </div>
    </header>
  );
}
