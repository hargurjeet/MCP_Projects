import streamlit as st
from utils.paper_tools import process_query

st.set_page_config(page_title="Research Chatbot", layout="wide")

# ⬇️ Custom CSS to style the chat input box
st.markdown("""
    <style>
        section[data-testid="stChatInput"] textarea {
           background-color: #2c2f33 !important;  /* Darker background */
            color: #ffffff !important;             /* White text */
            border: 2px solid #4B8BBE !important;  /* Streamlit Blue border */
            font-weight: 500 !important;
            border-radius: 8px !important;
        }

       /* Chat Input Container */
        section[data-testid="stChatInput"] {
            background-color: #1f2225 !important;
            padding: 1rem !important;
            border-top: 1px solid #4B8BBE !important;
        }
    </style>
""", unsafe_allow_html=True)

# Logo and Branding Header
# st.image("logo.png", width=150)
st.title("🧠 ResearchGPT")
st.caption("Your intelligent assistant for exploring research papers.")

# Toggle for dark/light mode
# mode = st.toggle("🌗 Toggle Dark Mode", value=False)
# if mode:
#     st.markdown("""
#         <style>
#             body {
#                 background-color: #1e1e1e;
#                 color: white;
#             }
#         </style>
#     """, unsafe_allow_html=True)

# Contextual suggestions
st.markdown("#### 🔍 Try asking:")
st.markdown("- Search papers on large language models")
st.markdown("- Summarize paper 2403.00001")
st.markdown("- Find research on agentic AI")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input at the bottom of the page
query = st.chat_input("Your Query:")

# Process user query
if query:
    st.session_state.chat_history.append(("user", query))
    with st.spinner("Bot is typing..."):
        try:
            response = process_query(query)
            st.session_state.chat_history.append(("bot", response))
        except Exception as e:
            response = f"Error: {str(e)}"
            st.session_state.chat_history.append(("bot", response))

# Display chat messages in reverse order
for role, msg in reversed(st.session_state.chat_history):
    with st.chat_message("user" if role == "user" else "assistant"):
        if role == "bot" and msg.strip().startswith("##"):
            # Card-style layout for results
            st.markdown("""<div style='padding: 1rem; background-color: #f0f2f6; border-radius: 10px;'>""", unsafe_allow_html=True)
            st.markdown(msg)
            st.markdown("""</div>""", unsafe_allow_html=True)
        else:
            st.markdown(msg)

# Minimal footer
st.markdown("---")
# st.markdown("Made with ❤️ by [Hargurjeet](https://www.linkedin.com/in/hargurjeet/)")

# Fixed bottom-right footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 0.875rem;
        color: gray;
        z-index: 9999;
    }
    </style>
    <div class="footer">
        Made with ❤️ by <a href="https://www.linkedin.com/in/hargurjeet/" target="_blank" style="color: gray; text-decoration: none;">Hargurjeet</a>
    </div>
    """,
    unsafe_allow_html=True
)


