from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import RawWorkProductBoundaryStatus


def build_raw_work_product_boundary_status() -> dict:
    return RawWorkProductBoundaryStatus(
        warnings=[
            "未脱敏律师办案底稿只能在受控内部解析区处理。",
            "普通前端 API、Skill、训练结果、provider export 均不得直接接收未脱敏底稿。",
            "后续输出必须经过脱敏、抽象化和人工复核。",
        ],
        **v731b_safety_flags(),
    ).model_dump()
