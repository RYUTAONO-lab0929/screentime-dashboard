#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
from datetime import datetime
from typing import Optional
import json

# NOTE: 実際はDBへ書き込み/検証/補完を実装。ここでは雛形。


MAPPING = {
    "date": "date",
    "participant_id": "participant_id",
    "category": "category",
    "app_bundle_id": "app_bundle_id",
    "total_minutes": "total_minutes",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    p.add_argument("--format", choices=["csv", "json"], default="csv")
    return p.parse_args()


def import_csv(path: str):
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = {dst: row.get(src) for src, dst in MAPPING.items()}
            # 欠損補完例
            if not item.get("total_minutes"):
                item["total_minutes"] = 0
            out.append(item)
    print(json.dumps({"records": out[:5], "count": len(out)}, ensure_ascii=False))


def import_json(path: str):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps({"records": data[:5], "count": len(data)}, ensure_ascii=False))


if __name__ == "__main__":
    args = parse_args()
    if args.format == "csv":
        import_csv(args.file)
    else:
        import_json(args.file)
