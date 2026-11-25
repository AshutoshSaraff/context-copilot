import os
import hashlib
import requests
import streamlit as st

# =========================================================
# CONFIGURATION
# =========================================================

try:
    API_URL = st.secrets["API_URL"]
except Exception:
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Context Copilot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM STYLING
# Editorial Minimalism (dark)
# bg #0a0a0a | surface #111111 | border #1e1e1e | fg #fafafa
# accent #d4f756 (3 uses: primary button, brand mark, indexed dot)
# muted #737373 | Fraunces (hero h1) / Space Grotesk / JetBrains Mono
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@1,9..144,700&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500&display=swap');

    :root {
        --bg: #0a0a0a;
        --surface: #111111;
        --border: #1e1e1e;
        --fg: #fafafa;
        --muted: #737373;
        --body: #a3a3a3;
        --accent: #d4f756;
        --sans: 'Space Grotesk', ui-sans-serif, system-ui, sans-serif;
        --mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;
    }

    /* ---------- Base ---------- */
    html, body, .stApp, [data-testid="stAppViewContainer"],
    .stMarkdown, .stMarkdown p, label, button, input, textarea,
    [data-baseweb="select"] {
        font-family: var(--sans);
    }

    [data-testid="stIconMaterial"] {
        font-family: "Material Symbols Rounded" !important;
    }

    .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--fg);
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1120px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }

    hr, [data-testid="stDivider"] hr {
        border-color: var(--border) !important;
        opacity: 1;
    }

    :focus-visible {
        outline: 1px solid var(--fg) !important;
        outline-offset: 2px;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }

    .brand {
        font-size: 22px;
        font-weight: 500;
        color: var(--fg);
        letter-spacing: -0.04em;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .brand::before {
        content: "";
        width: 10px;
        height: 10px;
        background: var(--accent);
        display: inline-block;
    }

    .brand span { color: var(--muted); }

    .sub-brand {
        color: var(--muted);
        font-family: var(--mono);
        font-size: 11px;
        margin-top: 8px;
        letter-spacing: 0;
    }

    [data-testid="stSidebar"] h3 {
        font-family: var(--mono);
        font-size: 12px;
        font-weight: 500;
        color: var(--muted);
        letter-spacing: 0;
        padding: 0;
        margin-bottom: 4px;
    }

    /* ---------- Hero ---------- */
    .hero {
        padding: 24px 0 44px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 40px;
    }

    .hero h1 {
        font-family: 'Fraunces', serif;
        font-style: italic;
        font-weight: 700;
        color: var(--fg);
        font-size: clamp(44px, 7vw, 72px);
        line-height: 1.02;
        letter-spacing: -0.035em;
        margin: 0;
        padding: 0;
    }

    .hero p {
        color: var(--body);
        font-size: 20px;
        line-height: 1.5;
        max-width: 620px;
        margin: 22px 0 0;
    }

    /* ---------- Sample retrieval mockup (CSS only) ---------- */
    .mock {
        background: var(--surface);
        border: 1px solid var(--border);
        max-width: 780px;
        margin: 0 0 56px;
    }

    .mock-bar {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 12px 16px;
        border-bottom: 1px solid var(--border);
        font-family: var(--mono);
        font-size: 11px;
        color: var(--muted);
    }

    .mock-bar i {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #262626;
        display: inline-block;
    }

    .mock-bar span { margin-left: auto; }

    .mock-q {
        padding: 20px 16px;
        font-size: 16px;
        font-weight: 500;
        color: var(--fg);
    }

    .mock-row {
        display: grid;
        grid-template-columns: 56px 1fr 64px;
        gap: 16px;
        padding: 13px 16px;
        border-top: 1px solid var(--border);
        font-size: 13px;
        color: var(--body);
    }

    .mock-row b, .mock-row em {
        font-family: var(--mono);
        font-style: normal;
        font-weight: 400;
        font-size: 12px;
        color: var(--muted);
    }

    .mock-row em { text-align: right; }

    /* ---------- Features (asymmetric two-column) ---------- */
    .feature {
        display: grid;
        grid-template-columns: 1fr 2.4fr;
        gap: 32px;
        border-top: 1px solid var(--border);
        padding: 34px 0 38px;
    }

    .feature-label {
        font-family: var(--mono);
        font-size: 12px;
        color: var(--muted);
    }

    .feature-title {
        font-size: 26px;
        font-weight: 500;
        letter-spacing: -0.025em;
        line-height: 1.15;
        color: var(--fg);
        margin-bottom: 14px;
    }

    .feature p {
        color: var(--body);
        font-size: 15px;
        line-height: 1.65;
        max-width: 560px;
        margin: 0 0 12px;
    }

    @media (max-width: 768px) {
        .feature { grid-template-columns: 1fr; gap: 12px; }
    }

    /* ---------- Section labels & cards ---------- */
    .section-label {
        color: var(--muted);
        font-family: var(--mono);
        font-size: 12px;
        margin-bottom: 12px;
    }

    .info-card {
        background: var(--bg);
        border: 1px solid var(--border);
        padding: 16px;
        border-radius: 0;
        margin-bottom: 12px;
    }

    .info-card-title {
        color: var(--fg);
        font-size: 14px;
        font-weight: 500;
        word-break: break-word;
    }

    .info-card-text {
        color: var(--muted);
        font-size: 12px;
        margin-top: 8px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: transparent;
        color: var(--body);
        font-family: var(--mono);
        font-size: 11px;
        font-weight: 500;
    }

    .status-pill::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: var(--accent);
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        border-radius: 0;
        font-weight: 500;
        min-height: 42px;
        background: transparent;
        color: var(--fg);
        border: 1px solid #2a2a2a;
        transition: border-color 0.15s ease, background 0.15s ease;
    }

    .stButton > button:hover {
        background: var(--surface);
        border-color: var(--fg);
        color: var(--fg);
    }

    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: var(--accent);
        border-color: var(--accent);
        color: #0a0a0a;
    }

    .stButton > button[kind="primary"] *,
    .stButton > button[data-testid="stBaseButton-primary"] * {
        color: #0a0a0a;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        background: var(--accent);
        border-color: var(--accent);
        filter: brightness(1.08);
    }

    .stButton > button:disabled {
        opacity: 0.35;
        cursor: not-allowed;
    }

    /* Destructive action stays quiet: outline, not accent */
    [data-testid="stExpander"] .stButton > button[kind="primary"],
    [data-testid="stExpander"] .stButton > button[data-testid="stBaseButton-primary"] {
        background: transparent;
        border-color: var(--fg);
        color: var(--fg);
    }

    [data-testid="stExpander"] .stButton > button[kind="primary"] *,
    [data-testid="stExpander"] .stButton > button[data-testid="stBaseButton-primary"] * {
        color: var(--fg);
    }

    /* ---------- Inputs ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--bg);
        border: 1px dashed #2a2a2a;
        border-radius: 0;
    }

    [data-baseweb="select"] > div {
        background: var(--bg);
        border: 1px solid var(--border);
        border-radius: 0;
    }

    [data-baseweb="popover"] > div, [data-baseweb="popover"] ul {
        background: var(--surface);
        border-radius: 0;
    }

    [data-testid="stMetric"] { padding: 0; }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
        font-size: 12px;
    }

    [data-testid="stMetricValue"] {
        font-family: var(--mono);
        font-weight: 500;
        font-size: 30px;
        color: var(--fg);
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        font-family: var(--mono);
        font-size: 12px;
        color: var(--muted);
    }

    /* ---------- Alerts ---------- */
    [data-testid="stAlert"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 0;
        color: var(--fg);
    }

    /* ---------- Expanders ---------- */
    div[data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 0;
    }

    div[data-testid="stExpander"] details {
        border: none !important;
        border-radius: 0 !important;
        background: transparent !important;
    }

    /* ---------- Chat ---------- */
    [data-testid="stMain"] h3, .main h3 {
        font-size: 26px;
        font-weight: 500;
        letter-spacing: -0.025em;
        color: var(--fg);
        padding: 0;
    }

    .stChatMessage, [data-testid="stChatMessage"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 0;
        padding: 16px 20px;
    }

    [data-testid="stChatMessageAvatarUser"] {
        background: var(--border);
        color: var(--fg);
        border-radius: 0;
    }

    [data-testid="stChatMessageAvatarAssistant"] {
        background: var(--fg);
        color: #0a0a0a;
        border-radius: 0;
    }

    [data-testid="stBottom"] > div { background: var(--bg); }

    [data-testid="stChatInput"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 0;
    }

    [data-testid="stChatInput"]:focus-within { border-color: var(--fg); }

    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] textarea {
        background: transparent;
        border-radius: 0;
    }

    /* ---------- Footer ---------- */
    .footer {
        color: #525252;
        font-family: var(--mono);
        font-size: 11px;
        text-align: left;
        padding: 12px 0;
        line-height: 1.6;
    }

    @media (prefers-reduced-motion: reduce) {
        * { transition: none !important; }
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

if "active_document_id" not in st.session_state:
    st.session_state.active_document_id = None

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

# =========================================================
# API HELPERS
# =========================================================

def get_documents():
    response = requests.get(
        f"{API_URL}/documents",
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("documents", [])


def upload_document(uploaded_file):
    response = requests.post(
        f"{API_URL}/documents/upload",
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        },
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def process_document(document_id):
    response = requests.post(
        f"{API_URL}/documents/{document_id}/process",
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def delete_document(document_id):
    response = requests.delete(
        f"{API_URL}/documents/{document_id}",
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def ask_question(question, document_id):
    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": question,
            "document_id": document_id,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def get_error_message(exc):
    if exc.response is not None:
        try:
            return exc.response.json().get("detail", exc.response.text)
        except ValueError:
            return exc.response.text
    return str(exc)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">Context<span>Copilot</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sub-brand">Organizational knowledge assistant</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # -------------------------
    # Upload section
    # -------------------------

    st.markdown("### Upload knowledge")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help="Upload an unencrypted PDF file.",
    )

    if st.button(
        "Upload and process",
        disabled=uploaded_file is None,
        use_container_width=True,
        type="primary",
    ):
        try:
            with st.spinner("Uploading document..."):
                upload_result = upload_document(uploaded_file)

            document_id = upload_result["document"]["document_id"]

            with st.spinner("Extracting, chunking and indexing..."):
                process_result = process_document(document_id)

            st.session_state.active_document_id = document_id
            st.success("Document indexed successfully!")
            st.json(process_result)
            st.rerun()

        except requests.RequestException as exc:
            st.error(f"Upload or processing failed: {get_error_message(exc)}")

        except (KeyError, ValueError) as exc:
            st.error(f"Unexpected API response: {exc}")

    st.divider()

    # -------------------------
    # Knowledge base
    # -------------------------

    st.markdown("### Knowledge base")

    col_refresh, col_count = st.columns([1, 1])

    with col_refresh:
        refresh_clicked = st.button(
            "Refresh",
            use_container_width=True,
        )

    try:
        documents = get_documents()

    except requests.RequestException as exc:
        documents = None
        st.error(f"Backend unavailable: {get_error_message(exc)}")

    if documents is None:
        st.stop()

    if documents is not None:

        completed_documents = [
            doc for doc in documents
            if doc.get("status") == "completed"
        ]

        with col_count:
            st.metric("Indexed documents", len(completed_documents))

        if completed_documents:

            document_options = {
                doc["document_id"]: doc["filename"]
                for doc in completed_documents
            }

            document_ids = list(document_options.keys())

            current_id = st.session_state.active_document_id

            default_index = (
                document_ids.index(current_id)
                if current_id in document_ids
                else 0
            )

            # Change widget key when document list changes.
            # This prevents stale selections after deletion.
            ids_signature = hashlib.md5(
                "|".join(document_ids).encode()
            ).hexdigest()[:10]

            selected_document_id = st.selectbox(
                "Select document",
                options=document_ids,
                index=default_index,
                format_func=lambda doc_id: document_options[doc_id],
                key=f"document_selector_{ids_signature}",
            )

            st.session_state.active_document_id = selected_document_id

            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-card-title">{
                        document_options[selected_document_id]
                    }</div>
                    <div class="info-card-text">
                        <span class="status-pill">Indexed</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # -------------------------
            # Delete document
            # -------------------------

            with st.expander("Document management"):

                st.warning(
                    "Deleting a document permanently removes its "
                    "uploaded file and indexed chunks."
                )

                confirm_delete = st.checkbox(
                    "I understand. Delete this document.",
                    key=f"confirm_delete_{selected_document_id}",
                )

                if st.button(
                    "Delete document",
                    disabled=not confirm_delete,
                    use_container_width=True,
                    type="primary",
                ):
                    try:
                        with st.spinner("Deleting document..."):
                            delete_document(selected_document_id)

                        st.session_state.conversations.pop(
                            selected_document_id,
                            None,
                        )

                        st.session_state.active_document_id = None

                        st.success("Document deleted successfully.")
                        st.rerun()

                    except requests.RequestException as exc:
                        st.error(
                            f"Deletion failed: {get_error_message(exc)}"
                        )

        else:
            st.info("No processed documents available.")

            st.session_state.active_document_id = None

    st.divider()

    st.markdown(
        f"""
        <div class="footer">
            Connected API<br>
            {API_URL}
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# MAIN DASHBOARD
# =========================================================

st.markdown("""
<div class="hero">
<h1>Knowledge, connected.</h1>
<p>Search your documents, retrieve relevant information, and get answers grounded in your knowledge base.</p>
</div>
""", unsafe_allow_html=True)

document_id = st.session_state.active_document_id

if not document_id:

    st.markdown("""
<div class="mock">
<div class="mock-bar"><i></i><i></i><i></i><span>sample retrieval</span></div>
<div class="mock-q">What notice is required to terminate the agreement?</div>
<div class="mock-row"><b>p. 14</b><span>Either party may terminate this agreement with sixty days written notice.</span><em>0.1342</em></div>
<div class="mock-row"><b>p. 15</b><span>Termination for cause takes effect immediately upon written notice.</span><em>0.1876</em></div>
<div class="mock-row"><b>p. 3</b><span>The initial term of this agreement is twelve months from the effective date.</span><em>0.2410</em></div>
</div>

<div class="feature">
<div class="feature-label">Ingest</div>
<div>
<div class="feature-title">Every page, parsed and indexed.</div>
<p>Upload an unencrypted PDF and the backend extracts the text page by page, splits it into chunks, and stores an embedding for each one.</p>
<p>Page numbers travel with every chunk, so any passage can be traced back to where it came from.</p>
</div>
</div>

<div class="feature">
<div class="feature-label">Retrieve</div>
<div>
<div class="feature-title">Questions match meaning, not keywords.</div>
<p>Your question is embedded and compared against the document's chunks with vector search, so a query about ending a contract can find a clause titled Termination.</p>
<p>Each result carries its cosine distance. Lower means closer, which tells you how far to trust a match.</p>
</div>
</div>

<div class="feature">
<div class="feature-label">Answer</div>
<div>
<div class="feature-title">Answers you can check.</div>
<p>The reply is written from the retrieved passages instead of from general knowledge.</p>
<p>Open Retrieved sources under any answer to read the exact text and page it was built from.</p>
</div>
</div>
""", unsafe_allow_html=True)

    st.info(
        "Upload and process a PDF from the sidebar to start chatting."
    )

    st.stop()

# =========================================================
# CHAT INTERFACE
# =========================================================

conversation = st.session_state.conversations.setdefault(
    document_id,
    [],
)

document_name = next(
    (
        doc["filename"]
        for doc in documents
        if doc["document_id"] == document_id
    ),
    "Selected document",
)

chat_col, action_col = st.columns([5, 1])

with chat_col:
    st.markdown("### Document assistant")
    st.caption(f"Currently searching: {document_name}")

with action_col:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.conversations[document_id] = []
        st.rerun()

st.divider()

# -------------------------
# Display conversation
# -------------------------

for item in conversation:

    with st.chat_message(item["role"]):
        st.markdown(item["content"])

        if item["role"] == "assistant" and item.get("sources"):

            with st.expander(
                f"Retrieved sources ({len(item['sources'])})"
            ):

                for index, source in enumerate(
                    item["sources"],
                    start=1,
                ):
                    st.markdown(
                        f"**Source {index} — Page "
                        f"{source.get('page_number', 'N/A')}**"
                    )

                    st.caption(
                        f"Cosine distance: {source['distance']:.4f}"
                    )

                    st.write(source["text"])
                    st.divider()

# -------------------------
# Chat input
# -------------------------

question = st.chat_input(
    "Ask something about your document..."
)

if question:

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching and generating answer..."):

            try:
                result = ask_question(question, document_id)

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:

                    with st.expander(
                        f"Retrieved sources ({len(sources)})"
                    ):

                        for index, source in enumerate(
                            sources,
                            start=1,
                        ):
                            st.markdown(
                                f"**Source {index} — Page "
                                f"{source.get('page_number', 'N/A')}**"
                            )

                            st.caption(
                                f"Cosine distance: {source['distance']:.4f}"
                            )

                            st.write(source["text"])
                            st.divider()

                conversation.append({
                    "role": "user",
                    "content": question,
                })

                conversation.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except requests.RequestException as exc:
                st.error(
                    f"Chat request failed: {get_error_message(exc)}"
                )

            except (KeyError, ValueError) as exc:
                st.error(f"Unexpected API response: {exc}")

    st.rerun()
