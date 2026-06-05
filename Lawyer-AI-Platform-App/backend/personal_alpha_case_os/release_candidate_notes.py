from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSReleaseNotesPreview,
    PersonalAlphaCaseOSReleaseNotesPreviewSection,
)


def build_release_notes_preview() -> dict[str, object]:
    sections = [
        PersonalAlphaCaseOSReleaseNotesPreviewSection(section_id="summary", title="Summary"),
        PersonalAlphaCaseOSReleaseNotesPreviewSection(section_id="capabilities", title="Capabilities"),
        PersonalAlphaCaseOSReleaseNotesPreviewSection(section_id="safety_boundary", title="Safety Boundary"),
        PersonalAlphaCaseOSReleaseNotesPreviewSection(section_id="validation", title="Validation"),
        PersonalAlphaCaseOSReleaseNotesPreviewSection(section_id="next", title="Next: v7.0 Personal Production Workspace Foundation"),
    ]
    return PersonalAlphaCaseOSReleaseNotesPreview(
        release_notes_preview={
            "title": "v6.9 Personal Alpha Case OS Release Candidate",
            "release_type": "metadata_only_release_candidate_preview",
            "sections": [section.model_dump() for section in sections],
        },
        would_create_file=False,
        would_generate_final_report=False,
        would_generate_legal_opinion=False,
        would_include_raw_content=False,
        warnings=[
            "Release notes preview does not create files.",
            "Release notes preview is metadata-only.",
        ],
    ).model_dump()
