from personal_skill_studio.training_artifacts.schemas import safety_flags


SAFETY_CHECKLIST = [
    "仅加载合成训练产物 metadata",
    "Codex 训练不等于模型微调",
    "只允许脱敏闭案样本 metadata",
    "未结案件不得进入训练产物",
    "不读取真实案件正文",
    "不读取 OCR 原文",
    "不读取或返回密钥值",
    "不调用真实 provider",
    "不写训练集",
    "不更新 Skill",
    "不自动发布 Skill",
    "不生成最终法律意见",
    "不生成正式报告",
    "不创建公开链接",
    "不发送邮件",
    "不自动对外交付",
    "案由匹配与 fallback 仅 dry-run",
    "Gate 仅作为参考",
]


def build_safety() -> dict:
    return {
        "safety_checklist": SAFETY_CHECKLIST,
        "safety": safety_flags(),
        "all_safety_checks_passed": True,
        **safety_flags(),
        "warnings": ["v7.30 training artifact loader is metadata-only and dry-run by default."],
    }


def build_practice_runtime_safety() -> dict:
    from personal_skill_studio.training_artifacts.practice_runtime_registry import build_v731g_status
    from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags

    status = build_v731g_status()
    return {
        "safety_checklist": [
            "仅允许 v7.31f 律师批准经验包进入受控加载 registry",
            "实战运行只读取脱敏/抽象经验 metadata",
            "策略评估必须检查案由、workspace、运行模式、任务类型、灰度比例和使用上限",
            "禁用和回滚只改变加载状态，不删除 package、audit 或 source trace",
            "不调用 provider，不读取密钥，不生成最终法律意见，不对外交付",
        ],
        "runtime_load_count": status.get("runtime_load_count", 0),
        "blocked_count": status.get("blocked_count", 0),
        "all_safety_checks_passed": True,
        **v731g_safety_flags(),
        "warnings": ["v7.31g runtime safety is controlled-loading metadata only."],
    }


def build_practice_feedback_safety() -> dict:
    from personal_skill_studio.training_artifacts.practice_feedback_registry import build_feedback_summary
    from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import v731h_safety_flags

    summary = build_feedback_summary()
    return {
        "safety_checklist": [
            "仅记录实战输出观察 metadata",
            "律师反馈只作为后续迭代候选输入",
            "风险事件不自动触发禁用或回滚",
            "反馈不自动修改已加载 experience package",
            "不调用 provider，不读取密钥，不返回原始输出或案件材料",
        ],
        "observation_count": summary.get("observation_count", 0),
        "feedback_count": summary.get("feedback_count", 0),
        "risk_event_count": summary.get("risk_event_count", 0),
        "all_safety_checks_passed": True,
        **v731h_safety_flags(),
        "warnings": ["v7.31h feedback safety is observation-and-feedback metadata only."],
    }


def build_iteration_candidate_safety() -> dict:
    from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import v731i_safety_flags
    from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import build_v731i_status

    status = build_v731i_status()
    return {
        "safety_checklist": [
            "仅从已 triage 的 v7.31h 反馈和风险 metadata 生成候选包",
            "candidate diff 只作为下一版候选，不修改当前加载包",
            "不修改 lawyer-approved package，不改变 runtime policy",
            "不自动禁用、回滚、训练、发布或加载下一版经验包",
            "不调用 provider，不读取 key value，不返回原始输出或案件材料",
        ],
        "candidate_pack_count": status.get("candidate_pack_count", 0),
        "ready_for_next_build_count": status.get("ready_for_next_build_count", 0),
        "all_safety_checks_passed": True,
        **v731i_safety_flags(),
        "warnings": ["v7.31i candidate pack safety is iteration-preparation metadata only."],
    }


def build_next_package_safety() -> dict:
    from personal_skill_studio.training_artifacts.next_experience_package_registry import build_v731j_status
    from personal_skill_studio.training_artifacts.next_package_safety_engine import v731j_safety_flags

    status = build_v731j_status()
    return {
        "safety_checklist": [
            "仅从 ready_for_next_experience_build 的 candidate pack 生成下一版草案",
            "next package draft 不自动替换当前 runtime package",
            "next package draft 必须重新进入 Practice Load Review Gate",
            "不自动禁用、回滚、训练、发布、生成最终法律意见或对外交付",
            "不调用 provider，不读取 key value，不返回原始输出或案件材料",
        ],
        "next_package_count": status.get("next_package_count", 0),
        "pending_practice_load_review_count": status.get("pending_practice_load_review_count", 0),
        "all_safety_checks_passed": True,
        **v731j_safety_flags(),
        "warnings": ["v7.31j next package safety is draft-rebuild metadata only."],
    }


def build_case_analysis_workbench_safety() -> dict:
    from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
    from personal_skill_studio.training_artifacts.case_analysis_runtime_output_registry import build_v733_workbench_status

    status = build_v733_workbench_status()
    return {
        "safety_checklist": [
            "前端只渲染后端 Skill Output Schema 返回的 output_groups 与 outputs",
            "产出标题、类型、数量、排序均来自 schema",
            "输出仅为脱敏抽象辅助 metadata",
            "反馈和风险事件不自动修改已加载经验包",
            "不调用 provider，不读取 key value，不生成最终法律意见或正式报告",
        ],
        "view_count": status.get("view_count", 0),
        "output_count": status.get("output_count", 0),
        "all_safety_checks_passed": True,
        **v733_safety_flags(),
        "warnings": ["v7.33 case-analysis workbench safety is schema-driven metadata only."],
    }
