from personal_skill_studio.training_artifacts.schemas import CaseCauseNode, CaseCauseTaxonomyManifest


NODES = [
    CaseCauseNode(
        case_cause_id="civil",
        case_domain="civil",
        case_cause_code="civil",
        case_cause_name="民事案件",
        level=1,
        case_cause_path=["civil"],
        child_ids=["civil_contract_dispute", "civil_tort_dispute", "civil_marriage_inheritance"],
        applicable_dispute_types=["民事争议"],
        applicable_fact_patterns=["主体关系", "时间线", "证据链"],
        applicable_legal_patterns=["请求权基础", "抗辩路径"],
        evidence_types=["contract", "receipt", "communication_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_contract_dispute",
        case_domain="civil",
        case_cause_code="civil.contract",
        case_cause_name="合同纠纷",
        level=2,
        case_cause_path=["civil", "contract_dispute"],
        parent_id="civil",
        child_ids=["civil_contract_sales", "civil_contract_loan", "civil_contract_lease"],
        applicable_dispute_types=["买卖合同", "借款合同", "租赁合同"],
        applicable_fact_patterns=["合同成立", "履行节点", "违约事实", "损失计算"],
        applicable_legal_patterns=["合同效力", "违约责任", "解除与抗辩"],
        evidence_types=["contract", "invoice", "delivery_record", "payment_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_contract_sales",
        case_domain="civil",
        case_cause_code="civil.contract.sales",
        case_cause_name="买卖合同纠纷",
        level=3,
        case_cause_path=["civil", "contract_dispute", "sales_contract_dispute"],
        parent_id="civil_contract_dispute",
        applicable_dispute_types=["货款", "交付", "质量", "验收"],
        applicable_fact_patterns=["订单", "交付", "验收", "对账", "欠款"],
        applicable_legal_patterns=["付款请求权", "质量抗辩", "迟延履行责任"],
        evidence_types=["contract", "invoice", "delivery_record", "reconciliation_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_contract_loan",
        case_domain="civil",
        case_cause_code="civil.contract.loan",
        case_cause_name="借款合同纠纷",
        level=3,
        case_cause_path=["civil", "contract_dispute", "loan_contract_dispute"],
        parent_id="civil_contract_dispute",
        applicable_dispute_types=["本金", "利息", "担保", "还款"],
        applicable_fact_patterns=["借款交付", "利息约定", "还款节点", "催收记录"],
        applicable_legal_patterns=["借款返还", "利息边界", "担保责任"],
        evidence_types=["loan_contract", "transfer_record", "repayment_record", "guarantee_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_contract_lease",
        case_domain="civil",
        case_cause_code="civil.contract.lease",
        case_cause_name="租赁合同纠纷",
        level=3,
        case_cause_path=["civil", "contract_dispute", "lease_contract_dispute"],
        parent_id="civil_contract_dispute",
        applicable_dispute_types=["租金", "押金", "返还", "解除"],
        applicable_fact_patterns=["交付占有", "租金支付", "解除通知"],
        applicable_legal_patterns=["租赁返还", "违约责任", "损害赔偿"],
        evidence_types=["lease_contract", "payment_record", "notice_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_tort_dispute",
        case_domain="civil",
        case_cause_code="civil.tort",
        case_cause_name="侵权责任纠纷",
        level=2,
        case_cause_path=["civil", "tort_dispute"],
        parent_id="civil",
        child_ids=["civil_tort_traffic", "civil_tort_medical"],
        applicable_dispute_types=["交通事故", "医疗损害"],
        applicable_fact_patterns=["侵权行为", "损害后果", "因果关系", "责任比例"],
        applicable_legal_patterns=["过错责任", "赔偿项目", "举证责任"],
        evidence_types=["accident_record", "medical_record", "expense_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_tort_traffic",
        case_domain="civil",
        case_cause_code="civil.tort.traffic",
        case_cause_name="机动车交通事故责任纠纷",
        level=3,
        case_cause_path=["civil", "tort_dispute", "traffic_accident_dispute"],
        parent_id="civil_tort_dispute",
        applicable_dispute_types=["责任认定", "人身损害", "保险赔付"],
        applicable_fact_patterns=["事故经过", "责任认定", "损害项目", "保险关系"],
        applicable_legal_patterns=["赔偿责任", "保险责任", "责任比例"],
        evidence_types=["traffic_accident_certificate", "medical_record", "insurance_policy"],
    ),
    CaseCauseNode(
        case_cause_id="civil_tort_medical",
        case_domain="civil",
        case_cause_code="civil.tort.medical",
        case_cause_name="医疗损害责任纠纷",
        level=3,
        case_cause_path=["civil", "tort_dispute", "medical_damage_dispute"],
        parent_id="civil_tort_dispute",
        applicable_dispute_types=["诊疗行为", "损害后果", "鉴定"],
        applicable_fact_patterns=["诊疗经过", "损害后果", "病历封存", "鉴定意见"],
        applicable_legal_patterns=["医疗过错", "因果关系", "赔偿范围"],
        evidence_types=["medical_record", "expert_opinion", "expense_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_marriage_inheritance",
        case_domain="civil",
        case_cause_code="civil.marriage_inheritance",
        case_cause_name="婚姻家事与继承纠纷",
        level=2,
        case_cause_path=["civil", "marriage_inheritance"],
        parent_id="civil",
        child_ids=["civil_marriage_divorce", "civil_inheritance"],
        applicable_dispute_types=["离婚", "继承"],
        applicable_fact_patterns=["身份关系", "财产范围", "处分行为"],
        applicable_legal_patterns=["共同财产", "继承顺位", "遗嘱效力"],
        evidence_types=["identity_record", "property_record", "will_metadata"],
    ),
    CaseCauseNode(
        case_cause_id="civil_marriage_divorce",
        case_domain="civil",
        case_cause_code="civil.marriage.divorce",
        case_cause_name="离婚纠纷",
        level=3,
        case_cause_path=["civil", "marriage_inheritance", "divorce_dispute"],
        parent_id="civil_marriage_inheritance",
        applicable_dispute_types=["解除婚姻", "子女抚养", "财产分割"],
        applicable_fact_patterns=["婚姻关系", "子女情况", "财产范围", "过错事实"],
        applicable_legal_patterns=["离婚条件", "抚养安排", "共同财产分割"],
        evidence_types=["identity_record", "property_record", "child_care_record"],
    ),
    CaseCauseNode(
        case_cause_id="civil_inheritance",
        case_domain="civil",
        case_cause_code="civil.inheritance",
        case_cause_name="继承纠纷",
        level=3,
        case_cause_path=["civil", "marriage_inheritance", "inheritance_dispute"],
        parent_id="civil_marriage_inheritance",
        applicable_dispute_types=["法定继承", "遗嘱继承", "遗产范围"],
        applicable_fact_patterns=["继承人范围", "遗产清单", "遗嘱 metadata"],
        applicable_legal_patterns=["继承顺位", "遗嘱效力", "遗产分割"],
        evidence_types=["identity_record", "property_record", "will_metadata"],
    ),
]


def list_nodes() -> list[CaseCauseNode]:
    return list(NODES)


def build_taxonomy_manifest() -> CaseCauseTaxonomyManifest:
    nodes = list_nodes()
    return CaseCauseTaxonomyManifest(
        nodes=nodes,
        node_count=len(nodes),
        warnings=["Synthetic taxonomy metadata only; no real case material is included."],
    )


def get_case_cause_node(case_cause_id: str) -> CaseCauseNode | None:
    return next((node for node in NODES if node.case_cause_id == case_cause_id), None)


def find_node_by_path(case_cause_path: list[str]) -> CaseCauseNode | None:
    path = [item for item in case_cause_path if item]
    return next((node for node in NODES if node.case_cause_path == path), None)

