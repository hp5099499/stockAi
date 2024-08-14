import streamlit as st

def redirect(url):
    st.write(f'<meta http-equiv="refresh" content="0; URL={url}">', unsafe_allow_html=True)


st.title('Create New Password')

p = st.text_input('Enter New Password', type = 'password')
p1 = st.text_input('Re-Enter New Password', type = 'password')


if p != p1 and st.button('Reset Password'):
    st.error("Password doesn't match.")
    st.success("New Password Created Successfully.")
    st.balloons()
    st.write("You have been redirected to the login page")
    redirect('https://resetpassword-c4qtkqjpgdnzx4xtttbtnk.streamlit.app/login')
