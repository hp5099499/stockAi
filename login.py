# import firebase_admin

# from firebase_admin import credentials
# from firebase_admin import auth

# try:
#     firebase_admin.get_app()
# except ValueError:
#     cred = credentials.Certificate('services-7b5c8-f7bf4c632563.json')
#     firebase_admin.initialize_app(cred)

# def app():
#     st.title('Welcome to :violet[Services] 😎')

#     # choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])
#     # choice = st.selectbox('What would you like to do', ['Login', 'Sign Up'], index=None, placeholder="Select Sign Up if you want to register")

#     if 'username' not in st.session_state:
#         st.session_state.username = ''
#     if 'useremail' not in st.session_state:
#         st.session_state.useremail = ''

#     def f():
#         try:
#             user = auth.get_user_by_email(email)
#             st.success('Login Successful')
#             st.session_state.username = user.uid
#             st.session_state.useremail = user.email

#             st.session_state.signedout = True
#             st.session_state.signout = True

#         except:
#             st.warning('Login Failed')

#     def t():
#         st.session_state.signout = False
#         st.session_state.signedout = False
#         st.session_state.username = ''

#     if 'signedout' not in st.session_state:
#         st.session_state.signedout = False
#     if 'signout' not in st.session_state:
#         st.session_state.signout = False

#     if not st.session_state['signedout']:
#         choice = st.selectbox('Login/Signup', ['Login', 'Sign Up'])
    

#         if choice =='Login':

#             email= st.text_input('Email Address')
#             password = st.text_input('Password', type='password')

#             st.button('Login', on_click=f)

#             # st.button('Login')

#         else:

#             email= st.text_input('Email Address')
#             password = st.text_input('Password', type='password')

#             username = st.text_input('Enter your unique username')

#             if st.button('Create My Account'):
#                 user = auth.create_user(email = email, password = password, uid = username)

#                 st.success('Account created successfully!')
#                 st.markdown('Please Login using your email and password')
#                 st.balloons()

#     if st.session_state.signout:
#         st.text('Name' + st.session_state.username)
#         st.text('Email id: ' + st.session_state.useremail)
#         st.button('Sign out', on_click=t)

#         # st.write("You selected:", choice)
