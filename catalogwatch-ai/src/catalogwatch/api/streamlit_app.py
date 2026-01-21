"""Minimal Streamlit dashboard for Phase 1 demo."""
from __future__ import annotations

# Ensure project root and `src/` are on sys.path so the app can be run with
# `streamlit run` from the project root or when Streamlit spawns a subprocess.
import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
for p in (SRC_DIR, PROJECT_ROOT):
    if p and p not in sys.path:
        sys.path.insert(0, p)

import streamlit as st
import pandas as pd
import altair as alt
import json

from catalogwatch.ingest.csv_loader import load_csv, canonicalize
from catalogwatch.eligibility.config import load_windows
from catalogwatch.eligibility.rules import explain_classification
from catalogwatch.nlp.parser import parse_ownership_notes
from catalogwatch.modeling.features import feature_from_record
from catalogwatch.modeling.scoring import simple_score
from catalogwatch.modeling.explainability import compute_contributions

import os


CFG_PATH = os.path.join("configs", "eligibility_windows.yml")


def main() -> None:
    st.set_page_config(page_title="CatalogWatch AI — Demo", layout="wide")
    st.title("CatalogWatch AI — Demo")

    st.sidebar.header("Ingest")
    sample = st.sidebar.checkbox("Load sample data", value=True)

    if sample:
        df = load_csv("data/samples/sample_catalogs.csv")
    else:
        uploaded = st.sidebar.file_uploader("Upload CSV", type=["csv"]) 
        if uploaded is None:
            st.info("Upload a CSV or check 'Load sample data' to proceed.")
            return
        df = pd.read_csv(uploaded)

    df = canonicalize(df)

    windows = load_windows(CFG_PATH)

    # annotate
    annotated = []
    for _, row in df.iterrows():
        release_year_val = int(row.release_year) if pd.notna(row.release_year) else None
        expl = explain_classification(release_year_val, None, windows)
        nlp = parse_ownership_notes(row.ownership_notes)
        rec = dict(row)
        rec.update(expl)
        rec["ownership_signals"] = nlp.get("signals")
        rec["ownership_confidence"] = nlp.get("confidence")

        # features and score
        feats = feature_from_record({
            **rec,
            "years_since_release": expl.get("years_since_release"),
            "ownership_signals": nlp.get("signals"),
        })
        rec["features"] = feats
        rec["score"] = simple_score(feats)
        rec["explainability"] = compute_contributions(feats)

        annotated.append(rec)

    adf = pd.DataFrame(annotated)

    st.header("Overview")
    st.metric("Total catalogs", len(adf))

    st.subheader("Eligibility distribution")
    dist = adf["eligibility_window"].value_counts().reset_index()
    dist.columns = ["window", "count"]
    st.bar_chart(dist.set_index("window"))

    st.subheader("Top catalogs approaching eligibility")
    # sort by years_since_release desc
    top = adf.sort_values(by="years_since_release", ascending=False).head(10)
    st.dataframe(top[["catalog_id", "artist_name", "track_title", "release_year", "eligibility_window", "ownership_confidence", "score"]])

    st.subheader("Catalog detail")
    sel = st.selectbox("Select catalog", options=adf["catalog_id"].tolist())
    detail = adf[adf["catalog_id"] == sel].iloc[0]
    detail_obj = {
        "catalog_id": detail["catalog_id"],
        "artist_name": detail["artist_name"],
        "track_title": detail["track_title"],
        "release_year": int(detail["release_year"]) if pd.notna(detail["release_year"]) else None,
        "eligibility_window": detail.get("eligibility_window"),
        "ownership_signals": detail.get("ownership_signals"),
        "ownership_confidence": detail.get("ownership_confidence"),
        "score": detail.get("score"),
    }

    st.markdown("**Catalog summary**")
    st.json(detail_obj)

    st.markdown("**Ownership notes & evidence**")
    st.write(detail.get("ownership_notes"))
    st.markdown("Evidence:")
    evidence = parse_ownership_notes(detail.get("ownership_notes", ""))
    for ev in evidence.get("evidence", []):
        st.write(f"- {ev}")

    st.markdown("**Explainability (feature contributions)**")
    expl = detail.get("explainability", {})
    # show each contribution in a small table and horizontal bar chart
    expl_df = pd.DataFrame(
        [
            {"component": "eligibility", "value": expl.get("eligibility_value"), "contribution": expl.get("eligibility_contribution")},
            {"component": "ownership_clarity", "value": expl.get("ownership_clarity_value"), "contribution": expl.get("ownership_contribution")},
            {"component": "exclusive_penalty", "value": expl.get("exclusive_penalty_value"), "contribution": expl.get("exclusive_contribution")},
        ]
    )
    st.table(expl_df)
    st.metric("Composite score", f"{expl.get('total', 0):.3f}")

    # Horizontal bar chart for contributions (investor-friendly)
    try:
        # color map and accent color (muted blue)
        COLOR_MAP = {
            "eligibility": "#4e79a7",
            "ownership_clarity": "#7bb274",
            "exclusive_penalty": "#e15759",
        }

        # create a formatted label for each contribution (e.g., +0.42)
        def fmt_label(x):
            try:
                v = float(x)
                sign = "+" if v >= 0 else ""
                return f"{sign}{v:.2f}"
            except Exception:
                return ""

        expl_df = expl_df.copy()
        expl_df["label"] = expl_df["contribution"].apply(fmt_label)
        expl_df["color"] = expl_df["component"].map(COLOR_MAP)

        chart = (
            alt.Chart(expl_df)
            .mark_bar()
            .encode(
                x=alt.X("contribution:Q", title="Contribution"),
                y=alt.Y("component:N", sort="-x", title="Component"),
                color=alt.Color("component:N", scale=alt.Scale(domain=list(COLOR_MAP.keys()), range=list(COLOR_MAP.values())), legend=None),
                tooltip=["component", "value", "contribution"],
            )
            .properties(width=600, height=150)
        )

        # add value labels at end of bars
        text = (
            alt.Chart(expl_df)
            .mark_text(align="left", dx=5, dy=0)
            .encode(
                x=alt.X("contribution:Q"),
                y=alt.Y("component:N", sort="-x"),
                text=alt.Text("label:N"),
            )
        )

        st.altair_chart((chart + text), use_container_width=True)

        # manual legend (small, minimal)
        legend_md = (
            f"<div style='display:flex;gap:12px;align-items:center;margin-top:6px;'>"
            f"<div style='display:flex;gap:8px;align-items:center;'>"
            f"<span style='display:inline-block;width:14px;height:14px;background:{COLOR_MAP['eligibility']};margin-right:6px;border-radius:2px;'></span>Eligibility proximity</div>"
            f"<div style='display:flex;gap:8px;align-items:center;'>"
            f"<span style='display:inline-block;width:14px;height:14px;background:{COLOR_MAP['ownership_clarity']};margin-right:6px;border-radius:2px;'></span>Ownership clarity</div>"
            f"<div style='display:flex;gap:8px;align-items:center;'>"
            f"<span style='display:inline-block;width:14px;height:14px;background:{COLOR_MAP['exclusive_penalty']};margin-right:6px;border-radius:2px;'></span>Penalties</div>"
            f"</div>"
        )
        st.markdown(legend_md, unsafe_allow_html=True)
    except Exception:
        # If altair rendering fails, continue without chart
        pass

    # Selected-catalog CSV export (single-record) — labeled as requested
    try:
        single = detail.to_dict()
        # serialize nested objects as JSON strings for CSV
        for k in ["ownership_signals", "features", "explainability", "ingestion_metadata"]:
            if k in single:
                single[k] = json.dumps(single[k]) if single[k] is not None else ""
        single_df = pd.DataFrame([single])
        single_csv = single_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download enriched CSV (Phase-1 output)",
            data=single_csv,
            file_name=f"catalog_{single.get('catalog_id', 'record')}_enriched.csv",
            mime="text/csv",
        )
    except Exception:
        pass


if __name__ == "__main__":
    main()
