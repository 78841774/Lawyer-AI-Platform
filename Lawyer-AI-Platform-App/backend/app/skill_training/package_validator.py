from app.models.skill import Skill


class PackageValidator:
    def validate_skill(self, skill: Skill) -> None:
        if not skill.evaluation_details or skill.evaluation_details == "{}":
            raise ValueError("skill not evaluated")
        if skill.validation_status != "validated":
            raise ValueError("skill not validated")

