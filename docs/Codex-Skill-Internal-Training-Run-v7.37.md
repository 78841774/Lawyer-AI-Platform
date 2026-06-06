# Codex Skill Internal Training Run v7.37

v7.37 adds a controlled internal training run surface after v7.35 dataset generation and v7.36 dry-run validation.

## Scope

- Starts an internal training run metadata record from ready improvement candidates.
- Reuses v7.35 dataset / gate artifacts and v7.36 dry-run artifacts as prerequisites.
- Supports internal simulation labels for local CPU / GPU style execution metadata without external provider calls.
- Records training logs, metrics, audit metadata, source trace metadata, dry-run comparison, and a gate report.
- Adds frontend training run status, metrics overview, logs, and gate report panels.

## Safety Boundary

v7.37 does not call providers, read key values, perform external training, replace runtime packages, modify loaded packages, modify lawyer-approved packages, update or publish Skills, generate final legal opinions, generate formal reports, create real PDF/DOCX files, create public links, send email, or trigger external delivery.

Training artifacts remain inside the internal training workspace as metadata-only records. No local path, raw case material, raw OCR text, secret, or provider response is exposed.

