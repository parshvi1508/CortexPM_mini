import streamlit as st
import pandas as pd
import plotly.express as px
import qrcode
from io import BytesIO
from PIL import Image

def render():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
            body {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: #f4f4f8;
                font-family: 'Poppins', sans-serif;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
            }
            .stButton>button {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                font-family: 'Poppins', sans-serif;
                font-size: 16px;
                font-weight: 500;
                border-radius: 8px;
                padding: 10px 24px;
                border: none;
                transition: all 0.3s ease;
                box-shadow: 0px 4px 10px rgba(30, 60, 114, 0.3);
                display: block;
                margin: 10px auto;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #2a5298, #1e3c72);
                transform: translateY(-2px);
                box-shadow: 0px 6px 15px rgba(30, 60, 114, 0.5);
            }
            .stSelectbox>div>div {
                background-color: rgba(255, 255, 255, 0.05);
                color: #f4f4f8;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .stTextInput>div>div>input {
                background-color: rgba(255, 255, 255, 0.05);
                color: #f4f4f8 !important;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 8px 12px;
                font-family: 'Poppins', sans-serif;
                transition: all 0.3s ease;
            }
            .stTextInput>div>div>input:focus {
                border-color: #1e3c72;
                box-shadow: 0 0 5px rgba(30, 60, 114, 0.5);
            }
            .stSelectbox>div>div:hover, .stTextInput>div>div>input:hover {
                border-color: #2a5298;
                box-shadow: 0 0 5px rgba(42, 82, 152, 0.5);
            }
            .stMetric>div {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0px 4px 10px rgba(30, 60, 114, 0.3);
                transition: all 0.3s ease;
            }
            .stMetric>div:hover {
                transform: translateY(-2px);
                box-shadow: 0px 6px 15px rgba(30, 60, 114, 0.5);
            }
            .sidebar .sidebar-content {
                background: linear-gradient(135deg, #1e3c72, #2a5298);
                color: white;
            }
            .sidebar .sidebar-content a {
                color: white;
            }
            .sidebar .sidebar-content a:hover {
                color: #f0f2f6;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Student Dashboard")
    st.write("Welcome to the Student Dashboard!")

    options = ["Dashboard", "View Projects", "Submit Work", "Chat", "Notifications", "Profile & Settings"]
    choice = st.sidebar.radio("Student", options)

    if choice == "Dashboard":
        st.subheader("Overview")

        # Mock data for demonstration
        projects = pd.DataFrame({
            'Project ID': [1, 2, 3],
            'Project Title': ['Project 1', 'Project 2', 'Project 3'],
            'Status': ['In Progress', 'Completed', 'Initiated']
        })
        notifications = pd.DataFrame({
            'Notification': ['Deadline approaching', 'New submission', 'Meeting scheduled'],
            'Date': ['2023-10-01', '2023-10-02', '2023-10-03']
        })

        # Projects
        st.subheader("Your Projects")
        st.dataframe(projects)

        # Notifications
        st.subheader("Notifications")
        st.dataframe(notifications)

        # Analysis Graphs
        st.subheader("Project Status Distribution")
        project_status_counts = projects['Status'].value_counts().reset_index()
        project_status_counts.columns = ['Status', 'Count']
        fig = px.pie(project_status_counts, values='Count', names='Status', title='Project Status Distribution')
        st.plotly_chart(fig)

        # QR Code for Profile
        st.subheader("Generate QR Code for Profile")
        profile_url = "https://example.com/profile/johndoe"  # Mock profile URL
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(profile_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buf = BytesIO()
        img.save(buf)
        st.image(buf.getvalue(), caption="Scan to view profile")

    elif choice == "View Projects":
        st.subheader("View Projects")
        projects = pd.DataFrame({
            'Project ID': [1, 2, 3],
            'Project Title': ['Project 1', 'Project 2', 'Project 3'],
            'Description': ['Description of Project 1', 'Description of Project 2', 'Description of Project 3'],
            'Status': ['In Progress', 'Completed', 'Initiated']
        })
        st.dataframe(projects)

    elif choice == "Submit Work":
        st.subheader("Submit Work")
        project_id = st.text_input("Project ID", key="submit_project_id")
        submission_text = st.text_area("Submission Text", key="submission_text")
        uploaded_files = st.file_uploader("Upload Files", type=["pdf", "docx", "txt", "jpg", "png"], accept_multiple_files=True)
        if st.button("Submit", key="submit_button"):
            st.success("Work submitted successfully.")
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    st.write(f"Uploaded file: {uploaded_file.name}")

    elif choice == "Chat":
        st.subheader("Chat with Team Members")
        team_members = ["Alice", "Bob", "Charlie"]  # Mock data for team members
        member = st.selectbox("Select Member", team_members, key="chat_member_selectbox")
        message = st.text_area("Message", key="chat_message")
        if st.button("Send Message", key="send_message_button"):
            st.success(f"Message sent to {member} successfully.")
        
        # Display chat history (mock data)
        st.subheader("Chat History")
        chat_history = pd.DataFrame({
            'Sender': ['You', 'Alice', 'You', 'Bob'],
            'Message': ['Hello!', 'Hi there!', 'How is the project going?', 'It is going well!'],
            'Timestamp': ['2023-10-01 10:00', '2023-10-01 10:01', '2023-10-01 10:05', '2023-10-01 10:10']
        })
        st.dataframe(chat_history)

    elif choice == "Notifications":
        st.subheader("Notifications")
        notifications = pd.DataFrame({
            'Notification': ['Deadline approaching', 'New submission', 'Meeting scheduled'],
            'Date': ['2023-10-01', '2023-10-02', '2023-10-03']
        })
        st.dataframe(notifications)

    elif choice == "Profile & Settings":
        st.subheader("Profile & Settings")

        settings_action = st.selectbox("Select Setting", ["Update Profile", "Change Password"], key="settings_action_selectbox")

        if settings_action == "Update Profile":
            st.subheader("Update Profile")
            username = st.text_input("Username", key="update_profile_username")
            # Mock data for demonstration
            user = {
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'resume': 'resume.pdf',
                'github': 'https://github.com/johndoe'
            }
            name = st.text_input("Full Name", value=user['name'], key="update_profile_name")
            email = st.text_input("Email", value=user['email'], key="update_profile_email")
            resume = st.file_uploader("Upload Resume", type=["pdf", "docx"], key="update_profile_resume")
            github = st.text_input("GitHub ID", value=user['github'], key="update_profile_github")
            profile_image = st.file_uploader("Upload Profile Image", type=["jpg", "png"], key="update_profile_image")
            if st.button("Update Profile", key="update_profile_button"):
                st.success("Profile updated successfully.")
                if resume:
                    st.write(f"Uploaded resume: {resume.name}")
                if profile_image:
                    st.image(profile_image, caption="Profile Image")

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