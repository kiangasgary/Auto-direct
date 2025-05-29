import os
import time
import json
from pathlib import Path
from typing import Optional
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ClientError
import logging

class InstagramClient:
    def __init__(self):
        self.client = Client()
        self.username = os.getenv("IG_USERNAME")
        self.password = os.getenv("IG_PASSWORD")
        self.session_file = Path("data/session.json")
        self.logger = logging.getLogger(__name__)

    def login(self) -> bool:
        """
        Login to Instagram using stored session or credentials
        """
        try:
            if self._load_session():
                self.logger.info("Logged in using saved session")
                return True

            if not self.username or not self.password:
                self.logger.error("Instagram credentials not found in environment variables")
                return False

            self.logger.info("Logging in with credentials...")
            self.client.login(self.username, self.password)
            self._save_session()
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return False

    def send_dm(self, username: str, message: str) -> bool:
        """
        Send a direct message to a user
        """
        try:
            # Get user ID from username
            user_id = self.client.user_id_from_username(username)
            if not user_id:
                self.logger.error(f"Could not find user ID for username: {username}")
                return False

            # Send the message
            self.client.direct_send(message, [user_id])
            self.logger.info(f"Successfully sent message to {username}")
            return True

        except LoginRequired:
            self.logger.error("Session expired, attempting to relogin...")
            if self.login():
                return self.send_dm(username, message)
            return False

        except ClientError as e:
            self.logger.error(f"Failed to send message to {username}: {str(e)}")
            return False

        except Exception as e:
            self.logger.error(f"Unexpected error sending message to {username}: {str(e)}")
            return False

    def _load_session(self) -> bool:
        """
        Load saved session data
        """
        try:
            if not self.session_file.exists():
                return False

            with open(self.session_file) as f:
                session_data = json.load(f)

            self.client.set_settings(session_data)
            self.client.login(self.username, self.password)
            return True

        except Exception as e:
            self.logger.error(f"Failed to load session: {str(e)}")
            return False

    def _save_session(self) -> None:
        """
        Save current session data
        """
        try:
            session_data = self.client.get_settings()
            
            # Ensure the data directory exists
            self.session_file.parent.mkdir(exist_ok=True)
            
            with open(self.session_file, "w") as f:
                json.dump(session_data, f)
            
            self.logger.info("Session saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save session: {str(e)}")

    def logout(self) -> bool:
        """
        Logout from Instagram and clear session
        """
        try:
            self.client.logout()
            if self.session_file.exists():
                self.session_file.unlink()
            return True
        except Exception as e:
            self.logger.error(f"Logout failed: {str(e)}")
            return False 