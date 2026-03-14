"""
San Diego FAQ Bot - Streamlit Application
Powered by Claude Sonnet 4.6
"""

import streamlit as st
import os
from dotenv import load_dotenv
from data_loader import load_data
from bot import create_bot
import pandas as pd

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="San Diego Permit FAQ Bot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease-in;
        border: 1px solid rgba(0, 0, 0, 0.1);
    }
    .user-message {
        background-color: #667eea;
        color: white;
        margin-left: 20%;
        border-color: #667eea;
    }
    .bot-message {
        background-color: #f0f2f6;
        color: #1a1a1a;
        margin-right: 20%;
        border-color: #e1e4e8;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .bot-message {
            background-color: #2d2d2d;
            color: #e8e8e8;
            border-color: #444;
        }
    }
    
    /* Streamlit dark theme detection */
    [data-theme="dark"] .bot-message {
        background-color: #2d2d2d;
        color: #e8e8e8;
        border-color: #444;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Make chat input sticky at bottom */
    .stChatInput {
        position: sticky;
        bottom: 0;
        padding: 1rem 0;
        z-index: 100;
    }
    
    /* Fix chat input styling - remove black box in light mode */
    .stChatInput > div {
        border: 1px solid #e1e4e8 !important;
        background: transparent !important;
    }
    
    /* Dark mode for chat input */
    @media (prefers-color-scheme: dark) {
        .stChatInput > div {
            border: 1px solid #444 !important;
        }
    }
    
    [data-theme="dark"] .stChatInput > div {
        border: 1px solid #444 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_bot():
    """Initialize bot once and cache it"""
    with st.spinner("🔄 Loading San Diego data and initializing bot..."):
        data_loader = load_data()
        bot = create_bot(data_loader)
    return bot, data_loader


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏛️ San Diego Permit FAQ Bot</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize bot
    try:
        bot, data_loader = initialize_bot()
        st.success("✅ Bot ready! Ask me anything about San Diego permits.")
    except Exception as e:
        st.error(f"❌ Error initializing bot: {str(e)}")
        st.info("💡 Make sure your ANTHROPIC_API_KEY is set in Streamlit secrets or .env file")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Data Overview")
        
        # Get data summary
        summary = data_loader.get_data_summary()
        stats = data_loader.get_permit_statistics()
        
        # Display stats
        if 'active_count' in stats:
            st.metric("Active Permits", f"{stats['active_count']:,}")
        if 'closed_count' in stats:
            st.metric("Closed Permits", f"{stats['closed_count']:,}")
        
        # Neighborhoods info
        if summary.get('neighborhoods', {}).get('communities'):
            communities_count = summary['neighborhoods']['communities']['rows']
            st.metric("Communities", communities_count)
        
        st.divider()
        
        st.header("ℹ️ About")
        st.markdown("""
        This bot uses:
        - Real San Diego permit data
        - Municipal code documents
        - Neighborhood information
        - AI-powered question answering
        
        **Data Sources:**
        - [San Diego Open Data Portal](https://data.sandiego.gov)
        - Development Services Dept.
        
        **Tech Stack:**
        - Claude Sonnet 4.6 (AI Model)
        - Streamlit (Web Framework)
        - Pandas (Data Processing)
        - Python
        
        **Developer:**  
        [Kedar Kulkarni](https://www.linkedin.com/in/kedar-kulkarni/)
        
        <p style="font-size: 0.85em; font-style: italic; color: #666; margin-top: 1rem;">
        <em>Disclaimer: This project is created for educational purposes using publicly available data from the City of San Diego Open Data Portal. The information provided is for general guidance only and should not be considered official advice. Always verify permit requirements and regulations with the San Diego Development Services Department.</em>
        </p>
        """, unsafe_allow_html=True)
        st.divider()
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs([
        "💬 Ask Questions", 
        "✅ Permit Checklist", 
        "📋 Meeting Summary"
    ])
    
    # Tab 1: Question & Answer Chat
    with tab1:
        st.subheader("Ask About San Diego Permits")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Create a container for chat messages with fixed height
        chat_container = st.container()
        
        with chat_container:
            # Display chat history
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>Bot:</strong><br>{message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input AT THE BOTTOM (before example questions)
        st.divider()
        prompt = st.chat_input("Ask a question about permits, regulations, or procedures...")
        
        if prompt:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Get bot response
            with st.spinner("🤔 Thinking..."):
                try:
                    response = bot.ask(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
            
            st.rerun()
        
        # Example questions AFTER the input
        st.markdown("**💡 Try asking:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("What permits do I need for a fence?", use_container_width=True):
                st.session_state.example_question = "What permits do I need for a fence?"
                st.rerun()
        
        with col2:
            if st.button("How long does permit approval take?", use_container_width=True):
                st.session_state.example_question = "How long does permit approval take?"
                st.rerun()
        
        # Handle example questions
        if hasattr(st.session_state, 'example_question'):
            question = st.session_state.example_question
            del st.session_state.example_question
            
            st.session_state.messages.append({"role": "user", "content": question})
            
            with st.spinner("🤔 Thinking..."):
                response = bot.ask(question)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    # Tab 2: Permit Checklist Generator
    with tab2:
        st.subheader("Generate Permit Checklist")
        st.markdown("Describe your project and get a customized permit checklist.")
        
        # Initialize project description in session state if not exists
        if 'project_description' not in st.session_state:
            st.session_state.project_description = ""
        
        # Handle example project selection
        if hasattr(st.session_state, 'selected_example_project'):
            st.session_state.project_description = st.session_state.selected_example_project
            del st.session_state.selected_example_project
        
        project_description = st.text_area(
            "Project Description",
            value=st.session_state.project_description,
            placeholder="Example: I want to build a 12x20 deck in my backyard with lighting",
            height=150,
            key="project_input"
        )
        
        # Update session state when text changes
        st.session_state.project_description = project_description
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            generate_button = st.button("🔍 Generate Checklist", use_container_width=True)
        
        if generate_button:
            if not project_description.strip():
                st.warning("⚠️ Please describe your project first")
            else:
                with st.spinner("📝 Generating your custom permit checklist..."):
                    try:
                        checklist = bot.generate_permit_checklist(project_description)
                        
                        st.success("✅ Checklist Generated!")
                        st.markdown("---")
                        st.markdown(checklist)
                        
                        # Download option as Markdown
                        st.download_button(
                            label="📥 Download Checklist",
                            data=f"# Permit Checklist\n\n**Project:** {project_description}\n\n{checklist}",
                            file_name="permit_checklist.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Example projects
        st.divider()
        st.markdown("**💡 Example Projects:**")
        
        examples = [
            "Build a detached garage",
            "Remodel kitchen with new electrical and plumbing",
            "Install solar panels on roof",
            "Add a bathroom to existing house"
        ]
        
        cols = st.columns(2)
        for i, example in enumerate(examples):
            with cols[i % 2]:
                if st.button(example, key=f"example_{i}", use_container_width=True):
                    st.session_state.selected_example_project = example
                    st.rerun()
    
    # Tab 3: Meeting Summary
    with tab3:
        st.subheader("Summarize Council Meetings by Neighborhood")
        st.markdown("Extract neighborhood-specific information from council meetings or transcripts.")
        
        # Get available communities for dropdown
        neighborhood_options = []
        
        try:
            if data_loader.neighborhoods_data and 'communities' in data_loader.neighborhoods_data:
                communities = data_loader.neighborhoods_data['communities']
                # Try different possible column names
                name_col = None
                for col in ['cpname', 'name', 'community', 'CPNAME', 'NAME']:
                    if col in communities.columns:
                        name_col = col
                        break
                
                if name_col:
                    community_list = sorted([str(name) for name in communities[name_col].unique() if pd.notna(name)])
                    neighborhood_options = community_list
                else:
                    st.warning("⚠️ Could not find neighborhood names in data")
        except Exception as e:
            st.warning(f"⚠️ Error loading neighborhoods: {str(e)}")
        
        # If no data loaded, provide manual options
        if not neighborhood_options:
            neighborhood_options = [
                "Barrio Logan", "City Heights", "Clairemont", "College Area", 
                "Downtown", "Golden Hill", "La Jolla", "Linda Vista", 
                "Mira Mesa", "Mission Valley", "North Park", "Ocean Beach",
                "Pacific Beach", "Point Loma", "Rancho Bernardo", "Scripps Ranch"
            ]
            st.info("ℹ️ Using default neighborhood list")
        
        # Neighborhood dropdown - more compact
        selected_neighborhood = st.selectbox(
            "Select Neighborhood",
            options=[""] + neighborhood_options,
            format_func=lambda x: "Choose a neighborhood..." if x == "" else x,
            help=f"{len(neighborhood_options)} neighborhoods available"
        )
        
        content = st.text_area(
            "Meeting Transcript or Content",
            placeholder="Paste council meeting transcript, agenda, or other content here...",
            height=250,
            help="Paste the full meeting transcript or relevant content to analyze"
        )
        
        if st.button("📊 Generate Summary", use_container_width=True):
            if not selected_neighborhood:
                st.warning("⚠️ Please select a neighborhood")
            elif not content.strip():
                st.warning("⚠️ Please provide meeting content")
            else:
                with st.spinner(f"📝 Analyzing content for {selected_neighborhood}..."):
                    try:
                        summary = bot.summarize_for_neighborhood(content, selected_neighborhood)
                        
                        st.success(f"✅ Summary for {selected_neighborhood}")
                        st.markdown("---")
                        st.markdown(summary)
                        
                        # Download option as Markdown
                        st.download_button(
                            label="📥 Download Summary",
                            data=f"# Summary for {selected_neighborhood}\n\n{summary}",
                            file_name=f"{selected_neighborhood.lower().replace(' ', '_')}_summary.md",
                            mime="text/markdown"
                        )
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>⚠️ This bot provides information for guidance only. 
        Always verify requirements with the San Diego Development Services Department.</p>
        <p>Data from <a href="https://data.sandiego.gov" target="_blank">San Diego Open Data Portal</a></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()