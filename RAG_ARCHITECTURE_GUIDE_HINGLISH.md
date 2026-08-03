# 🧠 Full RAG (Retrieval-Augmented Generation) Architecture Guide (Hinglish)

Yeh document hamare **AWS Serverless Observability** project mein Backend RAG system ki complete, detailed, aur step-by-step working ko explain karta hai.

---

## 📌 RAG Kya Hai Aur Kyun zaroori Hai?

Jab koi user LLM (ChatGPT / Gemini) se poochhta hai:
> *"Mere `send_message` Lambda function ki average latency kitni hai?"*

Generative AI Models (LLMs) ke paas aapke private PostgreSQL database ya CloudWatch logs ka access nahi hota.
Agar hum LLM ko direct poochhein, to woh guess karega ya galat answer dega (**Hallucination**).

**RAG (Retrieval-Augmented Generation)** is problem ko solve karta hai 3 main steps mein:
1. **Retrieval**: User ke question ke hisab se relevant database records / logs search karna.
2. **Augmentation**: Un retrieved data chunks ko Prompt ke saath jodhna (inject karna).
3. **Generation**: LLM se sachhe ground-truth context ke aadhar par accurate answer generate karwana.

---

## 🏗 System Architecture Diagram

```text
[ User Interface (Frontend Search Bar) ]
                   │
                   ▼ (POST /rag/query)
[ FastAPI Backend Router (app/api/rag.py) ]
                   │
                   ▼
[ RAG Service (app/services/rag_service.py) ]
                   │
    ┌──────────────┴─────────────────────────┐
    ▼                                        ▼
1. Embed User Query               2. Top-K Vector Search
 (app/rag/embedder.py)            (app/rag/vector_store.py)
    │                                        │
    └──────────────┬─────────────────────────┘
                   ▼
   [ Retrieved Ground-Truth Chunks ]
                   │
                   ▼
3. Prompt Augmentation & LLM Generation (app/rag/generator.py)
                   │
                   ▼
   [ Final Answer + Retrieved Sources ]
```

---

## 🗂 Code Folder Structure & Key Files

Backend mein RAG system completely modular aur systematic tarike se divided hai:

```text
backend/app/
├── rag/                           # 🧠 Dedicated RAG Engine Module
│   ├── __init__.py
│   ├── chunker.py                 # Text Chunking logic (Logs & Metrics split करना)
│   ├── embedder.py                # Vector Embeddings generation (Text to Math Vectors)
│   ├── vector_store.py            # Vector Storage & Cosine Similarity Search Engine
│   └── generator.py               # Prompt Augmenter & LLM Response Generator
├── services/
│   └── rag_service.py             # RAG Business Logic & Coordinator Service
├── api/
│   └── rag.py                     # FastAPI Endpoints (/rag/query, /rag/index)
└── schemas/
    └── rag.py                     # Request/Response Pydantic Models
```

---

## 🔍 Step-by-Step RAG Execution Pipeline Details

### Step 1: Data Ingestion & Chunking (`app/rag/chunker.py`)
- **Kyun zaroori hai?**: Raw logs aur metrics bahut bade hote hain. Pure document ko ek saath LLM ko nahi bheja ja sakta.
- **Kaise kaam karta hai?**: 
  - Hum PostgreSQL Database se `lambda_functions`, `cloudwatch_metrics`, aur `cloudwatch_logs` padhte hain.
  - Chunking Engine in records ko fixed-size semantic text chunks mein break karta hai:
    - **Chunk 1**: `Lambda Function: send_message | Memory: 1024MB | Timeout: 15s | Environment: Production`
    - **Chunk 2**: `Metric: Duration | Lambda: send_message | Value: 47.98ms | Timestamp: 2026-07-21`
    - **Chunk 3**: `Log: REPORT RequestId: 69cfff2d... | Duration: 47.98ms | Max Memory Used: 174MB`

### Step 2: Vector Embedding Generation (`app/rag/embedder.py`)
- **Kyun zaroori hai?**: Computers ko text samajhne ke liye text ko mathematical numbers (Vectors/Floating point arrays) mein convert karna padta hai.
- **Kaise kaam karta hai?**:
  - `TextEmbedder` class har text chunk ko ek **Vector Embedding** (e.g. 384-dimensional array like `[0.12, -0.45, 0.89, ...]`) mein convert karti hai.
  - Text: `"high memory lambda function"` ➔ Vector: `[0.08, 0.91, -0.33, ...]`.
  - In vectors se semantic meaning capture hoti hai (jaise "latency" aur "duration" dono pass-pass vectors honge).

### Step 3: Vector Indexing & Similarity Search (`app/rag/vector_store.py`)
- **Kyun zaroori hai?**: User ke query vector ke sabse paas wale (most similar) data chunks dhoondhna.
- **Kaise kaam karta hai?**:
  - `VectorStore` class sabhi chunks aur unke vectors ko memory/disk par index karti hai.
  - Jab query aati hai, hum **Cosine Similarity** (Vector Mathematics) ka use karke top-$K$ ($K=3$ ya $5$) highest similarity score wale chunks select karte hain.

$$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

### Step 4: Prompt Augmentation & Generation (`app/rag/generator.py`)
- **Kyun zaroori hai?**: Retrieved context ko system prompt ke saath append karke LLM se intelligent answer mangwana.
- **Prompt Structure**:
```text
System: You are an AWS Serverless Observability Expert. Use ONLY the following ground-truth retrieved context to answer the user's question.

Retrieved Context:
[Context 1]: Lambda send_message has avg duration 47.98ms.
[Context 2]: Lambda read_market_data memory is 1024MB.

User Question: Which function has high duration?
Answer:
```

---

## ⚡ API Endpoints (`app/api/rag.py`)

1. **`POST /rag/query`**
   - **Input**: `{"query": "Which lambda function is slowest?"}`
   - **Output**:
     ```json
     {
       "answer": "Based on retrieved metrics, send_message has the highest average duration of 47.98 ms.",
       "retrieved_chunks": [
         {
           "source": "CloudWatch Metrics",
           "text": "Lambda: send_message | Metric: Duration | Value: 47.98ms"
         }
       ],
       "confidence_score": "98%"
     }
     ```

2. **`POST /rag/reindex`**
   - Triggers re-chunking and re-embedding of PostgreSQL metrics into Vector Store.

---

## 🎯 Summary Checklist

- [x] Detailed Hinglish Guide created (`RAG_ARCHITECTURE_GUIDE_HINGLISH.md`).
- [ ] Implement `app/rag/chunker.py`
- [ ] Implement `app/rag/embedder.py`
- [ ] Implement `app/rag/vector_store.py`
- [ ] Implement `app/rag/generator.py`
- [ ] Implement `app/services/rag_service.py`
- [ ] Implement `app/api/rag.py` and register router in `main.py`
- [ ] Update frontend `ragApi.js` to point to `/rag/query`
