# src/nudge_assignment.py

"""
Gluco-X Data Science Challenge

Task 1: Response Time Pipeline

This module assigns glucose measurements to nudges.

Instruction alignment:
- A measurement is considered a response if it occurs within 4 hours of a nudge
- If multiple nudges exist before a measurement, assign it to the MOST RECENT one
"""

import pandas as pd


class NudgeAssigner:
    """
    Class to assign glucose measurements to nudges and compute response information.
    """

    def __init__(self, df_logs: pd.DataFrame, df_nudges: pd.DataFrame):
        # Full event log (nudges + measurements)
        self.df_logs = df_logs

        # Copy of nudges only (this will be enriched with response info)
        self.df_nudges = df_nudges.copy()

        # Initialize output columns
        self.df_nudges['measurement_time'] = None
        self.df_nudges['response_time_hours'] = None
        self.df_nudges['responded'] = 0  # 1 if responded, 0 otherwise

    def assign_responses(self, max_hours: float = 4) -> pd.DataFrame:
        """
        Assign measurements to nudges based on business rules.

        Rules:
        - A response must occur within `max_hours` (default: 4 hours)
        - Each measurement is assigned to the most recent prior nudge
        - Each nudge can receive at most one response

        Returns:
            pd.DataFrame: Nudges with response information
        """

        # Process each patient independently
        # This ensures we only match events within the same patient timeline
        for patient_id, group in self.df_logs.groupby('patient_id'):

            # Sort events chronologically (critical for correct attribution)
            group = group.sort_values('timestamp')

            # Track the most recent nudge for this patient
            last_nudge_index = None

            # Iterate through events in time order
            for idx, row in group.iterrows():

                # Case 1: Nudge is sent → update the "most recent nudge"
                if row['event_type'] == 'nudge_sent':
                    last_nudge_index = idx

                # Case 2: Measurement occurs → attempt to assign it
                elif row['event_type'] == 'measurement_logged' and last_nudge_index is not None:

                    # Get timestamps
                    nudge_time = self.df_logs.loc[last_nudge_index, 'timestamp']
                    measurement_time = row['timestamp']

                    # Compute time difference in hours
                    time_diff = (measurement_time - nudge_time).total_seconds() / 3600

                    # Apply 4-hour response window rule (core requirement)
                    if time_diff <= max_hours:

                        # Identify the corresponding nudge in df_nudges
                        nudge_event_id = self.df_logs.loc[last_nudge_index, 'event_id']
                        nudge_idx = self.df_nudges[
                            self.df_nudges['event_id'] == nudge_event_id
                        ].index[0]

                        # Assign response information to the nudge
                        self.df_nudges.loc[nudge_idx, 'measurement_time'] = measurement_time
                        self.df_nudges.loc[nudge_idx, 'response_time_hours'] = time_diff
                        self.df_nudges.loc[nudge_idx, 'responded'] = 1

                        # Reset last_nudge_index to enforce:
                        # "Each measurement is assigned to ONLY ONE (most recent) nudge"
                        last_nudge_index = None

        return self.df_nudges