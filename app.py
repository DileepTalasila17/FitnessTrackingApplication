import streamlit as st
from tracker import FitnessTracker

st.title("Fitness Tracker")

tracker = FitnessTracker()

nav_option = st.sidebar.selectbox("Choose an option", ["Register", "Login"])

if nav_option == "Register":
    st.header("Register")
    with st.form(key='registration_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        training_type = st.text_input("Training Type")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            result = tracker.register_user(username, password, training_type)
            st.write(result)
            if result == "Username already exists.":
                st.write("Already registered? [Login here](#login)")
    
elif nav_option == "Login":
    st.header("Login")
    with st.form(key='login_form'):
        login_username = st.text_input("Username", key="login")
        login_password = st.text_input("Password", type='password', key="password")
        login_button = st.form_submit_button("Login")
        if login_button:
            login_status = tracker.verify_user(login_username, login_password)
            if login_status == "Login successful.":
                st.write("Login successful!")
                progress_report = tracker.get_progress_report(login_username)
                st.subheader("Workouts")
                st.write(progress_report["workouts"])
                st.subheader("Measurements")
                st.write(progress_report["measurements"])
                st.subheader("Diet Recommendations")
                st.write(progress_report["diet_recommendations"])
                st.subheader("Progress Report")
                st.write(progress_report)
            else:
                st.write(login_status)
