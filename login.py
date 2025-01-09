import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Common configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# Page configuration
st.set_page_config(page_title="CortexPM", layout="centered")

# Hardcoded credentials for demonstration purposes
CREDENTIALS = {
    "admin@test.com": {"password": "admin123", "role": "Admin"},
    "faculty@test.com": {"password": "faculty123", "role": "Faculty"},
    "student@test.com": {"password": "student123", "role": "Student"}
}

# Initialize session states
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# CSS styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        body {
            background: linear-gradient(135deg, #0d47a1, #1de9b6);
            color: #f4f4f8;
            font-family: 'Poppins', sans-serif;
        }

        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.05);
            color: #e0f7fa !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            font-family: 'Poppins', sans-serif;
        }

        .stButton>button {
            background: linear-gradient(135deg, #0d47a1, #1de9b6);
            color: white;
            font-family: 'Poppins', sans-serif;
            font-size: 16px;
            font-weight: 500;
            border-radius: 8px;
            padding: 10px 24px;
            border: none;
            width: 100%;
            margin: 5px 0;
            transition: all 0.3s ease;
        }

        .stButton>button:hover {
            background: linear-gradient(135deg, #1565C0, #00BFA5);
            transform: translateY(-2px);
        }

        h1 {
            text-align: center;
            background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Poppins', sans-serif;
            font-weight: 700;
            font-size: 2.8em;
            margin-bottom: 10px;
        }

        h2 {
            text-align: center;
            color: #a5f3fc;
            font-family: 'Poppins', sans-serif;
            font-weight: 300;
            font-size: 1.5em;
            margin-bottom: 30px;
        }

        .element-container .stError {
            background: rgba(255, 82, 82, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 82, 82, 0.3);
            color: #ffcdd2;
            padding: 10px;
            border-radius: 8px;
        }

        .element-container .stSuccess {
            background: linear-gradient(135deg, rgba(13, 71, 161, 0.1), rgba(29, 233, 182, 0.1));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(29, 233, 182, 0.3);
            color: #e0f7fa;
            padding: 10px;
            border-radius: 8px;
        }

        .stInfo {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            color: #e0f7fa;
            padding: 20px;
            margin: 20px 0;
        }

        /* Select box styling */
        .stSelectbox > div > div {
            background-color: rgba(255, 255, 255, 0.05);
            color: #e0f7fa;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Logo
st.markdown("<div style='text-align: center; margin-bottom: 20px;'>", unsafe_allow_html=True)
st.image("assets/CORTEX PM LOGO.png", width=350)
st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # Title and tagline
    st.markdown("<h1>CortexPM</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Empowering Collaboration, Tracking Success</h2>", unsafe_allow_html=True)

    # Navigation buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔒 Login"):
            st.session_state.page = 'login'

    with col2:
        if st.button("📝 Register"):
            st.session_state.page = 'register'

    with col3:
        if st.button("ℹ️ About"):
            st.session_state.page = 'about'

    # Page content
    if st.session_state.page == 'login':
        st.markdown("### Enter your credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Submit"):
            if username in CREDENTIALS and CREDENTIALS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.role = CREDENTIALS[username]["role"]
                st.success(f"Successfully logged in as {CREDENTIALS[username]['role']}!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif st.session_state.page == 'register':
        st.markdown("### Register New Account")
        register_role = st.selectbox("Register as", ["Student", "Faculty", "Admin"])
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if not all([name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                st.success("Registration successful! Please log in.")
                st.session_state.page = 'login'
                st.rerun()

    elif st.session_state.page == 'about':
        st.markdown("### About CortexPM")
        st.info(
            "CortexPM is a streamlined project management system designed for seamless communication "
            "and effective project tracking among students, faculty, and administrators. Our mission "
            "is to empower collaboration and enhance productivity through a user-friendly platform "
            "tailored to the needs of educational institutions."
            
        )

else:
    # Dashboard content based on role
    if st.session_state.role == "Admin":
        st.success("Welcome to Admin Dashboard!")
        from dashboards.adminDashboard import render as render_admin_dashboard
        render_admin_dashboard()
        
    elif st.session_state.role == "Faculty":
        st.success("Welcome to Faculty Dashboard!")
        from dashboards.facultyDashboard import render as render_faculty_dashboard
        render_faculty_dashboard()
        
    elif st.session_state.role == "Student":
        st.success("Welcome to Student Dashboard!")
        from dashboards.studentDashboard import render as render_student_dashboard
        render_student_dashboard()

    # Logout button in sidebar
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.page = 'main'
        st.rerun()

# Footer
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #a5f3fc; font-family: "Poppins", sans-serif; font-size: 0.9em; position: fixed; bottom: 0; width: 100%; left: 0; background: rgba(0,0,0,0.1);'>
        © 2024 CortexPM | All rights reserved
    </div>
""", unsafe_allow_html=True)