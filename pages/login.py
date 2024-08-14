import streamlit as st
from reset import email_address
# from reset_password import p

def redirect(url):
    st.write(f'<meta http-equiv="refresh" content="0; URL={url}">', unsafe_allow_html=True)


st.title('Login')
em = st.text_input('Enter your email')
pa = st.text_input('Enter your password', type = 'password')

# if em != email_address and pa != p:
if em !=email_address and st.button('Login'):
    st.write('Enter correct detail')
    st.success('Login Successfully')
    st.write('You are redirect to Home Page')
    redirect('https://resetpassword-c4qtkqjpgdnzx4xtttbtnk.streamlit.app/home')
