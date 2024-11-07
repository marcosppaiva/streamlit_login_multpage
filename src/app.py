from pathlib import Path

import streamlit as st

from auth import StreamlitAuthenticator
from utils import get_project_root

CONFIG_PATH = Path(get_project_root()).joinpath(".secrets/config.yaml")


def display_logo():
    st.logo(
        str(Path(get_project_root()).joinpath("assets/logo.png")),
        icon_image=str(Path(get_project_root()).joinpath("assets/logo.png")),
    )


def display_sidebar(auth: StreamlitAuthenticator):
    with st.sidebar:
        st.write(f"Welcome {auth.current_username}")
        if auth.logout():
            st.rerun()


def create_navigation_pages(auth: StreamlitAuthenticator):
    if not auth.is_authenticated:
        st.navigation(
            [st.Page(lambda: None, title="Streamlit Login Demo")], position="hidden"
        ).run()
        st.stop()
    else:
        page_01 = st.Page(
            "ui/page_01.py",
            title="Page 1",
            icon=":material/help:",
        )
        page_02 = st.Page(
            "ui/page_02.py",
            title="Page 2",
            icon=":material/help:",
        )

        pages = {"Agents": [page_01, page_02]}

        if "admin" in auth.current_role:
            admin_page = st.Page(
                "ui/admin.py",
                title="Admin",
                icon=":material/person_add:",
            )
            pages["Settings"] = [admin_page]

        st.navigation(pages).run()


def main():
    auth = StreamlitAuthenticator(CONFIG_PATH)
    if not auth.is_authenticated:
        auth.authenticate()
    else:
        # display_logo() #
        display_sidebar(auth)
        create_navigation_pages(auth)


if __name__ == "__main__":
    main()
