"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import {
  DarkSafetyBadge,
  DiagnosticsPanel,
  SafeErrorNotice,
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
  getPersonalSkillSampleRegistry,
  getPersonalSkillTrainingStatus,
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
      const [status, trainingStatus, sampleRegistry, runtimes, packages, candidates, testCases, evaluations, queue, traces, audit, safety] = await Promise.all([
        getPersonalSkillStudioStatus(),
        getPersonalSkillTrainingStatus(),
        getPersonalSkillSampleRegistry(),
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
      setData({ status, trainingStatus, sampleRegistry, runtimes, packages, candidates, testCases, evaluations, queue, traces, audit, safety });
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
        {error ? <SafeErrorNotice message={error} /> : null}
        <Hero title="经验包与技能工作室" subtitle="受控 Skill Training Runtime：训练样本脱敏、人工确认、仅生成草稿元数据，不自动发布 Skill" badges={["训练样本脱敏", "仅元数据", "草稿状态", "律师复核必需", "未自动发布"]} />
        <Panel title="v7.22 两个 Skill 最终稿与优化工作台">
          <div className="grid gap-4 md:grid-cols-3">
            <Card title="案件事实提炼 Skill" lines={["final draft metadata", "owner-only download", "不自动训练未结案件"]} />
            <Card title="案件法律分析 Skill" lines={["final draft metadata", "gate reference-only", "不自动发布 Skill"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/final-drafts">
              打开 Skill 最终稿工作台
            </a>
          </div>
        </Panel>
        <Panel title="v7.30 Codex 训练产物加载器">
          <div className="grid gap-4 md:grid-cols-4">
            <Card title="Codex 训练方案" lines={["不是模型微调", "闭案样本 metadata", "不训练未结案件"]} />
            <Card title="多层级案由" lines={["civil / contract / tort", "exact + ancestor fallback", "evidence overlay"]} />
            <Card title="Skill Context" lines={["fact + legal Skill", "dry-run only", "不自动发布 Skill"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/training-artifacts">
              打开训练产物加载器
            </a>
          </div>
        </Panel>
        <Panel title="v7.31 已结案件 Codex 训练执行">
          <div className="grid gap-4 md:grid-cols-4">
            <Card title="Synthetic Closed Cases" lines={["source_case_mode=synthetic_closed_case", "不读取真实案件", "不使用未结案件"]} />
            <Card title="Training Run Manifest" lines={["生成 run metadata", "experience packages", "loading manifest"]} />
            <Card title="Generated Skill Manifests" lines={["case_fact_extraction_skill", "case_legal_analysis_skill", "不自动发布 Skill"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/training-artifacts">
              打开 v7.31 训练执行
            </a>
          </div>
        </Panel>
        <Panel title="v7.31a 真实已结案件训练材料导入与脱敏管线">
          <div className="grid gap-4 md:grid-cols-4">
            <Card title="Real Closed Case Intake" lines={["source_case_mode=real_closed_case", "授权与已结确认", "不保存原文"]} />
            <Card title="Redaction Pipeline" lines={["身份信息移除", "法律必要 metadata 保留", "manual review required"]} />
            <Card title="Segments" lines={["事实类 segment", "法律分析类 segment", "metadata_only=true"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/training-artifacts">
              打开 v7.31a intake
            </a>
          </div>
        </Panel>
        <Panel title="v7.31b / v7.31c 经验候选与 Skill 草案工作台">
          <div className="grid gap-4 md:grid-cols-4">
            <Card title="v7.31b Experience Candidates" lines={["受控 OCR/文档解析", "法律检索 metadata", "脱敏后人工复核"]} />
            <Card title="v7.31c Experience Pool" lines={["仅导入 approved_for_skill_experience", "source trace required", "audit required"]} />
            <Card title="Skill Draft Boundary" lines={["requires_manual_confirmation", "not_publishable", "确认不发布 Skill"]} />
            <a className="rounded-md bg-slate-900 px-4 py-3 text-sm font-semibold text-white" href="/personal-skill-studio/training-artifacts">
              打开经验池与草案工作台
            </a>
          </div>
        </Panel>
        <section className="grid gap-4 md:grid-cols-6">
          {["工作室状态", "经验包草案", "技能候选草案", "测试用例", "评估记录", "发布门禁"].map((label) => <StatusCard key={label} label={label} />)}
        </section>
        <Panel title="Skill Training Runtime / 受控训练状态">
          <div className="grid gap-3 md:grid-cols-4">
            <Card title="Runtime" lines={[`status=${String(data.trainingStatus?.status ?? "draft_metadata_ready")}`, `metadata_only=${String(data.trainingStatus?.metadata_only ?? true)}`, `draft_only=${String(data.trainingStatus?.draft_only ?? true)}`]} />
            <Card title="Training Samples" lines={[`desensitized=${String(data.trainingStatus?.training_samples_desensitized ?? true)}`, `manual_confirmation=${String(data.trainingStatus?.manual_confirmation_required ?? true)}`, `source_trace=${String(data.trainingStatus?.source_trace_required ?? true)}`]} />
            <Card title="AI / Prompt Boundary" lines={[`live_call_executed=${String(data.trainingStatus?.live_call_executed ?? false)}`, `used_in_ai_prompt=${String(data.trainingStatus?.used_in_ai_prompt ?? false)}`, `provider_gated=${String(data.trainingStatus?.provider_gated ?? true)}`]} />
            <Card title="Publish Boundary" lines={[`final_skill_published=${String(data.trainingStatus?.final_skill_published ?? false)}`, `auto_publish=${String(data.trainingStatus?.auto_publish_enabled ?? false)}`, `external_delivery=${String(data.trainingStatus?.external_delivery_triggered ?? false)}`]} />
          </div>
        </Panel>
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
        <section className="grid gap-6 xl:grid-cols-3">
          <Panel title="Skill Candidate Cards / 技能候选草案">
            <div className="grid gap-3">
              {(data.candidates?.skill_candidates ?? []).slice(0, 4).map((candidate: any) => (
                <Card key={candidate.skill_candidate_id} title={candidate.skill_title ?? candidate.skill_candidate_id} lines={[`draft_only=${candidate.draft_only}`, `final_skill_published=${candidate.final_skill_published}`, `lawyer_review=${candidate.lawyer_review_required}`]} />
              ))}
            </div>
          </Panel>
          <Panel title="Test Case Draft Panel / 测试用例草案">
            <div className="grid gap-3">
              {(data.testCases?.test_cases ?? []).slice(0, 4).map((testCase: any) => (
                <Card key={testCase.test_case_id} title={testCase.test_case_title ?? testCase.test_case_id} lines={[`metadata_only=${testCase.metadata_only}`, `raw_content=${testCase.raw_content_included}`, `source_trace=${testCase.source_trace_required}`]} />
              ))}
            </div>
          </Panel>
          <Panel title="Evaluation Panel / 模拟评估">
            <div className="grid gap-3">
              {(data.evaluations?.evaluations ?? []).slice(0, 4).map((evaluation: any) => (
                <Card key={evaluation.evaluation_id} title={evaluation.evaluation_id} lines={[`recommendation=${evaluation.recommendation}`, `draft_only=${evaluation.draft_only}`, `final_skill_published=${evaluation.final_skill_published}`]} />
              ))}
            </div>
          </Panel>
        </section>
        <Panel title="Source Trace / 来源追踪">
          <div className="grid gap-3 md:grid-cols-3">{(data.traces?.source_traces ?? []).slice(0, 6).map((trace: any) => <Card key={trace.source_trace_id} title={trace.source_trace_id} lines={[trace.source_type, trace.source_label, `raw_content_returned=${trace.raw_content_returned}`]} />)}</div>
        </Panel>
        <TrustSafetyPanel items={data.safety?.safety_checklist ?? []} title="安全清单" />
        <Panel title="开发诊断（默认折叠）">
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
