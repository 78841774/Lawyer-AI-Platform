CREATE TABLE IF NOT EXISTS cases (
    id BIGSERIAL PRIMARY KEY,
    case_id VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    case_type VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    parties JSONB NOT NULL DEFAULT '[]'::jsonb,
    objective TEXT,
    experience_package_id VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_cases_case_type ON cases(case_type);
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);

CREATE TABLE IF NOT EXISTS materials (
    id BIGSERIAL PRIMARY KEY,
    material_id VARCHAR(64) NOT NULL UNIQUE,
    case_id VARCHAR(64) NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    material_type VARCHAR(80),
    content_type VARCHAR(120),
    storage_path TEXT NOT NULL,
    ocr_path TEXT,
    parse_status VARCHAR(40) NOT NULL DEFAULT 'pending',
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_materials_case_id ON materials(case_id);
CREATE INDEX IF NOT EXISTS idx_materials_parse_status ON materials(parse_status);

CREATE TABLE IF NOT EXISTS facts (
    id BIGSERIAL PRIMARY KEY,
    fact_id VARCHAR(64) NOT NULL UNIQUE,
    case_id VARCHAR(64) NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    fact_type VARCHAR(80) NOT NULL,
    source_materials JSONB NOT NULL DEFAULT '[]'::jsonb,
    evidence_refs JSONB NOT NULL DEFAULT '[]'::jsonb,
    occurred_at TIMESTAMPTZ,
    parties JSONB NOT NULL DEFAULT '[]'::jsonb,
    confidence NUMERIC(4, 3),
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_facts_case_id ON facts(case_id);
CREATE INDEX IF NOT EXISTS idx_facts_fact_type ON facts(fact_type);
CREATE INDEX IF NOT EXISTS idx_facts_status ON facts(status);

CREATE TABLE IF NOT EXISTS legal_issues (
    id BIGSERIAL PRIMARY KEY,
    issue_id VARCHAR(64) NOT NULL UNIQUE,
    case_id VARCHAR(64) NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    issue TEXT NOT NULL,
    related_facts JSONB NOT NULL DEFAULT '[]'::jsonb,
    legal_rules JSONB NOT NULL DEFAULT '[]'::jsonb,
    reasoning_chain JSONB NOT NULL DEFAULT '[]'::jsonb,
    conclusion TEXT,
    risk_level VARCHAR(40),
    citations JSONB NOT NULL DEFAULT '[]'::jsonb,
    confidence NUMERIC(4, 3),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_legal_issues_case_id ON legal_issues(case_id);
CREATE INDEX IF NOT EXISTS idx_legal_issues_risk_level ON legal_issues(risk_level);

CREATE TABLE IF NOT EXISTS reports (
    id BIGSERIAL PRIMARY KEY,
    report_id VARCHAR(64) NOT NULL UNIQUE,
    case_id VARCHAR(64) NOT NULL REFERENCES cases(case_id) ON DELETE CASCADE,
    report_type VARCHAR(80) NOT NULL,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'draft',
    version INTEGER NOT NULL DEFAULT 1,
    storage_path TEXT,
    source_refs JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reports_case_id ON reports(case_id);
CREATE INDEX IF NOT EXISTS idx_reports_report_type ON reports(report_type);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
