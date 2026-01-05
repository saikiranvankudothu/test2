# 📄 Multimodal Document Intelligence System

_A Transformer-Powered Workflow for Extraction, OCR, RAG, Q&A, Summarization & Mindmap Generation Using Groq LLM_

---

## 🚀 Overview

As unstructured documents continue to grow—PDFs, scanned images, research papers, handwritten notes, legal documents—organizations need systems that can **interpret, analyze, and interact** with their documents intelligently.

This project is a **complete end-to-end Document Intelligence Platform** that provides:

- 🔍 Intelligent text extraction (Docling + EasyOCR + TrOCR)
- 🧠 Layout-aware parsing of PDFs
- ✍️ Handwriting recognition
- 🧩 Document chunking & vector search (RAG)
- ❓ Semantic Q&A using Groq LLM with zero hallucinations
- 📝 Automated summarization
- 🧭 Mermaid.js Mindmap generation
- 🖥️ Beautiful split-view UI (PDF viewer + AI workspace)
- 🌗 Dark/Light mode
- 💬 Chat-style interactive interface
- ⚡ Smooth-loading animations (shimmer skeleton)

### Suitable for:

- Legal document analysis
- Academic research processing
- Enterprise report summarization
- Multimodal handwritten document workflows
- AI-assisted data extraction
- Intelligent knowledge visualization

---

## 🧠 Key Features

### **1. Multimodal Extraction Layer**

| Document Type     | Engine Used       | Output                    |
| ----------------- | ----------------- | ------------------------- |
| Digital PDF       | Docling           | Text + Markdown + JSON    |
| Scanned (printed) | EasyOCR           | Plain text                |
| Handwritten       | TrOCR (Microsoft) | Handwriting transcription |
| Mixed             | Auto-detected     | Hybrid extraction         |

---

### **2. Retrieval-Augmented Generation (RAG)**

- Text cleanup & chunking (250 tokens + overlap)
- Dense embeddings using **GTE-base**
- Vector search with **ChromaDB**
- Top-k retrieval for highly accurate answers
- Context is cleaned before LLM consumption to remove noise

---

### **3. Groq LLM Intelligence Layer**

Powered by **Llama-3.3-70B Versatile** (via Groq API):

- Real-time semantic Q&A
- Multi-level summarization
- Structural document understanding
- Mermaid.js mindmap generation
- Ultra-low-latency inference

---

### **4. Modern, Premium UI**

- 📄 Left → PDF viewer (PDF.js)
- 🤖 Right → AI Workspace
- Tabs: Extracted text, Chat, Summary, Mindmap
- Smooth animations
- Dark + Light theme toggle
- Mermaid mindmap live rendering

---

## ⚙️ Installation Guide

### **1. Clone the repository**

```bash
git clone https://github.com/yourusername/DIS.git
cd DIS
```

### **2. Install dependencies by uv and activate .venv**

```
uv sync
.venv\Scripts\activate.bat
```

### **Add .env file**

```
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.3-70b-versatile
FLASK_ENV=development
```

### **Run the application**

```
uv run python app.py
```
