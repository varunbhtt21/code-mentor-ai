import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Code Mentor AI",
    page_icon="🤖",
    layout="wide"
)

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Custom CSS for better UI
st.markdown("""
    <style>
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
    }
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

def get_ai_mentor_response(code):
    # Crafting a prompt that encourages learning rather than giving direct solutions
    prompt = f"""
    As a coding mentor, analyze this code:
    
    {code}
    
    Please:
    1. Don't provide direct solutions
    2. Guide the student to think about:
       - What test cases they should consider
       - Potential edge cases
       - Where bugs might occur
    3. Ask thought-provoking questions that will help them debug their own code
    4. Provide hints and suggestions for improvement
    5. Encourage good coding practices
    
    Format your response in a structured, easy-to-read way.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    # Header
    st.title("🤖 Code Mentor AI")
    st.markdown("### Your Personal Programming Guide")
    
    # Description
    st.markdown("""
    Welcome! I'm your AI coding mentor. I won't give you direct solutions, 
    but I'll help you think through problems and improve your coding skills.
    Paste your code below, and I'll guide you with helpful questions and suggestions.
    """)
    
    # Code input area
    code = st.text_area(
        "📝 Paste your code here:",
        height=200,
        placeholder="Paste your code here..."
    )
    
    # Submit button
    if st.button("Get Mentoring Feedback"):
        if code.strip():
            with st.spinner("Analyzing your code..."):
                # Create two columns for better layout
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### Your Code")
                    st.code(code, language="python")
                
                with col2:
                    st.markdown("### Mentor's Feedback")
                    feedback = get_ai_mentor_response(code)
                    st.markdown(feedback)
        else:
            st.error("Please paste some code first!")

if __name__ == "__main__":
    main()
