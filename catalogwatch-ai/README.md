# CatalogWatch AI — Phase 1 (MVP)

CatalogWatch AI identifies music catalogs approaching U.S. copyright termination eligibility.

This repository contains a Phase 1 proof-of-concept scaffold focused on:

- Ingesting catalog metadata (CSV)
- Config-driven eligibility detection
- Lightweight NLP for ownership notes
- A neural-ready scoring scaffold
- A minimal Streamlit dashboard

Goals: clarity, explainability, and an architecture that scales into advanced AI and automation.

See `requirements.txt` for dependencies and `configs/` for configuration.

How to run (dev):

1. Create a virtualenv with Python 3.10+ and install requirements:

   pip install -r requirements.txt

2. Run tests:

   pytest -q

3. Run the demo Streamlit app:

   streamlit run src/catalogwatch/api/streamlit_app.py

Notes:
- This is a non-production, local demo. No external APIs are called.
- The tool is not legal advice.
