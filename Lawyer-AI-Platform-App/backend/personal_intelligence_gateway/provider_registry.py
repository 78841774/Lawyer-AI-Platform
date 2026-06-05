from personal_intelligence_gateway.schemas import PersonalIntelligenceProvider, PersonalIntelligenceProviderList


PROVIDER_DEFINITIONS = [
    {
        "provider_id": "kuaicha365_lawskills_provider",
        "label": "快查 365 LawSkills",
        "category": "legal_search",
        "capabilities": [
            "法律法规检索 placeholder",
            "司法案例检索 placeholder",
            "裁判规则检索 placeholder",
            "法条详情 placeholder",
            "案例详情 placeholder",
        ],
    },
    {
        "provider_id": "tianyancha_ai_provider",
        "label": "天眼查 AI",
        "category": "enterprise_intelligence",
        "capabilities": [
            "企业工商信息 placeholder",
            "法定代表人/股东高管 placeholder",
            "经营状态 placeholder",
            "司法风险 placeholder",
            "执行信息 placeholder",
        ],
    },
    {
        "provider_id": "qichacha_provider_placeholder",
        "label": "企查查 Placeholder",
        "category": "enterprise_intelligence",
        "capabilities": ["企业信息 placeholder", "企业风险 placeholder"],
    },
    {
        "provider_id": "pkulaw_provider_placeholder",
        "label": "北大法宝 Placeholder",
        "category": "legal_search",
        "capabilities": ["法律检索 placeholder", "案例检索 placeholder"],
    },
    {
        "provider_id": "national_law_database_provider_placeholder",
        "label": "国家法律法规数据库 Placeholder",
        "category": "legal_search",
        "capabilities": ["法律法规检索 placeholder", "法条详情 placeholder"],
    },
]


def list_providers() -> dict:
    providers = [
        PersonalIntelligenceProvider(
            display_name=definition["label"],
            provider_type=definition["category"],
            warnings=["当前仅为占位和模拟结果，未调用真实服务。"],
            **definition,
        )
        for definition in PROVIDER_DEFINITIONS
    ]
    return PersonalIntelligenceProviderList(
        providers=providers,
        provider_count=len(providers),
        configured_provider_count=sum(1 for provider in providers if provider.configured),
        live_provider_count=sum(1 for provider in providers if provider.live_enabled),
        warnings=["所有法律与企业信息 Provider 均为 provider-gated 占位，未读取或显示 API key。"],
    ).model_dump()


def get_provider(provider_id: str) -> PersonalIntelligenceProvider | None:
    for provider in list_providers()["providers"]:
        if provider.get("provider_id") == provider_id:
            return PersonalIntelligenceProvider(**provider)
    return None


def validate_provider(provider_id: str, category: str) -> list[str]:
    provider = get_provider(provider_id)
    if provider is None:
        return ["provider_id 未注册"]
    if provider.category != category:
        return [f"provider 必须属于 {category} 类型"]
    if not provider.mock_available:
        return ["provider 未开启 mock 模式"]
    if provider.live_enabled:
        return ["v7.3 必须保持真实服务调用关闭"]
    return []
