export type CaseStatus = "draft" | "material_uploaded" | "facts_ready" | "legal_ready" | "reported";

export type CaseSummary = {
  caseId: string;
  title: string;
  caseType: string;
  status: CaseStatus;
  updatedAt: string;
};

export type Fact = {
  factId: string;
  description: string;
  factType: string;
  confidence: number;
  status: string;
};

export type LegalIssue = {
  issueId: string;
  issue: string;
  conclusion: string;
  riskLevel: "low" | "medium" | "high";
};
