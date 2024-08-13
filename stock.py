import streamlit as st
from analyses import run_analysis  # Import the analysis component


if "role" not in st.session_state:
    st.session_state.role=None
Roles=[None,"Requester","Responder","Admin"]

def login():
    st.header("Login")
    role=st.selectbox("Choose your role",Roles)

    if st.button("Login"):
        st.session_state.role=role
        st.rerun()

def logout():
    st.session_state.role=None
    st.rerun()

role=st.session_state.role
logout_page=st.Page(logout,title="Log out",icon=":material/logout:")
# logout_page=st.Page("loginpage.py",title="Profile",icon=":material/person:")
settings=st.Page("setting.py",title="Settings",icon=":material/settings:")
request_1=st.Page(
    "dashboard.py",
    title="Dashboard",icon="🛃",
        default=(role=="Requester")
        )
request_2=st.Page(
    "Aboutpage.py",
    title="About",icon="📃"
    )
request_3=st.Page(
    "Homepage.py",
    title="Stock Dashboard",
    icon="🏠")

request_4=st.Page(
    "loginpage.py",
    title="Account",icon="🔐"
    )
request_5=st.Page(
    "analyses.py",
    title="Analysis",
    icon="🏷️")
account_pages=[logout_page,settings]
request_pages=[request_1,request_2,request_3,request_4,request_5]

st.title("StockAI")
# st.logo("designer.png", icon_image="stock.png")

page_dict={}
if st.session_state.role in ["Requester"]:
    page_dict["Request"]=request_pages

if len(page_dict)>0:
    pg=st.navigation({"Account":account_pages}|page_dict)
else:
    pg=st.navigation([st.Page(login)])
pg.run()
