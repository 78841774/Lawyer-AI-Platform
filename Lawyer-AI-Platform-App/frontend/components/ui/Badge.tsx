type BadgeProps = {
  children: React.ReactNode;
  tone?: "default" | "gold" | "blue" | "muted";
};

const toneClass = {
  default: "border-line bg-white text-ink",
  gold: "border-gold bg-amber-50 text-amber-800",
  blue: "border-blue-200 bg-blue-50 text-blue-700",
  muted: "border-line bg-slate-50 text-muted"
};

export function Badge({ children, tone = "default" }: BadgeProps) {
  return (
    <span className={`inline-flex rounded-md border px-2 py-1 text-xs font-medium ${toneClass[tone]}`}>
      {children}
    </span>
  );
}
