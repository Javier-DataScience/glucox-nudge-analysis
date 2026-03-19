# report_generator.py

"""
Gluco-X Data Science Challenge

Task 3: Executive Summary

Generates a clean, concise PDF report:
- Task 1: Response Time Pipeline
- Task 2: Fatigue Analysis
- Business insights
- AI Disclosure
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def generate_pdf_report(df_nudges, fatigue_curve_fig, output_path="report.pdf"):
    """
    Generate an executive summary PDF optimized to fit cleanly on one page.
    """

    with PdfPages(output_path) as pdf:

        # --- Page 1: Executive Summary ---
        plt.figure(figsize=(8.27, 11.69))  # A4
        plt.axis('off')

        report_text = """
Gluco-X Nudge Effectiveness Analysis
Executive Summary

1. Business Context
-----------------------------------
Gluco-X uses push notifications ("nudges") to encourage patients to log glucose levels.
Two types are used: Gentle Reminder (soft prompt) and Urgent Alert (more direct, medical tone).
The Product Team suspects "nudge fatigue", where repeated nudges reduce responsiveness.

2. Methodology (Task 1: Response Time Pipeline)
-----------------------------------
- Parsed raw app logs (JSONL) and patient registry data (CSV)
- Defined a response as a glucose measurement within 4 hours of a nudge
- Assigned each measurement to the MOST RECENT preceding nudge

This produced a dataset linking each nudge to:
- Whether the patient responded
- Time to response

3. Key Findings (Task 2: Fatigue Analysis)
-----------------------------------
We analyzed how response rate changes as patients receive an increasing number of nudges.

- Nudges 1–15: Response rate remains stable (~50%–60%)
- Nudges 15–24: Response rate declines (~20%–30%)
- After ~24 nudges: Response rate approaches 0%

Note: This analysis focuses on overall response behavior. Further segmentation
by nudge type (Gentle vs Urgent) could provide deeper insights.

4. Interpretation
-----------------------------------
The results show clear evidence of nudge fatigue:

- Initially, patients respond to nudges
- Over time, repeated exposure reduces responsiveness
- Eventually, nudges lose effectiveness

5. Recommendations
-----------------------------------
- Limit the total number of nudges per patient (avoid excessive exposure)
- Introduce cooldown periods after repeated nudges
- Personalize nudging frequency based on patient behavior
- Use Urgent Alerts more selectively for high-risk patients, avoiding overuse
- Evaluate the effectiveness of Gentle Reminders vs Urgent Alerts over time

6. Conclusion
-----------------------------------
Nudges drive engagement early on, but their effectiveness declines significantly
with overuse. A more targeted and adaptive strategy is recommended.

7. AI Disclosure
-----------------------------------
AI tools (ChatGPT) were used to assist with:
- Structuring the data pipeline and modular code
- Refining logic and improving code clarity
- Drafting explanations and report structure

All outputs were reviewed, validated, and adapted to ensure correctness
and alignment with the problem requirements.
"""

        plt.text(0.05, 0.95, report_text, ha='left', va='top', fontsize=10, wrap=True)

        pdf.savefig()
        plt.close()

        # --- Page 2: Fatigue Curve ---
        pdf.savefig(fatigue_curve_fig)
        plt.close(fatigue_curve_fig)

    print(f"PDF report saved as {output_path}")