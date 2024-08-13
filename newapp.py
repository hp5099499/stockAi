import streamlit as st
from streamlit_navigation_bar import st_navbar

if "role" not in st.session_state:
    st.session_state.role = None

Roles = [None, "Requester", "Responder", "Admin"]

def login():
    st.header("Login")
    role = st.selectbox("Choose your role", Roles)

    if st.button("Login"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

def main():
    if st.session_state.role is None:
        login()
    else:
        st.title("StockAI")

        # Define the navigation pages
        nav_pages = [
            "dashboard.py",
            "Aboutpage.py",
            "Homepage.py",
            "loginpage.py",
            "analyses.py",
            "setting.py",
            "logout"
        ]

        # Create navigation bar
        selection = st_navbar(pages=nav_pages)

        # Handle the selection
        if selection == "logout":
            logout()
        else:
            page = selection
            if page:
                with open(page) as f:
                    exec(f.read())

if __name__ == "__main__":
    main()

