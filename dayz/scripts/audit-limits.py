#!/usr/bin/env python3
"""Audit DayZ CE category, tag, usage, and value references."""

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

FLAG_SECTIONS = {
    "category": "categories",
    "tag": "tags",
    "usage": "usageflags",
    "value": "valueflags",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find duplicate and undefined cfglimitsdefinition flags."
    )
    parser.add_argument(
        "mission",
        type=Path,
        help="Mission directory containing cfglimitsdefinition.xml",
    )
    return parser.parse_args()


def relative(path, root):
    return path.relative_to(root).as_posix()


def main():
    args = parse_args()
    mission = args.mission.resolve()
    limits_path = mission / "cfglimitsdefinition.xml"

    if not limits_path.is_file():
        print(f"ERROR: missing {limits_path}", file=sys.stderr)
        return 2

    try:
        limits_root = ET.parse(limits_path).getroot()
    except (OSError, ET.ParseError) as error:
        print(f"ERROR: cannot parse {limits_path}: {error}", file=sys.stderr)
        return 2

    definitions = {}
    duplicates = {}
    for flag, section_name in FLAG_SECTIONS.items():
        section = limits_root.find(section_name)
        names = []
        if section is not None:
            for element in section.findall(flag):
                name = element.get("name")
                if name:
                    names.append(name)
        definitions[flag] = set(names)
        duplicates[flag] = sorted(
            name for name, count in Counter(names).items() if count > 1
        )

    references = {
        flag: defaultdict(set) for flag in FLAG_SECTIONS
    }
    parse_errors = []
    for path in sorted(mission.rglob("*.xml")):
        if path.name.lower() == "cfglimitsdefinition.xml":
            continue
        try:
            xml_root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as error:
            parse_errors.append((relative(path, mission), str(error)))
            continue

        for element in xml_root.iter():
            flag = element.tag.rsplit("}", 1)[-1]
            name = element.get("name")
            if flag in references and name:
                references[flag][name].add(relative(path, mission))

    undefined = {
        flag: sorted(set(references[flag]) - definitions[flag])
        for flag in FLAG_SECTIONS
    }
    unused = {
        flag: sorted(definitions[flag] - set(references[flag]))
        for flag in FLAG_SECTIONS
    }

    print(f"Mission: {mission}")
    for flag in FLAG_SECTIONS:
        print(
            f"{flag}: {len(definitions[flag])} defined, "
            f"{len(references[flag])} referenced, "
            f"{len(undefined[flag])} undefined, "
            f"{len(duplicates[flag])} duplicated"
        )

    for flag in FLAG_SECTIONS:
        for name in duplicates[flag]:
            print(f"ERROR duplicate {flag}: {name}")
        for name in undefined[flag]:
            paths = ", ".join(sorted(references[flag][name]))
            print(f"ERROR undefined {flag}: {name} ({paths})")

    for path, error in parse_errors:
        print(f"ERROR malformed XML: {path}: {error}")

    for flag in FLAG_SECTIONS:
        if unused[flag]:
            print(f"NOTE unused {flag}: {', '.join(unused[flag])}")

    has_errors = bool(parse_errors) or any(duplicates.values()) or any(undefined.values())
    print("Result: FAIL" if has_errors else "Result: PASS")
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
