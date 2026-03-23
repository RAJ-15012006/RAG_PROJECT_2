# 🤖 AI RAG Chatbot (Next.js + FastAPI + Streamlit)

A modern **Retrieval-Augmented Generation (RAG) AI chatbot** that allows users to upload documents and interact with them using natural language.

The system uses **vector embeddings + LLMs + semantic search** to generate accurate answers grounded in the uploaded documents.

Built with a **modern full-stack architecture** using **Next.js, FastAPI, Streamlit, and LangChain**.

---

# 🚀 Features

* 📄 Upload PDF documents
* 🔍 Semantic search using vector embeddings
* 🤖 AI-powered question answering
* ⚡ Fast retrieval using vector database
* 💬 Interactive chat interface
* 🧠 Context-aware responses
* 📊 Clean UI dashboard
* 🔗 REST API backend

---

# 🏗️ Architecture

```
User
 │
 ▼
Next.js Frontend (Chat UI)
 │
 ▼
FastAPI Backend
 │
 ├── Document Processing
 │      ├─ PDF Loader
 │      ├─ Text Splitter
 │      └─ Embedding Model
 │
 ├── Vector Database
 │      └─ ChromaDB
 │
 └── LLM Model
        └─ Ollama / OpenAI
```

---

# 🧰 Tech Stack

### Frontend

* Next.js
* TypeScript
* TailwindCSS
* Shadcn UI

### Backend

* FastAPI
* Python

### AI / ML

* LangChain
* Ollama / OpenAI
* Chroma Vector Database
* Sentence Transformers

### Tools

* Git
* Docker
* Streamlit (for rapid testing UI)

---

# 📂 Project Structure

```
rag-chatbot/
│
├── frontend/
│     └── Next.js UI
│
├── backend/
│     ├── main.py
│     ├── rag_pipeline.py
│     ├── embeddings.py
│     └── api_routes.py
│
├── data/
│     └── uploaded_documents
│
├── vectorstore/
│     └── chroma_db
│
├── streamlit_app/
│     └── app.py
│
└── README.md
```

---

# ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/rag-chatbot.git

cd rag-chatbot
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv

venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Start backend

```bash
uvicorn main:app --reload
```

Backend runs on

```
http://localhost:8000
```

---

### 5️⃣ Run frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on

```
http://localhost:3000
```

---

### 6️⃣ Run Streamlit UI (optional)

```bash
streamlit run app.py
```

---

# 🧠 How It Works

1. User uploads a PDF
2. PDF is split into smaller chunks
3. Each chunk is converted into vector embeddings
4. Embeddings are stored in **ChromaDB**
5. When a user asks a question:

   * Relevant chunks are retrieved
   * Passed to the LLM as context
   * LLM generates an accurate answer

---

# 📸 Demo

Add screenshots here

```
/screenshots/chat-ui.png
/screenshots/upload-ui.png
```

---

# 🔮 Future Improvements

* Multi-document retrieval
* Voice assistant integration
* Agent-based workflow
* Real-time streaming responses
* Authentication system
* Cloud deployment (AWS / Railway / Render)

---

# 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

# 📜 License

MIT License

---

# 👨‍💻 Author

**Raj Kumar**

AI / Machine Learning Enthusiast
Building intelligent AI systems using LLMs.

---
