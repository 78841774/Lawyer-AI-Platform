from uuid import uuid4

from fastapi import HTTPException

from personal_trial_readiness.schemas import IssueLogItem, IssueLogList, IssueLogMockRequest
from personal_trial_readiness.storage import list_json, read_json, write_json


DEFAULT_ISSUES = [
    IssueLogItem(
        issue_id="issue_mock_001",
        trial_id="trial_mock_001",
        stage_id="diagnostics",
        issue_type="unclear_copy",
        severity="low",
        title="诊断区文案需要继续保持中文",
        description="Developer Diagnostics 默认折叠，摘要处继续使用中文说明。",
        suggested_fix="v7.26 可统一优化诊断摘要文案。",
        status="open",
    ),
    IssueLogItem(
        issue_id="issue_mock_002",
        trial_id="trial_mock_001",
        stage_id="owner_output_center",
        issue_type="workflow",
        severity="medium",
        title="本人下载边界需要在演示时重复说明",
        description="下载动作仅生成 metadata，不创建真实文件或公开链接。",
        suggested_fix="v7.26 可强化下载按钮旁的边界提示。",
        status="acknowledged",
    ),
]


def list_issues(trial_id: str | None = None) -> dict:
    stored = [IssueLogItem(**item) for item in list_json("issues")]
    records = stored or DEFAULT_ISSUES
    if trial_id:
        records = [issue for issue in records if issue.trial_id == trial_id]
    return IssueLogList(trial_id=trial_id, issues=records, issue_count=len(records)).model_dump()


def get_issue(issue_id: str) -> IssueLogItem | None:
    for issue in DEFAULT_ISSUES:
        if issue.issue_id == issue_id:
            return issue
    data = read_json("issues", issue_id)
    return IssueLogItem(**data) if data else None


def create_mock_issue(trial_id: str, request: IssueLogMockRequest) -> dict:
    issue = IssueLogItem(
        issue_id=f"issue_{uuid4().hex[:10]}",
        trial_id=trial_id,
        stage_id=request.stage_id,
        issue_type=request.issue_type,
        severity=request.severity,
        title=request.title,
        description=request.description,
        suggested_fix=request.suggested_fix,
        status="open",
        warnings=["问题记录只用于优化，不自动阻断下一步。"],
    )
    write_json("issues", issue.issue_id, issue.model_dump())
    return issue.model_dump()


def require_issue(issue_id: str) -> IssueLogItem:
    issue = get_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="issue_id 不存在")
    return issue

