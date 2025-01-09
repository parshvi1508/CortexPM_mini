import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

class Config:
    # Common configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

def render():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            body {
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: #ffffff;
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
            }
            .stButton>button {
                background: linear-gradient(135deg, #6a11cb, #2575fc);
                color: white;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                font-weight: 500;
                border-radius: 8px;
                padding: 10px 24px;
                border: none;
                transition: all 0.3s ease;
                box-shadow: 0px 4px 10px rgba(106, 17, 203, 0.3);
                display: block;
                margin: 10px auto;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #2575fc, #6a11cb);
                transform: translateY(-2px);
                box-shadow: 0px 6px 15px rgba(106, 17, 203, 0.5);
            }
            .stSelectbox>div>div {
                background-color: rgba(255, 255, 255, 0.05);
                color: #f4f4f8;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            .stTextInput>div>div>input {
                background-color: rgba(255, 255, 255, 0.05);
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-family: 'Poppins', sans-serif;
            }
            h1, h2, h3 {
                color: #ffdd55; /* Gold accent color for headings */
            }
            .metric-container {
                text-align: center;
            }
            .metric-container div {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("ADMIN")
    options = ["Dashboard", "User Management", "Team Management", "Project Tracking", "Analytics and Reports", "Notifications", "Logs and Activity", "Settings"]
    choice = st.sidebar.radio("", options)

    

    if choice == "Dashboard":
        st.title("Admin Dashboard")
        st.subheader("Overview")

        # Fetch data from Supabase
        users_response = supabase.table('users').select('*').execute()
        projects_response = supabase.table('projects').select('*').execute()
        approvals_response = supabase.table('approvals').select('*').execute()

        total_users = len(users_response.data)
        active_projects = len([project for project in projects_response.data if project['status'] == 'In Progress'])
        pending_approvals = len([approval for approval in approvals_response.data if approval['status'] == 'Pending'])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Users", value=total_users)
        with col2:
            st.metric(label="Active Projects", value=active_projects)
        with col3:
            st.metric(label="Pending Approvals", value=pending_approvals)

        # Example graph
        st.subheader("Project Status Distribution")
        project_status_counts = pd.DataFrame(projects_response.data)['status'].value_counts().reset_index()
        project_status_counts.columns = ['Status', 'Count']
        fig = px.pie(project_status_counts, values='Count', names='Status', title='Project Status Distribution')
        st.plotly_chart(fig)

    elif choice == "User Management":
        st.subheader("User Management")
        user_action = st.selectbox("Action", ["Add User", "Edit User", "Remove User", "View Users"], key="user_action_selectbox")
        
        if user_action == "Add User":
            role = st.selectbox("Role", ["Student", "Faculty", "Admin"], key="add_user_role")
            name = st.text_input("Full Name", key="add_user_name")
            username = st.text_input("Username", key="add_user_username")
            email = st.text_input("Email", key="add_user_email")
            password = st.text_input("Password", type="password", key="add_user_password")
            if st.button("Add User", key="add_user_button"):
                response = supabase.table('users').insert({
                    "role": role,
                    "name": name,
                    "username": username,
                    "email": email,
                    "password": password
                }).execute()
                if response.status_code == 201:
                    st.success(f"User {username} added successfully.")
                else:
                    st.error("Failed to add user.")
        
        elif user_action == "Edit User":
            username = st.text_input("Username of the user to edit", key="edit_user_username")
            if st.button("Fetch User", key="fetch_user_button"):
                response = supabase.table('users').select('*').eq('username', username).execute()
                if response.data:
                    user = response.data[0]
                    name = st.text_input("Full Name", value=user['name'], key="edit_user_name")
                    email = st.text_input("Email", value=user['email'], key="edit_user_email")
                    role = st.selectbox("Role", ["Student", "Faculty", "Admin"], index=["Student", "Faculty", "Admin"].index(user['role']), key="edit_user_role")
                    if st.button("Update User", key="update_user_button"):
                        response = supabase.table('users').update({
                            "name": name,
                            "email": email,
                            "role": role
                        }).eq('username', username).execute()
                        if response.status_code == 200:
                            st.success(f"User {username} updated successfully.")
                        else:
                            st.error("Failed to update user.")
                else:
                    st.error("User not found.")
        
        elif user_action == "Remove User":
            username = st.text_input("Username of the user to remove", key="remove_user_username")
            if st.button("Remove User", key="remove_user_button"):
                response = supabase.table('users').delete().eq('username', username).execute()
                if response.status_code == 200:
                    st.success(f"User {username} removed successfully.")
                else:
                    st.error("Failed to remove user.")
        
        elif user_action == "View Users":
            response = supabase.table('users').select('*').execute()
            users = response.data
            df = pd.DataFrame(users)
            st.dataframe(df)

    elif choice == "Team Management":
        st.subheader("Team Management")
        team_action = st.selectbox("Action", ["View Teams", "Approve Team", "Modify Team"], key="team_action_selectbox")
        
        if team_action == "View Teams":
            response = supabase.table('teams').select('*').execute()
            teams = response.data
            df = pd.DataFrame(teams)
            st.dataframe(df)
        
        elif team_action == "Approve Team":
            team_id = st.text_input("Team ID to approve", key="approve_team_id")
            if st.button("Approve Team", key="approve_team_button"):
                response = supabase.table('teams').update({"status": "Approved"}).eq("id", team_id).execute()
                if response.status_code == 200:
                    st.success(f"Team {team_id} approved successfully.")
                else:
                    st.error("Failed to approve team.")
        
        elif team_action == "Modify Team":
            team_id = st.text_input("Team ID to modify", key="modify_team_id")
            if st.button("Fetch Team", key="fetch_team_button"):
                response = supabase.table('teams').select('*').eq('id', team_id).execute()
                if response.data:
                    team = response.data[0]
                    team_name = st.text_input("Team Name", value=team['name'], key="modify_team_name")
                    mentor_id = st.text_input("Mentor ID", value=team['mentor_id'], key="modify_team_mentor_id")
                    if st.button("Update Team", key="update_team_button"):
                        response = supabase.table('teams').update({
                            "name": team_name,
                            "mentor_id": mentor_id
                        }).eq('id', team_id).execute()
                        if response.status_code == 200:
                            st.success(f"Team {team_id} updated successfully.")
                        else:
                            st.error("Failed to update team.")
                else:
                    st.error("Team not found.")

    elif choice == "Project Tracking":
        st.subheader("Project Tracking")
        project_action = st.selectbox("Action", ["View Projects", "Update Project Status"], key="project_action_selectbox")
        
        if project_action == "View Projects":
            response = supabase.table('projects').select('*').execute()
            projects = response.data
            df = pd.DataFrame(projects)
            st.dataframe(df)
        
        elif project_action == "Update Project Status":
            project_id = st.text_input("Project ID to update", key="update_project_id")
            new_status = st.selectbox("New Status", ["Initiated", "In Progress", "Completed"], key="update_project_status")
            if st.button("Update Status", key="update_project_button"):
                response = supabase.table('projects').update({"status": new_status}).eq("id", project_id).execute()
                if response.status_code == 200:
                    st.success(f"Project {project_id} status updated to {new_status}.")
                else:
                    st.error("Failed to update project status.")

        elif choice == "Analytics and Reports":
            st.subheader("Analytics and Reports")

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

    elif choice == "Notifications":
        st.subheader("Notifications")
        notification_action = st.selectbox("Action", ["Send Announcement", "Manage Deadlines"], key="notification_action_selectbox")
        
        if notification_action == "Send Announcement":
            announcement = st.text_area("Announcement", key="announcement_text")
            if st.button("Send Announcement", key="send_announcement_button"):
                response = supabase.table('notifications').insert({
                    "message": announcement,
                    "type": "announcement"
                }).execute()
                if response.status_code == 201:
                    st.success("Announcement sent successfully.")
                else:
                    st.error("Failed to send announcement.")
        
        elif notification_action == "Manage Deadlines":
            deadline_name = st.text_input("Deadline Name", key="deadline_name")
            deadline_date = st.date_input("Deadline Date", key="deadline_date")
            if st.button("Set Deadline", key="set_deadline_button"):
                response = supabase.table('notifications').insert({
                    "message": f"Deadline for {deadline_name} is {deadline_date}",
                    "type": "deadline"
                }).execute()
                if response.status_code == 201:
                    st.success("Deadline set successfully.")
                else:
                    st.error("Failed to set deadline.")

        elif choice == "Logs and Activity":
            st.subheader("Logs and Activity")

            log_action = st.selectbox("Select Log Type", ["View Logs", "View Activity"], key="log_action_selectbox")

            if log_action == "View Logs":
                response = supabase.table('logs').select('*').execute()
                if response.error:
                    st.error(f"Failed to fetch logs: {response.error['message']}")
                else:
                    logs = response.data
                    df = pd.DataFrame(logs)
                    st.dataframe(df)

            elif log_action == "View Activity":
                response = supabase.table('activity').select('*').execute()
                if response.error:
                    st.error(f"Failed to fetch activity: {response.error['message']}")
                else:
                    activity = response.data
                    df = pd.DataFrame(activity)
                    st.dataframe(df)
        elif choice == "Settings":
            st.subheader("Settings")

            settings_action = st.selectbox("Select Setting", ["Change Password", "Update Profile", "Manage Roles"], key="settings_action_selectbox")

            if settings_action == "Change Password":
                st.subheader("Change Password")
                username = st.text_input("Username", key="change_password_username")
                old_password = st.text_input("Old Password", type="password", key="old_password")
                new_password = st.text_input("New Password", type="password", key="new_password")
                confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password")
                if st.button("Change Password", key="change_password_button"):
                    if new_password == confirm_password:
                        response = supabase.table('users').select('*').eq('username', username).eq('password', old_password).execute()
                        if response.data:
                            user_id = response.data[0]['id']
                            update_response = supabase.table('users').update({"password": new_password}).eq('id', user_id).execute()
                            if update_response.status_code == 200:
                                st.success("Password changed successfully.")
                            else:
                                st.error("Failed to change password.")
                        else:
                            st.error("Incorrect username or old password.")
                    else:
                        st.error("New passwords do not match.")

            elif settings_action == "Update Profile":
                st.subheader("Update Profile")
                username = st.text_input("Username", key="update_profile_username")
                if st.button("Fetch Profile", key="fetch_profile_button"):
                    response = supabase.table('users').select('*').eq('username', username).execute()
                    if response.data:
                        user = response.data[0]
                        name = st.text_input("Full Name", value=user['name'], key="update_profile_name")
                        email = st.text_input("Email", value=user['email'], key="update_profile_email")
                        if st.button("Update Profile", key="update_profile_button"):
                            update_response = supabase.table('users').update({
                            "name": name,
                            "email": email
                        }).eq('username', username).execute()
                            if update_response.status_code == 200:
                                st.success("Profile updated successfully.")
                            else:
                                st.error("Failed to update profile.")
                    else:
                        st.error("User not found.")

            elif settings_action == "Manage Roles":
                st.subheader("Manage Roles")
                username = st.text_input("Username", key="manage_roles_username")
                new_role = st.selectbox("New Role", ["Student", "Faculty", "Admin"], key="manage_roles_new_role")
                if st.button("Update Role", key="update_role_button"):
                    response = supabase.table('users').update({"role": new_role}).eq('username', username).execute()
                    if response.status_code == 200:
                        st.success(f"Role for {username} updated to {new_role}.")
                    else:
                        st.error("Failed to update role.")

if __name__ == "__main__":
    render()