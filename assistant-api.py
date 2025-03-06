import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

# Configure page settings
st.set_page_config(
    page_title="Code Mentor AI (Assistant API)",
    page_icon="🤖",
    layout="wide"
)

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

def create_assistant():
    """Create or load an existing assistant"""
    assistant = client.beta.assistants.create(
        name="Code Mentor",
        instructions="""
        You are a coding mentor for students. When analyzing code:
        1. Identify main problems in simple language
        2. Suggest specific test cases
        3. Provide simple hints without giving direct solutions
        4. Use beginner-friendly explanations
        5. Keep responses brief and clear
        """,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-turbo-preview"
    )
    return assistant

def get_ai_mentor_response(code, assistant_id):
    """Get response from the AI assistant"""
    try:
        # Create a thread
        thread = client.beta.threads.create()

        # Add the message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Please analyze this code:\n\n{code}"
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                return "Sorry, there was an error analyzing your code."

        # Get the messages
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Return the latest assistant message
        return messages.data[0].content[0].text.value

    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    # Create or load assistant
    assistant = create_assistant()

    # Header
    st.title("🤖 Code Mentor AI (Assistant API)")
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
                    feedback = get_ai_mentor_response(code, assistant.id)
                    st.markdown(feedback)
        else:
            st.error("Please paste some code first!")

if __name__ == "__main__":
    main() 