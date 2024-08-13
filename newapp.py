import streamlit as st
from streamlit_navigation_bar import st_navbar

# Import page modules
import dashboard
import Aboutpage
import Homepage
import loginpage
import analyses
import setting

if "role" not in st.session_state:
    st.session_state.role = None

Roles = [None, "Requester", "Responder", "Admin"]

def login():
    st.header("Login")
    role = st.selectbox("Choose your role", Roles)

    if st.button("Login"):
        st.session_state.role = role
        st.experimental_rerun()

def logout():
    st.session_state.role = None
    st.experimental_rerun()

def main():
    if st.session_state.role is None:
        login()
    else:
        st.title("StockAI")

        # Define the navigation pages
        nav_pages = [
            "Dashboard",
            "About",
            "Home",
            "Account",
            "Analysis",
            "Settings",
            "Logout"
        ]

        # Create navigation bar
        selection = st_navbar(pages=nav_pages)
        st.write(f"Selection: {selection}")  # Debugging line

        # Handle the selection
        if selection == "Logout":
            logout()
        elif selection == "Dashboard":
            st.write("Rendering Dashboard")  # Debugging line
            dashboard.render()
        elif selection == "About":
            st.write("Rendering About Page")  # Debugging line
            Aboutpage.render()
        elif selection == "Home":
            st.write("Rendering Home Page")  # Debugging line
            Homepage.render()
        elif selection == "Account":
            st.write("Rendering Login Page")  # Debugging line
            loginpage.render()
        elif selection == "Analysis":
            st.write("Rendering Analysis Page")  # Debugging line
            analyses.render()
        elif selection == "Settings":
            st.write("Rendering Settings Page")  # Debugging line
            setting.render()

if __name__ == "__main__":
    main()
