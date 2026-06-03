type InfoRowProps = {
  label: string;
  value: string;
};

export function InfoRow({ label, value }: InfoRowProps) {
  return (
    <div className="flex items-start justify-between gap-4 border-b border-line pb-3 text-sm last:border-b-0 last:pb-0">
      <span className="text-muted">{label}</span>
      <span className="break-words text-right font-medium text-ink">{value}</span>
    </div>
  );
}
