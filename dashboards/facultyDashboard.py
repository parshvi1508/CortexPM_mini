import streamlit as st
import pandas as pd
import plotly.express as px

def render():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            body {
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: #333;
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
            }
            .stButton>button {
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: white;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                font-weight: 500;
                border-radius: 8px;
                padding: 10px 24px;
                border: none;
                transition: all 0.3s ease;
                box-shadow: 0px 4px 10px rgba(255, 154, 158, 0.3);
                display: block;
                margin: 10px auto;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #fad0c4, #ff9a9e);
                transform: translateY(-2px);
                box-shadow: 0px 6px 15px rgba(255, 154, 158, 0.5);
            }
            .stSelectbox>div>div {
                background-color: rgba(255, 255, 255, 0.05);
                color: #333;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .stTextInput>div>div>input {
                background-color: rgba(255, 255, 255, 0.05);
                color: #333 !important;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .stTextInput>div>div>input:focus {
                border-color: #ff9a9e;
                box-shadow: 0 0 5px rgba(255, 154, 158, 0.5);
            }
            .stSelectbox>div>div:hover, .stTextInput>div>div>input:hover {
                border-color: #fad0c4;
                box-shadow: 0 0 5px rgba(250, 208, 196, 0.5);
            }
            .stMetric>div {
                background: linear-gradient(135deg, #ff9a9e, #fad0c4);
                color: white;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0px 4px 10px rgba(255, 154, 158, 0.3);
                transition: all 0.3s ease;
            }
            .stMetric>div:hover {
                transform: translateY(-2px);
                box-shadow: 0px 6px 15px rgba(255, 154, 158, 0.5);
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("FACULTY")
    options = ["Dashboard", "View Mentees", "Feedback & Grading", "Project Tracking", "Chat", "Notifications", "Analytics", "Profile & Settings"]
    choice = st.sidebar.radio("Faculty", options)

    if choice == "Dashboard":
        st.title("Faculty Dashboard")
        st.subheader("Overview")

        # Mock data for demonstration
        teams = pd.DataFrame({
            'Team ID': [1, 2, 3],
            'Team Name': ['Team A', 'Team B', 'Team C'],
            'Project Title': ['Project 1', 'Project 2', 'Project 3'],
            'Status': ['In Progress', 'Completed', 'Initiated']
        })
        notifications = pd.DataFrame({
            'Notification': ['Deadline approaching', 'New submission', 'Meeting scheduled'],
            'Date': ['2023-10-01', '2023-10-02', '2023-10-03']
        })

        # Assigned Teams
        st.subheader("Assigned Teams")
        st.dataframe(teams)

        # Notifications
        st.subheader("Notifications")
        st.dataframe(notifications)

        # Analysis Graphs
        st.subheader("Project Status Distribution")
        project_status_counts = teams['Status'].value_counts().reset_index()
        project_status_counts.columns = ['Status', 'Count']
        fig = px.pie(project_status_counts, values='Count', names='Status', title='Project Status Distribution')
        st.plotly_chart(fig)

    elif choice == "View Mentees":
        st.subheader("View Mentees")
        mentees = pd.DataFrame({
            'Mentee ID': [1, 2, 3],
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Role': ['Leader', 'Member', 'Member']
        })
        st.dataframe(mentees)

    elif choice == "Feedback & Grading":
        st.subheader("Feedback & Grading")
        team_id = st.text_input("Team ID", key="feedback_team_id")
        if st.button("Fetch Team Details", key="fetch_team_details_button"):
            # Mock data for demonstration
            team = {
                'name': 'Team A',
                'project_title': 'Project 1',
                'project_description': 'Description of Project 1'
            }
            st.write(f"Team Name: {team['name']}")
            st.write(f"Project Title: {team['project_title']}")
            st.write(f"Project Description: {team['project_description']}")
            feedback = st.text_area("Feedback", key="feedback_text")
            grade = st.text_input("Grade", key="grade_text")
            if st.button("Submit Feedback & Grade", key="submit_feedback_button"):
                st.success("Feedback and grade submitted successfully.")

    elif choice == "Project Tracking":
        st.subheader("Project Tracking")
        project_action = st.selectbox("Action", ["View Submissions", "Track Progress"], key="project_action_selectbox")
        
        if project_action == "View Submissions":
            submissions = pd.DataFrame({
                'Submission ID': [1, 2, 3],
                'Team ID': [1, 2, 3],
                'Submission Date': ['2023-10-01', '2023-10-02', '2023-10-03']
            })
            st.dataframe(submissions)
        
        elif project_action == "Track Progress":
            progress = pd.DataFrame({
                'Team ID': [1, 2, 3],
                'Milestone': ['Milestone 1', 'Milestone 2', 'Milestone 3'],
                'Status': ['Completed', 'In Progress', 'Not Started']
            })
            st.dataframe(progress)

    elif choice == "Chat":
        st.subheader("Chat Feature")
        chat_action = st.selectbox("Chat With", ["Individual Student", "Team"], key="chat_action_selectbox")
        
        if chat_action == "Individual Student":
            student_id = st.text_input("Student ID", key="chat_student_id")
            message = st.text_area("Message", key="chat_message")
            if st.button("Send Message", key="send_message_button"):
                st.success("Message sent successfully.")
        
        elif chat_action == "Team":
            team_id = st.text_input("Team ID", key="chat_team_id")
            message = st.text_area("Message", key="chat_team_message")
            if st.button("Send Message to Team", key="send_team_message_button"):
                st.success("Message sent to team successfully.")

    elif choice == "Notifications":
        st.subheader("Notifications")
        notification_action = st.selectbox("Action", ["Set Deadline", "Send Alert"], key="notification_action_selectbox")
        
        if notification_action == "Set Deadline":
            deadline_name = st.text_input("Deadline Name", key="deadline_name")
            deadline_date = st.date_input("Deadline Date", key="deadline_date")
            if st.button("Set Deadline", key="set_deadline_button"):
                st.success("Deadline set successfully.")
        
        elif notification_action == "Send Alert":
            alert_message = st.text_area("Alert Message", key="alert_message")
            if st.button("Send Alert", key="send_alert_button"):
                st.success("Alert sent successfully.")

    elif choice == "Analytics":
        st.subheader("Analytics and Insights")

        report_action = st.selectbox("Select Report Type", ["Monthly Report", "Yearly Report", "Custom Report"], key="report_action_selectbox")

        if report_action == "Monthly Report":
            month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], key="month_selectbox")
            year = st.number_input("Select Year", min_value=2000, max_value=2100, value=2023, step=1, key="year_input")
            if st.button("Download Monthly Report", key="download_monthly_report_button"):
                st.success(f"Monthly report for {month} {year} is being generated...")

        elif report_action == "Yearly Report":
            year = st.number_input("Select Year", min_value=2000, max_value=2100, value=2023, step=1, key="yearly_year_input")
            if st.button("Download Yearly Report", key="download_yearly_report_button"):
                st.success(f"Yearly report for {year} is being generated...")

        elif report_action == "Custom Report":
            start_date = st.date_input("Start Date", key="start_date_input")
            end_date = st.date_input("End Date", key="end_date_input")
            if st.button("Download Custom Report", key="download_custom_report_button"):
                st.success(f"Custom report from {start_date} to {end_date} is being generated...")

    elif choice == "Profile & Settings":
        st.subheader("Profile & Settings")

        settings_action = st.selectbox("Select Setting", ["Update Profile", "Change Password"], key="settings_action_selectbox")

        if settings_action == "Update Profile":
            st.subheader("Update Profile")
            username = st.text_input("Username", key="update_profile_username")
            # Mock data for demonstration
            user = {
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            }
            name = st.text_input("Full Name", value=user['name'], key="update_profile_name")
            email = st.text_input("Email", value=user['email'], key="update_profile_email")
            if st.button("Update Profile", key="update_profile_button"):
                st.success("Profile updated successfully.")

        elif settings_action == "Change Password":
            st.subheader("Change Password")
            username = st.text_input("Username", key="change_password_username")
            old_password = st.text_input("Old Password", type="password", key="old_password")
            new_password = st.text_input("New Password", type="password", key="new_password")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
            if st.button("Change Password", key="change_password_button"):
                if new_password == confirm_password:
                    st.success("Password changed successfully.")
                else:
                    st.error("New passwords do not match.")

if __name__ == "__main__":
    render()