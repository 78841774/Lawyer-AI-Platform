import Link from "next/link";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/cases", label: "Cases" },
  { href: "/cases/demo-case", label: "Case Detail" },
  { href: "/cases/demo-case/materials", label: "Materials" },
  { href: "/cases/demo-case/facts", label: "Facts" },
  { href: "/cases/demo-case/legal", label: "Legal" },
  { href: "/cases/demo-case/reports", label: "Reports" }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <main className="min-h-screen bg-paper">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-line bg-white px-5 py-6 md:block">
        <div className="text-lg font-semibold text-ink">Lawyer AI</div>
        <nav className="mt-8 space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block rounded-md px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <section className="md:pl-64">
        <div className="mx-auto max-w-6xl px-5 py-8">{children}</div>
      </section>
    </main>
  );
}
