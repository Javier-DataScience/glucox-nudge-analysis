# GlucoX Nudge Analysis

This repository contains the Gluco-X Nudge Effectiveness Analysis project.

## Project Overview
The project analyzes how patients respond to nudges (push notifications) in the Gluco-X app, computing response times and fatigue.

## Structure
- `src/` — Python modules (`data_loader.py`, `nudge_assignment.py`, `response_analysis.py`)
- `main.py` — Main script to run the analysis and generate PDF report
- `report_generator.py` — PDF report generator
- `data/` — CSV and JSONL input files
- `requirements.txt` — Python dependencies
- `report.pdf` — Generated report

## Python Environment
- Python 3.10+
- Install dependencies:

```bash
pip install -r requirements.txt

## How to Run

1. Ensure data/ folder is present.
2. Run the main script: python main.py

A PDF report (report.pdf) will be generated automatically.

Notes

All paths in the code are relative.

This project was developed using AI tools for code suggestions (ChatGPT), with careful validation and customization.