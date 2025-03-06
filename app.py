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
    prompt = f"""
    Analyze this code and respond ONLY in this format:

    CODE TO ANALYZE:
    {code}

    PROBLEMS IN YOUR CODE:
    1. Simple problem description (Example: "Your loop starts from wrong number" or "You forgot to check negative numbers")
    2. Another problem if found (Example: "Program crashes when input is zero")
    
    TRY RUNNING WITH:
    1. Try this input: [give exact number or string to test]
    What should happen: [simple explanation]
    What actually happens: [simple explanation]
    
    SMALL HINT TO FIX:
    • Write hint in very simple words (Example: "Check what happens when input is 5" or "Try printing value of x inside loop")

    Use simple English. Explain like you're talking to a beginner. Give concrete examples.
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
