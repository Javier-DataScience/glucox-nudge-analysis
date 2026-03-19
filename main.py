# main.py

"""
Gluco-X Data Science Challenge

Main execution script for the Nudge Effectiveness Analysis.

Pipeline Overview:
1. Task 1: Response Time Pipeline
   - Load and parse data
   - Assign glucose measurements to nudges

2. Task 2: Fatigue Analysis
   - Compute response rate per nudge number
   - Visualize fatigue curve

3. Task 3: Executive Summary
   - Generate PDF report with findings and recommendations

This script orchestrates the full workflow end-to-end.
"""

from src.data_loader import DataLoader
from src.nudge_assignment import NudgeAssigner
from src.response_analysis import ResponseAnalysis
from report_generator import generate_pdf_report


def main():
    # --- Step 1: Load data (Task 1: Parsing logs) ---
    # Initialize data loader with relative paths (portable across environments)
    data_loader = DataLoader(
        patient_file='data/patient_registry.csv',
        logs_file='data/app_logs.jsonl'
    )

    # Load datasets
    df_patients = data_loader.load_patients()
    df_logs = data_loader.load_logs()
    print("Data loaded successfully.")

    # --- Step 2: Initialize nudges dataset ---
    # Filter only nudge events (these will be enriched with response info)
    df_nudges = df_logs[df_logs['event_type'] == 'nudge_sent'].copy()

    # --- Step 3: Assign measurements to nudges (Task 1 core logic) ---
    # Apply business rules:
    # - Response within 4 hours
    # - Assign to most recent nudge only
    assigner = NudgeAssigner(df_logs=df_logs, df_nudges=df_nudges)
    df_nudges_assigned = assigner.assign_responses()
    print("Nudge assignment completed.")

    # --- Step 4: Fatigue Analysis (Task 2) ---
    # Analyze how response rate changes with number of nudges
    analysis = ResponseAnalysis(df_nudges=df_nudges_assigned)

    # Compute sequential nudge number per patient
    analysis.compute_nudge_numbers()

    # Compute response probability per nudge number
    response_rate = analysis.compute_response_rate()
    print("Response rates computed:\n", response_rate.head(15))

    # Generate fatigue curve (response rate vs nudge number)
    fatigue_fig = analysis.plot_fatigue_curve()

    # --- Step 5: Generate PDF report (Task 3) ---
    # Create executive summary with findings and visualization
    generate_pdf_report(df_nudges_assigned, fatigue_fig, output_path="report.pdf")
    print("PDF report generated successfully.")


if __name__ == "__main__":
    main()