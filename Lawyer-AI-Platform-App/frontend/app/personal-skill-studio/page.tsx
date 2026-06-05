"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  TrustSafetyPanel
} from "@/components/personal-production/ProductionShowcaseUI";
import {
  createPersonalExperiencePackage,
  createPersonalSkillCandidate,
  createPersonalSkillEvaluation,
  createPersonalSkillTestCase,
  getPersonalSkillStudioAudit,
  getPersonalSkillStudioPromotionQueue,
  getPersonalSkillStudioSafety,
  getPersonalSkillStudioStatus,
  listPersonalExperiencePackages,
  listPersonalSkillCandidates,
  listPersonalSkillEvaluations,
  listPersonalSkillStudioRuntimes,
  listPersonalSkillStudioSourceTraces,
  listPersonalSkillTestCases,
  submitPersonalSkillStudioPromotionAction
} from "@/services/api";

const defaultCaseId = "case_v55_approve_all";
const promotionActions = ["approve_for_future_review", "request_revision", "reject", "mark_low_confidence", "mark_not_ready"];

export default function PersonalSkillStudioPage() {
  const [data, setData] = useState<Record<string, any>>({});
  const [error, setError] = useState("");
  const [confirmed, setConfirmed] = useState(true);
  const [caseId, setCaseId] = useState(defaultCaseId);
  const [packageTitle, setPackageTitle] = useState("合同纠纷经验包草案");
  const [legalArea, setLegalArea] = useState("合同纠纷");
  const [caseCause, setCaseCause] = useState("买卖合同纠纷");
  const [jurisdiction, setJurisdiction] = useState("中国大陆");
  const [experiencePackageId, setExperiencePackageId] = useState("");
  const [skillCandidateId, setSkillCandidateId] = useState("");
  const [testCaseId, setTestCaseId] = useState("");
  const [promotionAction, setPromotionAction] = useState("approve_for_future_review");

  async function loadStudio() {
    setError("");
    try {
      const [status, runtimes, packages, candidates, testCases, evaluations, queue, traces, audit, safety] = await Promise.all([
        getPersonalSkillStudioStatus(),
        listPersonalSkillStudioRuntimes(),
        listPersonalExperiencePackages(),
        listPersonalSkillCandidates(),
        listPersonalSkillTestCases(),
        listPersonalSkillEvaluations(),
        getPersonalSkillStudioPromotionQueue(),
        listPersonalSkillStudioSourceTraces(),
        getPersonalSkillStudioAudit(),
        getPersonalSkillStudioSafety()
      ]);
      setData({ status, runtimes, packages, candidates, testCases, evaluations, queue, traces, audit, safety });
      setExperiencePackageId((current) => current || packages.experience_packages?.[0]?.experience_package_id || "");
      setSkillCandidateId((current) => current || candidates.skill_candidates?.[0]?.skill_candidate_id || "");
      setTestCaseId((current) => current || testCases.test_cases?.[0]?.test_case_id || "");
    } catch {
      setError("经验包与技能工作室 API 暂不可用，请确认后端服务已启动。");
    }
  }

  useEffect(() => {
    void loadStudio();
  }, []);

  async function createPackage() {
    const result = await createPersonalExperiencePackage({
      case_id: caseId,
      source_trace_ids: [],
      review_result_ids: [],
      package_title: packageTitle,
      legal_area: legalArea,
      case_cause: caseCause,
      jurisdiction,
      explicit_mock_confirmation: confirmed,
      explicit_source_trace_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed,
      explicit_no_auto_publish_confirmation: confirmed
    });
    setExperiencePackageId(result.experience_package_id);
    await loadStudio();
  }

  async function createCandidate() {
    const result = await createPersonalSkillCandidate({
      experience_package_id: experiencePackageId,
      skill_title: "合同纠纷技能候选草案",
      skill_type: "draft_skill_candidate",
      target_legal_area: legalArea,
      target_case_cause: caseCause,
      explicit_mock_confirmation: confirmed,
      explicit_lawyer_review_confirmation: confirmed,
      explicit_no_auto_publish_confirmation: confirmed
    });
    setSkillCandidateId(result.skill_candidate_id);
    await loadStudio();
  }

  async function createTestCase() {
    const result = await createPersonalSkillTestCase({
      skill_candidate_id: skillCandidateId,
      test_case_title: "合同纠纷测试用例草案",
      scenario_type: "metadata_only_scenario",
      explicit_mock_confirmation: confirmed,
      explicit_no_raw_content_confirmation: confirmed
    });
    setTestCaseId(result.test_case_id);
    await loadStudio();
  }

  async function createEvaluation() {
    await createPersonalSkillEvaluation({
      skill_candidate_id: skillCandidateId,
      test_case_ids: testCaseId ? [testCaseId] : [],
      evaluation_scope: "mock_safety_and_quality_check",
      explicit_mock_confirmation: confirmed,
      explicit_manual_review_confirmation: confirmed,
      explicit_no_auto_publish_confirmation: confirmed
    });
    await loadStudio();
  }

  async function submitPromotion() {
    await submitPersonalSkillStudioPromotionAction(skillCandidateId, {
      action: promotionAction,
      reviewer_id: "local_demo_lawyer",
      reviewer_note: "仅更新发布门禁 metadata",
      explicit_manual_confirmation: confirmed,
      explicit_no_auto_publish_confirmation: confirmed,
      explicit_no_final_opinion_confirmation: confirmed
    });
    await loadStudio();
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {error ? <div className="rounded-md border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">{error}</div> : null}
        <Hero title="经验包与技能工作室" subtitle="沉淀案件经验，生成技能候选草案，人工复核后再进入后续流程" badges={["经验包草案", "技能候选草案", "律师复核必需", "未自动发布"]} />
        <section className="grid gap-4 md:grid-cols-6">
          {["工作室状态", "经验包草案", "技能候选草案", "测试用例", "评估记录", "发布门禁"].map((label) => <StatusCard key={label} label={label} />)}
        </section>
        <Panel title="Runtime Cards / 工作室 Runtime">
          <div className="grid gap-3 md:grid-cols-5">
            {(data.runtimes?.runtimes ?? []).map((runtime: any) => <Card key={runtime.runtime_id} title={runtime.display_name} lines={[runtime.runtime_id, `live_enabled=${runtime.live_enabled}`, `auto_publish=${runtime.auto_publish_enabled}`]} />)}
          </div>
        </Panel>
        <section className="grid gap-6 xl:grid-cols-2">
          <Panel title="生成经验包草案">
            <FormGrid>
              <Text label="案件 ID" value={caseId} onChange={setCaseId} />
              <Text label="包标题" value={packageTitle} onChange={setPackageTitle} />
              <Text label="法律领域" value={legalArea} onChange={setLegalArea} />
              <Text label="案由" value={caseCause} onChange={setCaseCause} />
              <Text label="管辖/地域" value={jurisdiction} onChange={setJurisdiction} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <Button label="生成经验包草案" onClick={() => void createPackage()} />
            </FormGrid>
          </Panel>
          <Panel title="生成技能候选草案">
            <FormGrid>
              <Text label="Experience Package ID" value={experiencePackageId} onChange={setExperiencePackageId} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <Button label="生成技能候选草案" onClick={() => void createCandidate()} />
            </FormGrid>
          </Panel>
          <Panel title="生成测试用例草案">
            <FormGrid>
              <Text label="Skill Candidate ID" value={skillCandidateId} onChange={setSkillCandidateId} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <Button label="生成测试用例草案" onClick={() => void createTestCase()} />
            </FormGrid>
          </Panel>
          <Panel title="运行模拟评估">
            <FormGrid>
              <Text label="Test Case ID" value={testCaseId} onChange={setTestCaseId} />
              <Confirm checked={confirmed} onChange={setConfirmed} />
              <Button label="运行模拟评估" onClick={() => void createEvaluation()} />
            </FormGrid>
          </Panel>
        </section>
        <Panel title="Promotion Queue / 发布门禁队列">
          <FormGrid>
            <Select value={promotionAction} options={promotionActions} onChange={setPromotionAction} />
            <Button label="提交发布门禁动作" onClick={() => void submitPromotion()} />
          </FormGrid>
        </Panel>
        <Panel title="Source Trace / 来源追踪">
          <div className="grid gap-3 md:grid-cols-3">{(data.traces?.source_traces ?? []).slice(0, 6).map((trace: any) => <Card key={trace.source_trace_id} title={trace.source_trace_id} lines={[trace.source_type, trace.source_label, `raw_content_returned=${trace.raw_content_returned}`]} />)}</div>
        </Panel>
        <TrustSafetyPanel items={data.safety?.safety_checklist ?? []} title="安全清单" />
        <Panel title="Developer Diagnostics">
          <DiagnosticsPanel data={data} />
        </Panel>
      </div>
    </AppShell>
  );
}

function Hero({ title, subtitle, badges }: { title: string; subtitle: string; badges: string[] }) {
  return <section className="rounded-md border border-slate-800 bg-[#1f261f] p-8 text-white"><h1 className="text-4xl font-semibold">{title}</h1><p className="mt-4 text-slate-300">{subtitle}</p><div className="mt-5 flex flex-wrap gap-2">{badges.map((badge) => <DarkSafetyBadge key={badge} label={badge} />)}</div></section>;
}
function Panel({ title, children }: { title: string; children: React.ReactNode }) { return <section className="rounded-md border border-line bg-paper p-5"><h2 className="text-base font-semibold text-ink">{title}</h2><div className="mt-4">{children}</div></section>; }
function StatusCard({ label }: { label: string }) { return <div className="rounded-md border border-line bg-white p-4"><div className="text-xs text-muted">{label}</div><div className="mt-2 text-xl font-semibold text-ink">已就绪</div></div>; }
function Card({ title, lines }: { title: string; lines: string[] }) { return <div className="rounded-md border border-line bg-white p-4"><div className="text-sm font-semibold text-ink">{title}</div><div className="mt-2 grid gap-1 text-xs text-muted">{lines.map((line) => <span key={line}>{line}</span>)}</div></div>; }
function FormGrid({ children }: { children: React.ReactNode }) { return <div className="grid gap-3">{children}</div>; }
function Text({ label, value, onChange }: { label: string; value: string; onChange: (value: string) => void }) { return <label className="grid gap-2 text-sm"><span>{label}</span><input className="rounded-md border border-line px-3 py-2" value={value} onChange={(event) => onChange(event.target.value)} /></label>; }
function Select({ value, options, onChange }: { value: string; options: string[]; onChange: (value: string) => void }) { return <select className="rounded-md border border-line px-3 py-2 text-sm" value={value} onChange={(event) => onChange(event.target.value)}>{options.map((option) => <option key={option}>{option}</option>)}</select>; }
function Confirm({ checked, onChange }: { checked: boolean; onChange: (value: boolean) => void }) { return <label className="flex gap-2 text-sm"><input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />明确确认：仅模拟结果、无原文、无最终意见、未自动发布</label>; }
function Button({ label, onClick }: { label: string; onClick: () => void }) { return <button type="button" className="rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white" onClick={onClick}>{label}</button>; }
