type SectionHeaderProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  action?: React.ReactNode;
};

export function SectionHeader({
  eyebrow,
  title,
  description,
  action
}: SectionHeaderProps) {
  return (
    <header className="flex flex-wrap items-start justify-between gap-4">
      <div>
        {eyebrow ? <div className="text-xs uppercase tracking-wide text-gold">{eyebrow}</div> : null}
        <h1 className="mt-2 text-2xl font-semibold text-ink">{title}</h1>
        {description ? <p className="mt-2 text-sm text-muted">{description}</p> : null}
      </div>
      {action}
    </header>
  );
}
