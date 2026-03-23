import streamlit as st
import os
import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(
    page_title="Transformer Research Assistant",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080612 !important;
    font-family: 'Inter', sans-serif !important;
    color: rgba(255,255,255,0.92);
    overflow-x: hidden;
}

/* ── 3D Canvas Background ── */
#three-canvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
}

/* ── Animated orbs ── */
.orb-container {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
}
@keyframes float-orb-1 {
    0%,100% { transform: translate(0,0) scale(1); }
    25%      { transform: translate(60px,-80px) scale(1.1); }
    50%      { transform: translate(-40px,-120px) scale(0.95); }
    75%      { transform: translate(80px,-40px) scale(1.05); }
}
@keyframes float-orb-2 {
    0%,100% { transform: translate(0,0) scale(1); }
    25%      { transform: translate(-80px,60px) scale(1.15); }
    50%      { transform: translate(50px,100px) scale(0.9); }
    75%      { transform: translate(-60px,-60px) scale(1.1); }
}
@keyframes float-orb-3 {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(100px,-50px) scale(1.08); }
    66%      { transform: translate(-70px,70px) scale(0.92); }
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.35;
}
.orb-1 {
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(99,60,220,0.7), transparent 70%);
    top: -5%; left: 10%;
    animation: float-orb-1 20s ease-in-out infinite;
}
.orb-2 {
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(34,180,180,0.5), transparent 70%);
    top: 45%; right: 5%;
    animation: float-orb-2 25s ease-in-out infinite;
}
.orb-3 {
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(200,60,220,0.45), transparent 70%);
    bottom: 5%; left: 35%;
    animation: float-orb-3 18s ease-in-out infinite;
}
.grid-pattern {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
}

/* ── 3D Header Card ── */
@keyframes glow-pulse {
    0%,100% { box-shadow: 0 0 30px rgba(99,102,241,0.25), 0 0 80px rgba(99,102,241,0.1), inset 0 1px 0 rgba(255,255,255,0.1); }
    50%      { box-shadow: 0 0 50px rgba(99,102,241,0.4), 0 0 120px rgba(99,102,241,0.2), inset 0 1px 0 rgba(255,255,255,0.15); }
}
@keyframes card-float {
    0%,100% { transform: perspective(1200px) rotateX(3deg) rotateY(-1deg) translateZ(0px); }
    50%      { transform: perspective(1200px) rotateX(1deg) rotateY(1deg) translateZ(10px); }
}
.header-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.04) 100%);
    backdrop-filter: blur(40px) saturate(2);
    -webkit-backdrop-filter: blur(40px) saturate(2);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 24px;
    padding: 2.2rem 2rem;
    text-align: center;
    margin: 1rem auto 1.5rem;
    max-width: 700px;
    animation: glow-pulse 3s ease-in-out infinite, card-float 6s ease-in-out infinite;
    position: relative;
    z-index: 2;
    overflow: hidden;
}
/* 3D shine sweep */
.header-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -60%;
    width: 40%; height: 200%;
    background: linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.08) 50%, transparent 60%);
    animation: shine-sweep 4s ease-in-out infinite;
}
@keyframes shine-sweep {
    0%   { left: -60%; }
    100% { left: 160%; }
}
.brain-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px; height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3));
    border: 1px solid rgba(99,102,241,0.4);
    font-size: 2rem;
    margin-bottom: 0.85rem;
    box-shadow: 0 0 20px rgba(99,102,241,0.3), 0 0 40px rgba(99,102,241,0.1);
    animation: icon-pulse 2s ease-in-out infinite;
}
@keyframes icon-pulse {
    0%,100% { box-shadow: 0 0 20px rgba(99,102,241,0.3), 0 0 40px rgba(99,102,241,0.1); }
    50%      { box-shadow: 0 0 30px rgba(99,102,241,0.5), 0 0 60px rgba(99,102,241,0.2); }
}
.header-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #c7d2fe 0%, #a5b4fc 40%, #818cf8 70%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
    text-shadow: none;
}
.header-sub {
    font-size: 0.7rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.38);
    margin-top: 0.5rem;
    font-weight: 500;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    margin-top: 0.85rem;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.2);
    font-size: 0.72rem;
    color: rgba(52,211,153,0.9);
    font-weight: 500;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #34d399;
    animation: pulse 2s ease-in-out infinite;
}

/* ── 3D Message Bubbles ── */
@keyframes msg-in {
    from { opacity: 0; transform: translateY(16px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
.msg-wrap {
    display: flex;
    margin: 0.5rem 0;
    animation: msg-in 0.4s cubic-bezier(0.16,1,0.3,1) forwards;
    position: relative;
    z-index: 2;
}
.msg-wrap.user      { justify-content: flex-end; }
.msg-wrap.assistant { justify-content: flex-start; }

.bubble-user {
    max-width: 78%;
    padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 4px 20px;
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
    color: white;
    font-size: 0.95rem;
    line-height: 1.65;
    font-weight: 500;
    box-shadow:
        0 8px 32px rgba(99,102,241,0.4),
        0 2px 8px rgba(99,102,241,0.2),
        inset 0 1px 0 rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.12);
    transform: perspective(600px) rotateY(-2deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    word-wrap: break-word;
}
.bubble-user:hover {
    transform: perspective(600px) rotateY(0deg) translateZ(4px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.5), inset 0 1px 0 rgba(255,255,255,0.2);
}
.bubble-assistant {
    max-width: 85%;
    padding: 1.1rem 1.4rem;
    border-radius: 20px 20px 20px 4px;
    background: linear-gradient(135deg, rgba(20,16,50,0.92) 0%, rgba(15,12,40,0.88) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.5),
        0 2px 8px rgba(0,0,0,0.3),
        inset 0 1px 0 rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.92);
    font-size: 0.95rem;
    line-height: 1.75;
    transform: perspective(600px) rotateY(2deg);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    word-wrap: break-word;
}
.bubble-assistant:hover {
    transform: perspective(600px) rotateY(0deg) translateZ(4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.1);
}
.source-badge {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #a5b4fc;
    font-size: 0.68rem;
    font-weight: 600;
    margin: 0.15rem 0.1rem;
    box-shadow: 0 0 8px rgba(99,102,241,0.2);
}
.sources-row { margin-top: 0.7rem; }

/* ── 3D Typing indicator ── */
@keyframes bounce-dot {
    0%,80%,100% { transform: scale(0.5) translateY(0); opacity: 0.3; }
    40%          { transform: scale(1) translateY(-4px); opacity: 1; }
}
.typing-wrap {
    display: flex;
    justify-content: flex-start;
    margin: 0.5rem 0;
    position: relative;
    z-index: 2;
}
.typing-bubble {
    padding: 0.9rem 1.3rem;
    border-radius: 20px 20px 20px 4px;
    background: linear-gradient(135deg, rgba(20,16,50,0.92), rgba(15,12,40,0.88));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
    display: flex;
    align-items: center;
    gap: 8px;
}
.typing-label { font-size: 0.72rem; color: rgba(255,255,255,0.45); font-weight: 500; }
.dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    animation: bounce-dot 1.4s ease-in-out infinite both;
    box-shadow: 0 0 6px rgba(129,140,248,0.5);
}
.dot:nth-child(3) { animation-delay: 0.16s; }
.dot:nth-child(4) { animation-delay: 0.32s; }

/* ── Input ── */
.stChatInput > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 18px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stChatInput > div:focus-within {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.2), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}
.stChatInput textarea { color: white !important; font-family: 'Inter', sans-serif !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 780px !important; }
</style>

<!-- Animated background -->
<div class="orb-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
<div class="grid-pattern"></div>

<!-- 3D Particle canvas -->
<canvas id="three-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('three-canvas');
    const ctx = canvas.getContext('2d');
    let W, H, particles = [], lines = [];
    const N = 60;

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < N; i++) {
        particles.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            r: Math.random() * 1.5 + 0.5,
            alpha: Math.random() * 0.5 + 0.2
        });
    }

    function draw() {
        ctx.clearRect(0, 0, W, H);
        // Draw connections
        for (let i = 0; i < N; i++) {
            for (let j = i + 1; j < N; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 150) {
                    ctx.beginPath();
                    ctx.strokeStyle = `rgba(129,140,248,${0.15 * (1 - dist/150)})`;
                    ctx.lineWidth = 0.5;
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
        }
        // Draw particles
        particles.forEach(p => {
            ctx.beginPath();
            const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 3);
            grad.addColorStop(0, `rgba(165,180,252,${p.alpha})`);
            grad.addColorStop(1, 'transparent');
            ctx.fillStyle = grad;
            ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2);
            ctx.fill();

            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > W) p.vx *= -1;
            if (p.y < 0 || p.y > H) p.vy *= -1;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>

<!-- Header -->
<div class="header-card">
    <div class="brain-icon">🧠</div>
    <div class="header-title">Transformer Research Assistant</div>
    <div class="header-sub">Attention Is All You Need &bull; RAG System</div>
    <div class="status-badge">
        <span class="status-dot"></span>
        System Online
    </div>
</div>
""", unsafe_allow_html=True)

# ── RAG Pipeline ────────────────────────────────────────────
@st.cache_resource(show_spinner="🔧 Initializing RAG pipeline...")
def load_rag():
    pdf_path = os.path.join(os.path.dirname(__file__), "backend", "data", "AttentionAllYouNeed.pdf")
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="llama3-8b-8192", api_key=groq_api_key)
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert AI research assistant specializing in the 'Attention Is All You Need' paper. "
            "Answer ONLY based on the context below. Be concise and specific. "
            "If the answer is not in the context, say 'I don't have that information.'\n\nContext:\n{context}"
        )),
        ("human", "{input}"),
    ])
    chain = (
        {"context": retriever | (lambda d: "\n\n".join(x.page_content for x in d)), "input": RunnablePassthrough()}
        | prompt | llm | StrOutputParser()
    )
    return chain, retriever

chain, retriever = load_rag()

# ── Session State ───────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm your <strong>Transformer Research Assistant</strong>. I've analyzed the <em>Attention Is All You Need</em> paper. Ask me anything! 🚀",
        "sources": [],
    }]

# ── Render messages ─────────────────────────────────────────
chat_html = ""
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += f'<div class="msg-wrap user"><div class="bubble-user">{msg["content"]}</div></div>'
    else:
        sources_html = ""
        if msg.get("sources"):
            badges = "".join(f'<span class="source-badge">📄 Page {s}</span>' for s in msg["sources"])
            sources_html = f'<div class="sources-row">{badges}</div>'
        chat_html += f'<div class="msg-wrap assistant"><div class="bubble-assistant">{msg["content"]}{sources_html}</div></div>'

st.markdown(f'<div style="position:relative;z-index:2">{chat_html}</div>', unsafe_allow_html=True)

# ── Chat Input ──────────────────────────────────────────────
if question := st.chat_input("Ask about the Transformer paper..."):
    content = question.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    st.markdown(f'<div class="msg-wrap user"><div class="bubble-user">{content}</div></div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": content, "sources": []})

    st.markdown("""
    <div class="typing-wrap">
        <div class="typing-bubble">
            <span class="typing-label">Thinking</span>
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
        </div>
    </div>""", unsafe_allow_html=True)

    try:
        docs = retriever.invoke(question)
        sources = sorted(set(doc.metadata.get("page", 0) + 1 for doc in docs))
        answer = chain.invoke(question)

        answer_html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', answer)
        answer_html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', answer_html)
        answer_html = answer_html.replace("\n", "<br>")

        badges = "".join(f'<span class="source-badge">📄 Page {s}</span>' for s in sources)
        sources_html = f'<div class="sources-row">{badges}</div>' if sources else ""

        st.markdown(f'<div class="msg-wrap assistant"><div class="bubble-assistant">{answer_html}{sources_html}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": answer_html, "sources": sources})

    except Exception as e:
        err = f"❌ Error: {str(e)}"
        st.markdown(f'<div class="msg-wrap assistant"><div class="bubble-assistant">{err}</div></div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": err, "sources": []})
