import pandas as pd
from typing import List, Dict, Any
import logging
from pathlib import Path

class UserLoader:
    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)
        self.logger = logging.getLogger(__name__)

    def load_users(self) -> List[Dict[str, Any]]:
        """
        Load users from CSV file and return as list of dictionaries
        """
        try:
            if not self.csv_path.exists():
                self.logger.error(f"CSV file not found: {self.csv_path}")
                return []

            # Read CSV file
            df = pd.read_csv(self.csv_path)

            # Validate required columns
            required_columns = ["username", "category", "status"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                self.logger.error(f"Missing required columns: {', '.join(missing_columns)}")
                return []

            # Filter for pending users only
            df = df[df["status"].str.lower() == "pending"]

            # Convert to list of dictionaries
            users = df.to_dict("records")
            
            self.logger.info(f"Loaded {len(users)} pending users from {self.csv_path}")
            return users

        except Exception as e:
            self.logger.error(f"Error loading users from CSV: {str(e)}")
            return []

    def update_user_status(self, username: str, new_status: str) -> bool:
        """
        Update the status of a user in the CSV file
        """
        try:
            df = pd.read_csv(self.csv_path)
            
            # Find the user and update status
            mask = df["username"] == username
            if not mask.any():
                self.logger.error(f"User not found: {username}")
                return False

            df.loc[mask, "status"] = new_status
            
            # Save back to CSV
            df.to_csv(self.csv_path, index=False)
            self.logger.info(f"Updated status for user {username} to {new_status}")
            return True

        except Exception as e:
            self.logger.error(f"Error updating user status: {str(e)}")
            return False

    def get_user_count(self) -> Dict[str, int]:
        """
        Get count of users by status
        """
        try:
            df = pd.read_csv(self.csv_path)
            status_counts = df["status"].value_counts().to_dict()
            return status_counts

        except Exception as e:
            self.logger.error(f"Error getting user counts: {str(e)}")
            return {} 