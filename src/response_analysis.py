# src/response_analysis.py

"""
Gluco-X Data Science Challenge

Task 2: Fatigue Analysis

This module analyzes how patient responsiveness changes as they receive more nudges.

Instruction alignment:
- "Visualize the relationship between Nudge Count and Response Rate"
- Identify whether response probability decreases after many nudges (nudge fatigue)
"""

import pandas as pd
import matplotlib.pyplot as plt


class ResponseAnalysis:
    """
    Class to compute nudge numbers, response rates, and visualize fatigue curves.
    """

    def __init__(self, df_nudges: pd.DataFrame):
        # Copy of enriched nudges dataset (output from Task 1)
        self.df_nudges = df_nudges.copy()

        # Placeholder for aggregated response rates
        self.response_rate = None

    def compute_nudge_numbers(self) -> pd.DataFrame:
        """
        Assign a sequential nudge number per patient.

        This represents the order in which nudges were received by each patient
        and is critical to analyze fatigue over time.

        Returns:
            pd.DataFrame: Nudges with an added 'nudge_number' column
        """
        # For each patient, assign cumulative count of nudges (1, 2, 3, ...)
        self.df_nudges['nudge_number'] = (
            self.df_nudges.groupby('patient_id').cumcount() + 1
        )

        return self.df_nudges

    def compute_response_rate(self) -> pd.DataFrame:
        """
        Compute average response rate per nudge number.

        This measures the probability of responding after receiving the N-th nudge.

        Returns:
            pd.DataFrame: Response rate per nudge number
        """
        # Ensure nudge numbers exist before aggregation
        if 'nudge_number' not in self.df_nudges.columns:
            self.compute_nudge_numbers()

        # Aggregate mean response (responded = 1 or 0)
        # This gives the probability of response per nudge number
        self.response_rate = (
            self.df_nudges
            .groupby('nudge_number')['responded']
            .mean()
            .reset_index()
        )

        return self.response_rate

    def plot_fatigue_curve(self):
        """
        Plot fatigue curve: Response Rate vs Nudge Number.

        This visualization helps identify whether response probability decreases
        as patients receive more nudges (nudge fatigue hypothesis).

        Returns:
            matplotlib.figure.Figure: Figure object for further use (e.g., PDF report)
        """
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Plot response rate curve
        ax.plot(
            self.response_rate['nudge_number'],
            self.response_rate['responded'],
            marker='o'
        )

        # Label axes and title for clarity
        ax.set_xlabel('Nudge Number')
        ax.set_ylabel('Response Rate')
        ax.set_title('Nudge Fatigue Curve')

        # Add grid for better readability
        ax.grid(True)

        return fig