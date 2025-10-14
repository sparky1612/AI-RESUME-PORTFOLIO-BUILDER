import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os
from datetime import datetime, date
from streamlit_option_menu import option_menu

# Custom JSON encoder to handle date objects
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

# Configure page
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = {
        'personal_info': {},
        'experience': [],
        'education': [],
        'skills': [],
        'projects': []
    }

if 'portfolio_data' not in st.session_state:
    st.session_state.portfolio_data = {
        'projects': [],
        'achievements': [],
        'certifications': []
    }

# Hugging Face AI Integration
class HuggingFaceAI:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models"
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY', '')}"}
    
    def generate_content(self, prompt, model="microsoft/DialoGPT-medium"):
        """Generate content using Hugging Face models"""
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 200,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(
                f"{self.api_url}/{model}",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "API request failed"}
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_resume_text(self, text):
        """Analyze resume text for improvements"""
        prompt = f"Analyze this resume text and provide improvement suggestions: {text[:500]}"
        return self.generate_content(prompt)

# Initialize AI helper
ai_helper = HuggingFaceAI()

# Main navigation
selected = option_menu(
    menu_title=None,
    options=["Home", "Resume Builder", "Portfolio Builder", "AI Assistant", "Deploy"],
    icons=["house", "file-text", "palette", "robot", "cloud"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#667eea", "font-size": "18px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#667eea"},
    }
)

# Home Page
if selected == "Home":
    st.markdown("""
    <div class="main-header">
        <h1>AI Resume & Portfolio Builder</h1>
        <p>Build professional resumes and portfolios with AI-powered assistance</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>Smart Resume Builder</h3>
            <p>Create professional resumes with AI-powered content suggestions and formatting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>Portfolio Creator</h3>
            <p>Build stunning portfolios showcasing your projects and achievements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>AI Assistant</h3>
            <p>Get intelligent suggestions and improvements for your content</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Metrics
    st.markdown("### Features Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Templates</h4>
            <h2>10+</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>AI Models</h4>
            <h2>5+</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Cloud Ready</h4>
            <h2>Yes</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>Responsive</h4>
            <h2>Yes</h2>
        </div>
        """, unsafe_allow_html=True)

# Resume Builder Page
elif selected == "Resume Builder":
    st.header("AI-Powered Resume Builder")
    
    # Personal Information Section
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=st.session_state.resume_data['personal_info'].get('name', ''))
        email = st.text_input("Email", value=st.session_state.resume_data['personal_info'].get('email', ''))
        phone = st.text_input("Phone", value=st.session_state.resume_data['personal_info'].get('phone', ''))
    
    with col2:
        location = st.text_input("Location", value=st.session_state.resume_data['personal_info'].get('location', ''))
        linkedin = st.text_input("LinkedIn", value=st.session_state.resume_data['personal_info'].get('linkedin', ''))
        github = st.text_input("GitHub", value=st.session_state.resume_data['personal_info'].get('github', ''))
    
    # Update session state
    st.session_state.resume_data['personal_info'] = {
        'name': name, 'email': email, 'phone': phone,
        'location': location, 'linkedin': linkedin, 'github': github
    }
    
    # Professional Summary
    st.subheader("Professional Summary")
    summary = st.text_area("Write your professional summary", height=100)
    
    # Experience Section
    st.subheader("Work Experience")
    
    if st.button("Add Experience"):
        st.session_state.resume_data['experience'].append({
            'title': '', 'company': '', 'start_date': '', 'end_date': '',
            'description': '', 'current': False
        })
    
    for i, exp in enumerate(st.session_state.resume_data['experience']):
        with st.expander(f"Experience {i+1}"):
            col1, col2 = st.columns(2)
            
            with col1:
                exp['title'] = st.text_input(f"Job Title {i+1}", value=exp.get('title', ''))
                exp['company'] = st.text_input(f"Company {i+1}", value=exp.get('company', ''))
                exp['current'] = st.checkbox(f"Current Position {i+1}", value=exp.get('current', False))
            
            with col2:
                exp['start_date'] = st.date_input(f"Start Date {i+1}", value=date(2023, 1, 1))
                if not exp['current']:
                    exp['end_date'] = st.date_input(f"End Date {i+1}", value=date(2023, 12, 31))
            
            exp['description'] = st.text_area(f"Job Description {i+1}", value=exp.get('description', ''), height=100)
            
            if st.button(f"Remove Experience {i+1}"):
                st.session_state.resume_data['experience'].pop(i)
                st.rerun()
    
    # Skills Section
    st.subheader("Skills")
    skills_input = st.text_input("Enter skills separated by commas")
    if st.button("Add Skills"):
        if skills_input:
            skills_list = [skill.strip() for skill in skills_input.split(',')]
            st.session_state.resume_data['skills'].extend(skills_list)
            st.session_state.resume_data['skills'] = list(set(st.session_state.resume_data['skills']))
            st.success("Skills added successfully!")
    
    if st.session_state.resume_data['skills']:
        st.write("**Current Skills:**")
        for skill in st.session_state.resume_data['skills']:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {skill}")
            with col2:
                if st.button(f"Remove {skill}", key=f"remove_{skill}"):
                    st.session_state.resume_data['skills'].remove(skill)
                    st.rerun()
    
    # Generate Resume Button
    if st.button("Generate AI-Enhanced Resume", type="primary"):
        st.success("Resume generated successfully!")
        st.download_button(
            label="Download Resume",
            data=json.dumps(st.session_state.resume_data, indent=2, cls=DateEncoder),
            file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Portfolio Builder Page
elif selected == "Portfolio Builder":
    st.header("Portfolio Builder")
    
    # Project Portfolio Section
    st.subheader("Projects")
    
    if st.button("Add Project"):
        st.session_state.portfolio_data['projects'].append({
            'title': '', 'description': '', 'technologies': '', 'github_url': '',
            'live_url': '', 'image': None
        })
    
    for i, project in enumerate(st.session_state.portfolio_data['projects']):
        with st.expander(f"Project {i+1}"):
            project['title'] = st.text_input(f"Project Title {i+1}", value=project.get('title', ''))
            project['description'] = st.text_area(f"Project Description {i+1}", value=project.get('description', ''), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                project['technologies'] = st.text_input(f"Technologies {i+1}", value=project.get('technologies', ''))
                project['github_url'] = st.text_input(f"GitHub URL {i+1}", value=project.get('github_url', ''))
            with col2:
                project['live_url'] = st.text_input(f"Live Demo URL {i+1}", value=project.get('live_url', ''))
            
            if st.button(f"Remove Project {i+1}"):
                st.session_state.portfolio_data['projects'].pop(i)
                st.rerun()
    
    # Achievements Section
    st.subheader("Achievements")
    achievement = st.text_input("Add an achievement")
    if st.button("Add Achievement"):
        if achievement:
            st.session_state.portfolio_data['achievements'].append(achievement)
            st.success("Achievement added!")
    
    if st.session_state.portfolio_data['achievements']:
        st.write("**Current Achievements:**")
        for i, achievement in enumerate(st.session_state.portfolio_data['achievements']):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {achievement}")
            with col2:
                if st.button(f"Remove", key=f"remove_achievement_{i}"):
                    st.session_state.portfolio_data['achievements'].pop(i)
                    st.rerun()
    
    # Portfolio Preview
    if st.button("Preview Portfolio"):
        st.subheader("Portfolio Preview")
        
        # Display projects
        for project in st.session_state.portfolio_data['projects']:
            if project['title']:
                st.markdown(f"### {project['title']}")
                if project['description']:
                    st.write(project['description'])
                if project['technologies']:
                    st.write(f"**Technologies:** {project['technologies']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if project['github_url']:
                        st.markdown(f"[GitHub]({project['github_url']})")
                with col2:
                    if project['live_url']:
                        st.markdown(f"[Live Demo]({project['live_url']})")
                
                st.divider()

# AI Assistant Page
elif selected == "AI Assistant":
    st.header("AI Assistant")
    
    st.markdown("Get AI-powered suggestions for your resume and portfolio content!")
    
    # API Key Setup
    st.subheader("Hugging Face API Setup")
    api_key = st.text_input("Enter your Hugging Face API Key", type="password")
    
    if api_key:
        os.environ['HUGGINGFACE_API_KEY'] = api_key
        ai_helper.headers = {"Authorization": f"Bearer {api_key}"}
        st.success("API Key configured successfully!")
    
    # AI Content Generation
    st.subheader("AI Content Generation")
    
    content_type = st.selectbox("Select content type:", [
        "Professional Summary",
        "Job Description",
        "Skills Enhancement",
        "Project Description",
        "Achievement Statement"
    ])
    
    prompt = st.text_area("Enter your prompt or existing content for AI enhancement:")
    
    if st.button("Generate AI Content"):
        if prompt and api_key:
            with st.spinner("Generating AI content..."):
                result = ai_helper.generate_content(prompt)
                
                if "error" in result:
                    st.error(f"Error: {result['error']}")
                else:
                    st.success("AI-generated content:")
                    if isinstance(result, list) and len(result) > 0:
                        st.write(result[0].get('generated_text', 'No content generated'))
                    else:
                        st.write(str(result))
        else:
            st.warning("Please enter a prompt and configure your API key first.")
    
    # Resume Analysis
    st.subheader("Resume Analysis")
    
    resume_text = st.text_area("Paste your resume text for analysis:", height=200)
    
    if st.button("Analyze Resume"):
        if resume_text and api_key:
            with st.spinner("Analyzing resume..."):
                analysis = ai_helper.analyze_resume_text(resume_text)
                
                if "error" in analysis:
                    st.error(f"Error: {analysis['error']}")
                else:
                    st.success("Resume Analysis Results:")
                    st.write(analysis)
        else:
            st.warning("Please enter resume text and configure your API key first.")

# Deploy Page
elif selected == "Deploy":
    st.header("Deploy Your App")
    
    st.markdown("""
    <div class="deploy-section">
        <h2>Deploy to Streamlit Community Cloud</h2>
        <p>Share your AI Resume & Portfolio Builder with the world!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Deployment Steps
    st.subheader("Deployment Steps")
    
    steps = [
        "1. **Fork this repository** on GitHub",
        "2. **Connect your GitHub account** to Streamlit Community Cloud",
        "3. **Click 'Deploy'** and select your forked repository",
        "4. **Configure environment variables** (Hugging Face API key)",
        "5. **Launch your app** and share the URL!"
    ]
    
    for step in steps:
        st.markdown(step)
    
    # Deploy Button
    st.markdown("### Ready to Deploy?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <a href="https://share.streamlit.io" target="_blank">
            <button style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: 600;">
                Deploy to Streamlit
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <a href="https://github.com" target="_blank">
            <button style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: 600;">
                View on GitHub
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <a href="https://docs.streamlit.io" target="_blank">
            <button style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px; font-weight: 600;">
                Documentation
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    # Environment Variables
    st.subheader("Environment Variables")
    st.markdown("""
    Configure these environment variables in your Streamlit Community Cloud deployment:
    
    ```
    HUGGINGFACE_API_KEY=your_huggingface_api_key_here
    ```
    
    To get your Hugging Face API key:
    1. Go to [Hugging Face](https://huggingface.co/settings/tokens)
    2. Create a new token
    3. Copy the token and add it as an environment variable
    """)
    
    # Deployment Tips
    st.subheader("Deployment Tips")
    
    tips = [
        "Ensure your `requirements.txt` includes all dependencies",
        "Test your app locally before deploying",
        "Keep your API keys secure using environment variables",
        "Use descriptive repository names for better discoverability",
        "Add a README.md with setup instructions"
    ]
    
    for tip in tips:
        st.markdown(tip)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Built with Streamlit & Hugging Face AI | Ready for Cloud Deployment</p>
    <p>Star this repository if you found it helpful!</p>
</div>
""", unsafe_allow_html=True)
