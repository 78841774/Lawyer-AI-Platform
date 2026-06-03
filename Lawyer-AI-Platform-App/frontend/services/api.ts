const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8001";

export type DashboardStats = {
  cases: number;
  materials: number;
  facts: number;
  analyses: number;
  reports: number;
};

export type CaseRecord = {
  case_id: string;
  title: string;
  case_type: string;
  status: string;
  objective: string | null;
  created_at: string;
  updated_at: string;
};

export type ReportRecord = {
  report_id: string;
  case_id: string;
  report_type: string;
  title: string;
  content: string;
  status: string;
  version: number;
  storage_path: string;
  source_refs: {
    fact_ids?: string[];
    analysis_id?: string;
  };
  created_at: string;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    throw new ApiError(`API request failed: ${path}`, response.status);
  }

  return response.json();
}

export async function getHealth(): Promise<{ status: string }> {
  return request<{ status: string }>("/health");
}

export async function getDashboardStats(): Promise<DashboardStats> {
  return request<DashboardStats>("/dashboard/stats");
}

export async function getCases(): Promise<CaseRecord[]> {
  return request<CaseRecord[]>("/cases");
}

export async function getReports(): Promise<ReportRecord[]> {
  return request<ReportRecord[]>("/reports");
}

export async function getReport(reportId: string): Promise<ReportRecord> {
  return request<ReportRecord>(`/reports/${reportId}`);
}
