import json
import time
import random
from pathlib import Path
from typing import Dict, Any
import logging
from datetime import datetime
import csv
import os
import pandas as pd

from src.auth.instagram_client import InstagramClient

class DMSender:
    def __init__(self, client: InstagramClient, templates_file: str):
        self.client = client
        self.templates_file = Path(templates_file)
        self.logger = logging.getLogger(__name__)
        self.templates = self._load_templates()
        self.log_file = Path("logs/sent_log.csv")
        self._ensure_log_file()

    def send_message(self, user: Dict[str, Any]) -> bool:
        """
        Send a message to a user based on their category
        """
        try:
            username = user["username"]
            category = user["category"]

            # Get template for category
            template = self._get_template(category)
            if not template:
                self.logger.error(f"No template found for category: {category}")
                return False

            # Format message with variables if any
            message = self._format_message(template, user)

            # Add random delay before sending
            self._random_delay()

            # Send the message
            success = self.client.send_dm(username, message)

            # Log the attempt
            self._log_attempt(username, category, success)

            return success

        except Exception as e:
            self.logger.error(f"Error sending message: {str(e)}")
            return False

    def _load_templates(self) -> Dict[str, Any]:
        """
        Load message templates from JSON file
        """
        try:
            if not self.templates_file.exists():
                self.logger.error(f"Templates file not found: {self.templates_file}")
                return {}

            with open(self.templates_file, encoding='utf-8') as f:
                templates = json.load(f)
            
            self.logger.info(f"Loaded templates for categories: {', '.join(templates.keys())}")
            return templates

        except Exception as e:
            self.logger.error(f"Error loading templates: {str(e)}")
            return {}

    def _get_template(self, category: str, template_name: str = None) -> Dict[str, Any]:
        """
        Get a template for the given category and template name
        If template_name is not provided, randomly select one
        """
        try:
            category_templates = self.templates.get(category, {})
            if not category_templates:
                return None

            if template_name:
                return category_templates.get(template_name)
            
            # Randomly select a template from available ones
            template_key = random.choice(list(category_templates.keys()))
            return category_templates[template_key]

        except Exception as e:
            self.logger.error(f"Error getting template: {str(e)}")
            return None

    def _format_message(self, template: Dict[str, Any], user: Dict[str, Any]) -> str:
        """
        Format message template with variables
        """
        try:
            message = template["text"]
            variables = template.get("variables", [])

            # Replace variables in message
            for var in variables:
                if var in user:
                    message = message.replace(f"{{{var}}}", str(user[var]))

            return message

        except Exception as e:
            self.logger.error(f"Error formatting message: {str(e)}")
            return template["text"]  # Return unformatted template as fallback

    def _random_delay(self) -> None:
        """
        Add a random delay between messages
        """
        min_delay = int(os.getenv("MIN_DELAY_SECONDS", "30"))
        max_delay = int(os.getenv("MAX_DELAY_SECONDS", "90"))
        delay = random.randint(min_delay, max_delay)
        time.sleep(delay)

    def _ensure_log_file(self) -> None:
        """
        Ensure log file exists with headers
        """
        try:
            self.log_file.parent.mkdir(exist_ok=True)
            
            if not self.log_file.exists():
                with open(self.log_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["timestamp", "username", "category", "status", "error"])

        except Exception as e:
            self.logger.error(f"Error ensuring log file: {str(e)}")

    def _log_attempt(self, username: str, category: str, success: bool) -> None:
        """
        Log message sending attempt
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = "success" if success else "failed"
            error = "" if success else "Message sending failed"

            with open(self.log_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, username, category, status, error])

        except Exception as e:
            self.logger.error(f"Error logging attempt: {str(e)}")

    def get_daily_sent_count(self) -> int:
        """
        Get count of messages sent today
        """
        try:
            if not self.log_file.exists():
                return 0

            df = pd.read_csv(self.log_file)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            today = datetime.now().date()
            return len(df[df["timestamp"].dt.date == today])

        except Exception as e:
            self.logger.error(f"Error getting daily sent count: {str(e)}")
            return 0 