# src/data_loader.py

"""
Gluco-X Data Science Challenge

Task 1: Response Time Pipeline

This module is responsible for:
- Loading patient registry data (CSV)
- Parsing raw app logs (JSONL format)
- Extracting relevant fields from nested payload data

Instruction alignment:
- "Parses the JSON logs"
"""

import pandas as pd


class DataLoader:
    """
    Class to load and preprocess Gluco-X patient and log data.
    """

    def __init__(self, patient_file: str, logs_file: str):
        # Store file paths (using relative paths for portability)
        self.patient_file = patient_file
        self.logs_file = logs_file

    def load_patients(self) -> pd.DataFrame:
        """
        Load patient registry CSV file.

        Returns:
            pd.DataFrame: Patient-level information (e.g., age_group, risk_segment)
        """
        df_patients = pd.read_csv(self.patient_file)
        return df_patients

    def load_logs(self) -> pd.DataFrame:
        """
        Load app logs (JSON Lines format) and preprocess key fields.

        Steps:
        - Parse JSONL file
        - Convert timestamp to datetime
        - Extract relevant fields from payload
        - Sort events chronologically per patient

        Returns:
            pd.DataFrame: Cleaned and structured log data
        """
        # Load JSON lines file (each line is a JSON object)
        df_logs = pd.read_json(self.logs_file, lines=True)

        # Convert timestamp column to datetime for time-based operations
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])

        # Extract nudge_type from payload (only exists for nudge_sent events)
        df_logs['nudge_type'] = df_logs['payload'].apply(
            lambda x: x.get('nudge_type') if 'nudge_type' in x else None
        )

        # Extract glucose_value from payload (only exists for measurement_logged events)
        df_logs['glucose_value'] = df_logs['payload'].apply(
            lambda x: x.get('glucose_value') if 'glucose_value' in x else None
        )

        # Sort logs by patient and time to ensure correct chronological processing
        # This is critical for assigning measurements to the most recent nudge
        df_logs = df_logs.sort_values(['patient_id', 'timestamp']).reset_index(drop=True)

        return df_logs