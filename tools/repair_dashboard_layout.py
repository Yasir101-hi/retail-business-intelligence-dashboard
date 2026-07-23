"""Apply verified presentation fixes to the retail Power BI report.

The script updates report-layout metadata only. It does not alter the semantic
model, stored DAX expressions, relationships, or imported data.
"""

from __future__ import annotations

import json
import os
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PBIX = ROOT / "Saudi_Retail_BI_Dashboard.pbix"


def update_textbox(single_visual: dict, replacements: dict[str, str]) -> list[str]:
    changes: list[str] = []
    general = single_visual.get("objects", {}).get("general", [])
    for item in general:
        paragraphs = item.get("properties", {}).get("paragraphs", [])
        for paragraph in paragraphs:
            for run in paragraph.get("textRuns", []):
                old_value = run.get("value")
                if old_value in replacements:
                    new_value = replacements[old_value]
                    run["value"] = new_value
                    changes.append(f"{old_value} -> {new_value}")
    return changes


def rename_measure_display(visual: dict, query_name: str, new_label: str) -> bool:
    changed = False

    config = json.loads(visual.get("config", "{}"))
    single_visual = config.get("singleVisual", {})
    for selected in single_visual.get("prototypeQuery", {}).get("Select", []):
        if (
            selected.get("Name") == query_name
            and selected.get("NativeReferenceName") != new_label
        ):
            selected["NativeReferenceName"] = new_label
            changed = True

    properties = single_visual.setdefault("columnProperties", {})
    if query_name in properties:
        if properties[query_name].get("displayName") != new_label:
            properties[query_name]["displayName"] = new_label
            changed = True
    elif any(
        item.get("Name") == query_name
        for item in single_visual.get("prototypeQuery", {}).get("Select", [])
    ):
        properties[query_name] = {"displayName": new_label}
        changed = True

    if changed:
        visual["config"] = json.dumps(config, separators=(",", ":"))

    if "query" in visual:
        query = json.loads(visual["query"])
        query_changed = False
        commands = query.get("Commands", [])
        for command in commands:
            selects = (
                command.get("SemanticQueryDataShapeCommand", {})
                .get("Query", {})
                .get("Select", [])
            )
            for selected in selects:
                if (
                    selected.get("Name") == query_name
                    and selected.get("NativeReferenceName") != new_label
                ):
                    selected["NativeReferenceName"] = new_label
                    query_changed = True
        if query_changed:
            visual["query"] = json.dumps(query, separators=(",", ":"))
            changed = True

    if "dataTransforms" in visual:
        transforms = json.loads(visual["dataTransforms"])
        transform_changed = False
        for selected in transforms.get("queryMetadata", {}).get("Select", []):
            if (
                selected.get("Name") == query_name
                and selected.get("Restatement") != new_label
            ):
                selected["Restatement"] = new_label
                transform_changed = True
        for selected in transforms.get("selects", []):
            if (
                selected.get("queryName") == query_name
                and selected.get("displayName") != new_label
            ):
                selected["displayName"] = new_label
                transform_changed = True
        if transform_changed:
            visual["dataTransforms"] = json.dumps(transforms, separators=(",", ":"))
            changed = True

    return changed


def disable_log_axis(single_visual: dict) -> bool:
    changed = False
    for axis in single_visual.get("objects", {}).get("valueAxis", []):
        literal = (
            axis.get("properties", {})
            .get("logAxisScale", {})
            .get("expr", {})
            .get("Literal", {})
        )
        if literal.get("Value") == "true":
            literal["Value"] = "false"
            changed = True
    return changed


def uses_linear_axis(single_visual: dict) -> bool:
    for axis in single_visual.get("objects", {}).get("valueAxis", []):
        value = (
            axis.get("properties", {})
            .get("logAxisScale", {})
            .get("expr", {})
            .get("Literal", {})
            .get("Value")
        )
        if value == "false":
            return True
    return False


with zipfile.ZipFile(PBIX, "r") as source:
    infos = source.infolist()
    payloads = {info.filename: source.read(info.filename) for info in infos}

layout = json.loads(payloads["Report/Layout"].decode("utf-16le"))
changes: list[str] = []
executive_branch_axis_linear = False

for section in layout["sections"]:
    original_page = section["displayName"].strip()
    if original_page == "Inventory Performance Analysis":
        section["displayName"] = "Inventory & Operations Analysis"
        changes.append("Renamed the inventory page")

    page = section["displayName"].strip()
    for visual in section.get("visualContainers", []):
        config = json.loads(visual.get("config", "{}"))
        single_visual = config.get("singleVisual", {})
        visual_type = single_visual.get("visualType")

        text_changes = update_textbox(
            single_visual,
            {
                "Retail Sales Performance Dashboard": "Saudi Retail BI Dashboard",
                "• Top 3 products generate over 30% of total sales.": (
                    "• Top 5 products generate ~26% of total sales."
                ),
                "Inventory Performance Analysis": "Inventory & Operations Analysis",
            },
        )
        if text_changes:
            visual["config"] = json.dumps(config, separators=(",", ":"))
            changes.extend(f"{page}: {item}" for item in text_changes)

        if (
            page == "Executive Overview"
            and visual_type == "columnChart"
            and "branches.Branch_Name" in visual.get("config", "")
        ):
            if disable_log_axis(single_visual):
                visual["config"] = json.dumps(config, separators=(",", ":"))
                changes.append("Executive Overview: changed branch chart to a linear axis")
            executive_branch_axis_linear = uses_linear_axis(single_visual)

        combined = " ".join(
            visual.get(key, "") for key in ("config", "query", "dataTransforms")
        )
        if (
            page == "Sales Performance Analysis"
            and "Previous Month Revenue" in combined
            and rename_measure_display(
                visual,
                "Pg2.Previous Month Revenue2",
                "Prior Period Revenue",
            )
        ):
            changes.append("Sales Performance: relabeled the comparison baseline")

final_layout_text = json.dumps(layout, separators=(",", ":"), ensure_ascii=False)
required_fragments = [
    "Top 5 products generate ~26% of total sales",
    "Saudi Retail BI Dashboard",
    "Inventory & Operations Analysis",
    "Prior Period Revenue",
]
for fragment in required_fragments:
    if fragment not in final_layout_text:
        raise RuntimeError(f"Expected layout state is missing: {fragment}")

for obsolete_fragment in [
    "Top 3 products generate over 30% of total sales",
    "Retail Sales Performance Dashboard",
]:
    if obsolete_fragment in final_layout_text:
        raise RuntimeError(f"Obsolete dashboard text remains: {obsolete_fragment}")

if not executive_branch_axis_linear:
    raise RuntimeError("The Executive Overview branch chart is not using a linear axis")

payloads["Report/Layout"] = final_layout_text.encode("utf-16le")

file_descriptor, temporary_name = tempfile.mkstemp(
    suffix=".pbix", dir=PBIX.parent
)
os.close(file_descriptor)
temporary = Path(temporary_name)

try:
    with zipfile.ZipFile(temporary, "w") as target:
        for info in infos:
            target.writestr(info, payloads[info.filename])

    with zipfile.ZipFile(temporary, "r") as check:
        if check.testzip() is not None:
            raise RuntimeError("The rebuilt PBIX archive failed integrity checks")
        json.loads(check.read("Report/Layout").decode("utf-16le"))

    os.replace(temporary, PBIX)
finally:
    temporary.unlink(missing_ok=True)

print("\n".join(changes) if changes else "Dashboard layout already up to date")
