"""Simple CLI entrypoints for ingest and scoring (Phase 1)."""
from __future__ import annotations

import argparse
import pandas as pd

from catalogwatch.ingest.csv_loader import load_csv, canonicalize
from catalogwatch.eligibility.config import load_windows
from catalogwatch.eligibility.rules import explain_classification
from catalogwatch.nlp.parser import parse_ownership_notes
from catalogwatch.services.store import write_parquet


def ingest(args):
    df = load_csv(args.path)
    c = canonicalize(df)
    windows = load_windows(args.windows)

    annotated = []
    for _, row in c.iterrows():
        expl = explain_classification(int(row.release_year) if pd.notna(row.release_year) else None, None, windows)
        nlp = parse_ownership_notes(row.ownership_notes)
        rec = dict(row)
        rec.update(expl)
        rec["ownership_signals"] = nlp.get("signals")
        rec["ownership_confidence"] = nlp.get("confidence")
        annotated.append(rec)

    out_df = pd.DataFrame(annotated)
    out_path = write_parquet(out_df, name="canonical_catalogs")
    print(f"Wrote canonical dataset to: {out_path}")


def main():
    parser = argparse.ArgumentParser(prog="catalogwatch")
    sub = parser.add_subparsers(dest="cmd")

    p_ingest = sub.add_parser("ingest")
    p_ingest.add_argument("path")
    p_ingest.add_argument("--windows", default="configs/eligibility_windows.yml")

    args = parser.parse_args()
    if args.cmd == "ingest":
        ingest(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
