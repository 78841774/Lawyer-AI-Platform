type ButtonProps = {
  children: React.ReactNode;
  type?: "button" | "submit";
  disabled?: boolean;
  onClick?: () => void;
  variant?: "primary" | "secondary";
  className?: string;
};

export function Button({
  children,
  type = "button",
  disabled = false,
  onClick,
  variant = "primary",
  className = ""
}: ButtonProps) {
  const variantClass =
    variant === "primary"
      ? "bg-accent text-white"
      : "border border-line bg-white text-ink";

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      className={`rounded-md px-3 py-2 text-sm font-medium shadow-sm disabled:opacity-60 ${variantClass} ${className}`}
    >
      {children}
    </button>
  );
}
