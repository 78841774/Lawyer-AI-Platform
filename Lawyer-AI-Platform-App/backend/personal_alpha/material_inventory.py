from collections import Counter
from pathlib import Path
from typing import Any
from uuid import uuid4

from local_sandbox.guards import check_material_safety_guard
from personal_alpha.schemas import MaterialInventoryItem, MaterialInventoryRequest, MaterialInventoryResult, utc_now


def build_material_inventory_preview(request: MaterialInventoryRequest) -> dict[str, Any]:
    material_guard = check_material_safety_guard(request.local_case_root)
    warnings = [
        "Material inventory preview only.",
        "File content was not read.",
        "File names are redacted.",
        "Real case material must remain outside Git.",
    ]
    warnings.extend(str(item) for item in material_guard.get("warnings", []))
    if request.include_file_names:
        warnings.append("include_file_names=true was requested, but filenames remain redacted in v4.1.")
    if not request.dry_run_only:
        warnings.append("dry_run_only=false is blocked; v4.1 supports dry-run only.")

    items = _preview_items(request.local_case_root)
    return MaterialInventoryResult(
        inventory_id=f"personal_alpha_inventory_{uuid4().hex[:12]}",
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        item_count=len(items),
        items=items,
        content_read=False,
        warnings=list(dict.fromkeys(warnings)),
        created_at=utc_now(),
    ).model_dump()


def _preview_items(local_case_root: str | None) -> list[MaterialInventoryItem]:
    extension_counts = _extension_counts(local_case_root)
    if not extension_counts:
        return [
            MaterialInventoryItem(
                item_id="material_preview_001",
                filename_redacted="<filename_redacted>.unknown",
                extension=None,
                relative_path_redacted="<relative_path_redacted>",
                size_bytes=None,
                content_read=False,
                mock_only=True,
            )
        ]

    items: list[MaterialInventoryItem] = []
    index = 1
    for extension, count in sorted(extension_counts.items()):
        for _ in range(count):
            suffix = extension or ".unknown"
            items.append(
                MaterialInventoryItem(
                    item_id=f"material_preview_{index:03d}",
                    filename_redacted=f"<filename_redacted>{suffix}",
                    extension=extension or None,
                    relative_path_redacted="<relative_path_redacted>",
                    size_bytes=None,
                    content_read=False,
                    mock_only=True,
                )
            )
            index += 1
            if index > 20:
                return items
    return items


def _extension_counts(local_case_root: str | None) -> Counter[str]:
    if not local_case_root:
        return Counter()
    if not local_case_root.startswith("~/"):
        return Counter()
    root = Path.home() / local_case_root[2:]
    if not root.exists() or not root.is_dir():
        return Counter()

    counts: Counter[str] = Counter()
    try:
        for entry in root.iterdir():
            if entry.is_file():
                counts[entry.suffix.lower()] += 1
    except OSError:
        return Counter()
    return counts
