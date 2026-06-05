# Provider Roadmap

## Provider Categories

- AI: OpenAI, DeepSeek, Local Model.
- OCR: PaddleOCR / Baidu AI Studio.
- File Parsing: MinerU, Docling.
- Legal Search: Kuaicha 365 LawSkills API.
- Enterprise Info: Tianyancha AI.
- Optional: Qichacha, PKULaw, National Law Database.

## Version Scope

- v7.1 only builds the AI Gateway for AI provider metadata, prompt rendering preview, and draft-only mock AI runs.
- v7.2 introduces MinerU, Docling, and PaddleOCR placeholders for Controlled Material Parsing and OCR runtime foundations.
- v7.3 builds Kuaicha 365 LawSkills API and Tianyancha AI gateway foundations.
- v7.4 builds Experience Package Skill Studio foundations without automatic Skill publishing.
- v7.5 builds Real Case Production Workflow foundations without final report generation or external delivery.
- v7.6 builds Personal Delivery Packet foundations without live provider calls, final legal opinion generation, final report generation, real PDF/DOCX generation, email sending, or external delivery.
- v7.7 builds Personal Production Pilot & Showcase Pack foundations without live provider calls, API key access, raw content exposure, final legal opinion generation, final report generation, real PDF/DOCX generation, email sending, external delivery, or Skill publishing.

## Boundary

Provider metadata may be registered before live integrations exist. Live provider calls stay disabled unless the target version explicitly enables them behind controlled gates.
