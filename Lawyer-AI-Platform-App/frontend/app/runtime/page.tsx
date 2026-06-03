import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Card, CardBody } from "@/components/ui/Card";
import { InfoRow } from "@/components/ui/InfoRow";
import { SectionHeader } from "@/components/ui/SectionHeader";
import { getLLMStatus } from "@/services/api";

export const dynamic = "force-dynamic";

export default async function RuntimePage() {
  const { runtime, error } = await loadRuntime();

  return (
    <AppShell>
      <div className="space-y-6">
        <SectionHeader
          eyebrow="AIHome.law 运行状态"
          title="运行状态"
          description="运行状态用于确认当前案件处理、法律分析、报告生成所使用的模型提供方和配置状态。"
        />

        {error ? <StatusMessage message={error} /> : null}

        <Card>
          <CardBody>
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="text-xs uppercase tracking-wide text-muted">模型状态</div>
                <div className="mt-2 text-lg font-semibold text-ink">{runtime?.provider ?? "-"}</div>
              </div>
              <Badge tone={runtime?.configured ? "gold" : "muted"}>
                {runtime?.configured ? "已配置" : "未配置"}
              </Badge>
            </div>
            <div className="mt-5 space-y-3">
              <InfoRow label="提供方" value={runtime?.provider ?? "-"} />
              <InfoRow label="模型" value={runtime?.model ?? "-"} />
              <InfoRow label="已配置" value={formatBoolean(runtime?.configured)} />
              <InfoRow label="Base URL 已配置" value={formatBoolean(runtime?.base_url_configured)} />
              <InfoRow label="llm_provider" value={runtime?.provider ?? "-"} />
              <InfoRow label="llm_status" value={runtime?.configured ? "configured" : "not_configured"} />
              <InfoRow label="未来 token 用量" value="暂不可用" />
              <InfoRow label="未来延迟" value="暂不可用" />
              <InfoRow label="未来成本" value="暂不可用" />
              <InfoRow label="未来错误日志" value="即将推出" />
            </div>
          </CardBody>
        </Card>
      </div>
    </AppShell>
  );
}

async function loadRuntime() {
  try {
    return { runtime: await getLLMStatus(), error: null };
  } catch {
    return { runtime: null, error: "后端 API 暂不可用，请确认 8001 端口的后端服务已启动。" };
  }
}

function formatBoolean(value: boolean | undefined) {
  if (typeof value !== "boolean") {
    return "-";
  }
  return value ? "是" : "否";
}

function StatusMessage({ message }: { message: string }) {
  return (
    <div className="rounded-md border border-line bg-white p-4 text-sm text-muted shadow-sm">
      {message}
    </div>
  );
}
