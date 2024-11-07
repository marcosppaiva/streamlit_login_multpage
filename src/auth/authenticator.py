from typing import Dict, Optional
from pathlib import Path

import yaml
import streamlit as st
import streamlit_authenticator as stauth
from yaml import SafeLoader
from streamlit_authenticator.utilities import LoginError


class StreamlitAuthenticator:

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config: Dict = {}
        self.authenticator: Optional[stauth.Authenticate] = None
        self._load_config()
        self._setup_authenticator()

    def _load_config(self) -> None:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f_in:
                self.config = yaml.load(f_in, Loader=SafeLoader)
        except FileNotFoundError:
            st.error(
                f"Authentication configuration file not found at: {self.config_path}"
            )
        except yaml.YAMLError as err:
            st.error(f"Error parsing authentication configuration: {err}")
            raise err

    def _setup_authenticator(self) -> None:
        try:
            self.authenticator = stauth.Authenticate(
                self.config["credentials"],
                self.config["cookie"]["name"],
                self.config["cookie"]["key"],
                self.config["cookie"]["expiry_days"],
            )
        except KeyError as err:
            st.error(f"Missing required configuration key: {err}")
            raise err

    def authenticate(self) -> bool:
        try:
            self.authenticator.login()
            return True
        except LoginError as err:
            st.error(err)
            raise err

    @property
    def is_authenticated(self) -> bool:
        return bool(st.session_state.get("username"))

    def logout(self) -> None:
        if self.authenticator:
            self.authenticator.logout(location="sidebar")

    @property
    def current_username(self) -> Optional[str]:
        return st.session_state.get("username")

    @property
    def current_role(self) -> Optional[str]:
        return st.session_state.get("roles")
