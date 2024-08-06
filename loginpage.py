import streamlit as st
import firebase_admin

from firebase_admin import credentials
from firebase_admin import auth


# Create app if not created otherwise opened it.
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate('services-7b5c8-f7bf4c632563.json')
    firebase_admin.initialize_app(cred)

# Create bar for selected login/Signup
def app():
    st.title('Welcome to :violet[Services] 😎')

    # choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])
    choice = st.selectbox('What would you like to do', ['Login', 'Sign Up'], index=None, placeholder="Select Sign Up if you want to register")

  # Create function for after click login button
    def f():
        try:
            user = auth.get_user_by_email(email)
            st.sidebar.write(user.uid)
            st.success('Login Successful')

        except:
            st.warning('Login Failed')
    

  # create login function for register user
    if choice =='Login':

        email= st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        st.button('Login', on_click=f())

        # st.button('Login')

    else:

      # create register function for new user
        email= st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        username = st.text_input('Enter your unique username')

        if st.button('Create My Account'):
            user = auth.create_user(email = email, password = password, uid = username)

            st.success('Account created successfully!')
            st.markdown('Please Login using your email and password')
            st.balloons()

    # st.write("You selected:", choice)
