import streamlit as st
import base64
import time
from pathlib import Path
import ollama

# =========================================================
# ZENTRA AI - OLLAMA CLOUD CONNECTION
# =========================================================

MODEL_NAME = "gpt-oss:120b"

client = ollama.Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {st.secrets['OLLAMA_API_KEY']}"
    }
)


def get_zentra_response(messages):

    ollama_messages = [
        {
            "role": "system",
            "content": (
                "You are ZENTRA AI, a helpful, friendly, "
                "intelligent AI assistant. "
                "You help users learn, write code, solve problems, "
                "brainstorm ideas, and answer questions. "
                "Give clear, accurate, and useful answers."
            )
        }
    ]

    # Add conversation history
    for message in messages:
        ollama_messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    # Send request to Ollama Cloud
    stream = client.chat(
        model=MODEL_NAME,
        messages=ollama_messages,
        stream=True
    )

    # Stream the AI response
    for chunk in stream:
        content = chunk["message"]["content"]

        if content:
            yield content
# =========================================================
# ZENTRA AI - CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ZENTRA AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "Home"

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"


# =========================================================
# BACKGROUND IMAGE
# Place mountain_background.png beside this Python file
# =========================================================

BACKGROUND_PATH = Path(__file__).parent / "mountain_background.png"

background_rule = """
linear-gradient(
    180deg,
    rgba(14, 5, 28, 0.22),
    rgba(9, 5, 23, 0.35)
),
linear-gradient(135deg, #100720, #241044)
"""

if BACKGROUND_PATH.exists():
    with open(BACKGROUND_PATH, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    background_rule = f"""
    linear-gradient(
        180deg,
        rgba(14, 5, 28, 0.20),
        rgba(9, 5, 23, 0.40)
    ),
    url("data:image/png;base64,{encoded_image}")
    """


# =========================================================
# CSS / UI
# =========================================================

css = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --violet: #9b4dff;
    --cyan: #28d8ff;
    --white: #f8f3ff;
}

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

/* MAIN APP BACKGROUND */

.stApp {
    background-image: __BACKGROUND__;
    background-color: #100720;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stMain"] {
    background: transparent !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 1rem;
    padding-bottom: 7rem;
}

/* ANIMATED BACKGROUND GLOW */

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background:
        radial-gradient(
            circle at 15% 20%,
            rgba(151, 54, 255, 0.12),
            transparent 40%
        ),
        radial-gradient(
            circle at 85% 70%,
            rgba(40, 216, 255, 0.08),
            transparent 40%
        );

    animation: auroraMove 12s ease-in-out infinite alternate;
}

@keyframes auroraMove {
    0% {
        transform: translate3d(-2%, -1%, 0);
        opacity: 0.55;
    }

    100% {
        transform: translate3d(2%, 1%, 0);
        opacity: 1;
    }
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        rgba(31, 16, 50, 0.92),
        rgba(19, 16, 39, 0.96)
    ) !important;

    border-right: 1px solid rgba(194, 145, 255, 0.25);
    backdrop-filter: blur(25px);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem;
}

/* BRAND */

.brand-wrap {
    display: flex;
    align-items: center;
    gap: 13px;
    margin: 8px 5px 26px;
}

.brand-logo {
    width: 54px;
    height: 54px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 30px;
    font-weight: 700;
    color: #c5f8ff;

    background: radial-gradient(
        circle at 30% 25%,
        #512f98,
        #151c4a 72%
    );

    border: 2px solid #9d58ff;

    box-shadow:
        0 0 16px #923dff,
        inset 0 0 14px #42c8ff55;

    animation: logoGlow 4s ease-in-out infinite;
}

@keyframes logoGlow {
    0%, 100% {
        box-shadow:
            0 0 12px #923dff,
            inset 0 0 10px #42c8ff55;
    }

    50% {
        box-shadow:
            0 0 24px #923dff,
            inset 0 0 18px #42c8ff80;
    }
}

.brand-name {
    font-size: 19px;
    font-weight: 650;
    letter-spacing: 0.4px;
    color: white;
}

.brand-sub {
    color: #c3b3e4;
    font-size: 13px;
    margin-top: 2px;
}

.sidebar-caption {
    color: #bdb0d5;
    font-size: 13px;
    margin: 20px 5px 8px;
}

/* SIDEBAR BUTTONS */

.stButton > button {
    border: 1px solid rgba(189, 132, 255, 0.28);
    border-radius: 13px;
    color: #eee7ff;

    background: rgba(76, 42, 115, 0.34);

    transition: all 0.25s ease;
}

.stButton > button:hover {
    border-color: #bd8bff;
    color: white;
    background: rgba(124, 60, 190, 0.45);

    box-shadow: 0 0 15px #994dff40;
    transform: translateY(-1px);
}

/* HEADER */

.topline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 13px 5px 8px;
    color: #e8dcff;
}

.topline-label {
    font-size: 14px;
    color: #c8b7ee;
}

.ready {
    font-size: 13px;
    color: #e4f8ff;
}

.ready-dot {
    color: #29e69a;
    text-shadow: 0 0 10px #29e69a;
}

/* PAGE TITLE */

.page-heading {
    font-size: 27px;
    font-weight: 750;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin-top: 24px;
    margin-bottom: 10px;
}

.page-subheading {
    color: #d0c0eb;
    font-size: 14px;
    margin-bottom: 24px;
}

/* CHAT MESSAGE ANIMATION */

@keyframes messageEnter {
    from {
        opacity: 0;
        transform: translateY(18px) scale(0.98);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* GENERAL CHAT MESSAGE */

[data-testid="stChatMessage"] {
    padding: 15px 18px !important;
    margin-bottom: 16px !important;
    border-radius: 22px !important;

    backdrop-filter: blur(20px);

    animation: messageEnter 0.45s cubic-bezier(.2,.8,.2,1) both;

    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

/* ASSISTANT - LEFT SIDE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: linear-gradient(
        135deg,
        rgba(28, 18, 52, 0.90),
        rgba(43, 26, 73, 0.82)
    ) !important;

    border: 1px solid rgba(158, 111, 255, 0.30) !important;

    margin-right: 12% !important;
    margin-left: 0 !important;

    box-shadow:
        0 8px 30px rgba(0, 0, 0, 0.12),
        inset 0 1px 0 rgba(255,255,255,0.05);
}

/* USER - RIGHT SIDE */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: linear-gradient(
        135deg,
        rgba(119, 54, 212, 0.90),
        rgba(80, 39, 153, 0.90)
    ) !important;

    border: 1px solid rgba(201, 151, 255, 0.48) !important;

    margin-left: 12% !important;
    margin-right: 0 !important;

    box-shadow:
        0 8px 30px rgba(96, 35, 190, 0.15),
        inset 0 1px 0 rgba(255,255,255,0.09);
}

/* MESSAGE HOVER */

[data-testid="stChatMessage"]:hover {
    transform: translateY(-2px);

    box-shadow:
        0 8px 35px rgba(145, 75, 255, 0.16);
}

/* CHAT TEXT */

[data-testid="stChatMessage"] p {
    color: #f8f3ff !important;
    font-size: 15px;
    line-height: 1.8;
}

/* CHAT CODE */

[data-testid="stChatMessage"] pre {
    border-radius: 14px !important;
    border: 1px solid rgba(171, 121, 255, 0.25);

    background: rgba(8, 7, 20, 0.72) !important;
}

[data-testid="stChatMessage"] code {
    color: #e6baff;
}

/* CHAT AVATARS */

[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(
        135deg,
        #913bff,
        #22cfff
    ) !important;

    border-radius: 50%;

    box-shadow:
        0 0 18px rgba(153, 75, 255, 0.35);
}

[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(
        135deg,
        #7040bd,
        #9d5cff
    ) !important;

    border-radius: 50%;
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    border: 1px solid rgba(178, 113, 255, 0.55) !important;
    border-radius: 24px !important;

    background: rgba(24, 13, 46, 0.90) !important;

    box-shadow:
        0 0 20px rgba(135, 69, 255, 0.12),
        inset 0 1px 0 rgba(255,255,255,0.04);

    backdrop-filter: blur(20px);

    transition: all 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #b77aff !important;

    box-shadow:
        0 0 0 2px rgba(154, 77, 255, 0.15),
        0 0 30px rgba(135, 69, 255, 0.25);
}

[data-testid="stChatInput"] textarea {
    color: white !important;
}

/* TYPING DOTS */

.typing-indicator {
    display: flex;
    gap: 6px;
    align-items: center;
    padding: 12px 16px;
}

.typing-indicator span {
    width: 8px;
    height: 8px;
    background: #b879ff;
    border-radius: 50%;

    animation: typingBounce 1.2s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typingBounce {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }

    30% {
        transform: translateY(-7px);
        opacity: 1;
        box-shadow: 0 0 12px #b879ff;
    }
}

/* PREMIUM CARD */

.upgrade {
    margin-top: 22px;
    border-radius: 19px;
    padding: 17px;

    background: rgba(98, 57, 139, 0.28);
    border: 1px solid #a76bff44;
    text-align: center;
}

.upgrade-icon {
    font-size: 25px;
    color: #bb7dff;
}

.upgrade h4 {
    margin: 7px 0;
    font-size: 15px;
    color: white;
}

.upgrade p {
    color: #c6b8dd;
    font-size: 12px;
    line-height: 1.55;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(151, 91, 255, 0.45);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(182, 125, 255, 0.75);
}

/* RESPONSIVE */

@media (max-width: 800px) {
    .block-container {
        padding-top: 0.5rem;
    }

    .page-heading {
        font-size: 23px;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        margin-left: 4% !important;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        margin-right: 4% !important;
    }

    .topline {
        padding-top: 5px;
    }
}
"""

css = css.replace("__BACKGROUND__", background_rule)

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # BRAND
    st.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-logo">Z</div>
            <div>
                <div class="brand-name">ZENTRA AI</div>
                <div class="brand-sub">Assistant</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # NAVIGATION
    for page, icon in [
        ("Home", "⌂"),
        ("Chat", "◌"),
        ("Archived", "▣"),
        ("Library", "▤"),
    ]:

        if st.button(
            f"{icon}   {page}",
            key=f"nav_{page}",
            use_container_width=True,
        ):
            st.session_state.active_page = page
            st.rerun()

    # WORKSPACE
    st.markdown(
        '<div class="sidebar-caption">Workspace</div>',
        unsafe_allow_html=True,
    )

    for item, icon in [
        ("New Project", "✧"),
        ("Image", "▧"),
        ("Presentation", "▷"),
        ("Reset", "⟳"),
        ("Image Tools", "▧"),
    ]:

        if st.button(
            f"{icon}   {item}",
            key=f"tool_{item}",
            use_container_width=True,
        ):

            if item == "Reset":
                st.session_state.messages = []
                st.session_state.active_page = "Home"
                st.session_state.chat_title = "New Chat"
                st.rerun()

            elif item == "New Project":
                st.session_state.messages = []
                st.session_state.active_page = "Home"
                st.session_state.chat_title = "New Chat"
                st.rerun()

            else:
                st.session_state.active_page = item
                st.rerun()

    # PREMIUM
    st.markdown(
        """
        <div class="upgrade">
            <div class="upgrade-icon">♛</div>
            <h4>Upgrade to premium</h4>
            <p>
                Unlock more features and get the best experience.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.button(
        "✨  Upgrade",
        key="upgrade",
        use_container_width=True,
    )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.active_page in ["Home", "Chat"]:

    st.markdown(
        '<div class="page-heading">Conversation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subheading">'
        'Chat with ZENTRA AI — your ideas start here.'
        '</div>',
        unsafe_allow_html=True,
    )

elif st.session_state.active_page != "Reset":

    st.markdown(
        f"""
        <div class="page-heading">
            {st.session_state.active_page}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        f"You selected {st.session_state.active_page}. "
        "Connect this workspace tool to its feature when you're ready."
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    avatar = "🤖" if message["role"] == "assistant" else "🔍"

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================

if st.session_state.active_page in ["Home", "Chat"]:

    prompt = st.chat_input("Message ZENTRA AI...")

    if prompt:

        # Add USER message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
        })

        # Display the new USER message
        with st.chat_message("user", avatar="🔍"):
            st.markdown(prompt)

        # -------------------------------------------------
        # DEMO AI RESPONSE
        # Replace with your real AI API call later.
        # -------------------------------------------------

       # =========================================================
# REAL AI RESPONSE - OLLAMA
# =========================================================

with st.chat_message("assistant", avatar="🤖"):

    try:
        # Connect to Ollama and stream the real AI response
        full_response = st.write_stream(
            get_zentra_response(st.session_state.messages)
        )

    except Exception as e:

        full_response = (
            "⚠️ Unable to connect to Ollama.\n\n"
            "Please make sure Ollama is installed, running, "
            "and your selected model is downloaded.\n\n"
            f"Error: {e}"
        )

        st.error(full_response)


# Save the real AI response
st.session_state.messages.append({
    "role": "assistant",
    "content": full_response
})


# =========================================================
# OTHER PAGES
# =========================================================

 
