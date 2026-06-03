class PromptContextBuilder:
    def build(
        self,
        *,
        case: object | None = None,
        materials: list[object] | None = None,
        facts: list[object] | None = None,
        analysis: object | None = None,
        skill: object | None = None,
        package: object | None = None,
        runtime_metadata: dict | None = None
    ) -> dict[str, object]:
        return {
            "case": self._to_dict(case),
            "materials": self._to_dict_list(materials),
            "facts": self._to_dict_list(facts),
            "analysis": self._to_dict(analysis),
            "skill": self._to_dict(skill),
            "package": self._to_dict(package),
            "runtime_metadata": runtime_metadata or {}
        }

    def _to_dict_list(self, value: list[object] | None) -> list[object]:
        return [self._to_dict(item) for item in value or []]

    def _to_dict(self, value: object | None) -> object | None:
        if value is None:
            return None
        if isinstance(value, dict):
            return value

        data = getattr(value, "__dict__", None)
        if not isinstance(data, dict):
            return value

        return {
            key: item
            for key, item in data.items()
            if not key.startswith("_")
        }
