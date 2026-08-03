# 🧠 RAG Architecture Guide (Hinglish)

Yeh document current implemented RAG system ka real flow explain karta hai. Is project mein RAG backend ke andar kaam karta hai aur PostgreSQL se telemetry data lekar, usko chunks mein tod ke, embeddings banake, aur phir user query ke hisaab se relevant context retrieve karke answer generate karta hai.

---

## 1. RAG ka goal kya hai?

Agar user poochhe:
> "send_message Lambda ka duration kaisa hai?"

LLM direct answer de sakta hai, lekin woh sirf guess kar sakta hai. Isliye hum RAG use karte hain jisme hum:
1. Database se real telemetry data fetch karte hain
2. Us data ko chunks mein convert karte hain
3. Har chunk ko vector mein convert karte hain
4. User query ke liye sabse relevant chunks nikalte hain
5. In chunks ko prompt ke saath jod kar grounded answer dete hain

Isse hallucination kam hota hai aur answer real data par based hota hai.

---

## 2. Current implementation ka flow

### A. Request aata hai
User frontend ya API se query bhejta hai:
- POST /rag/query

Request body simple hota hai:
```json
{"query": "Which lambda function has high duration?"}
```

### B. Service layer ka kaam
[RAG service](backend/app/services/rag_service.py) request ko handle karta hai. Yeh:
- vector index ensure karta hai
- query ko search ke liye bhejta hai
- generator ko result bhejta hai

### C. Index build hota hai
Agar index abhi build nahi hua hai, to service DB se data nikal kar chunks banata hai aur vector store ko populate karta hai.

### D. Chunking
[TelemetryChunker](backend/app/rag/chunker.py) DB tables se data lekar readable text chunks banata hai. Example:
- Lambda configuration
- CloudWatch metric
- CloudWatch log event

### E. Embedding
[TextEmbedder](backend/app/rag/embedder.py) har chunk ka vector banata hai. Current implementation simple bag-of-words based hai.

### F. Vector search
[VectorStore](backend/app/rag/vector_store.py) in-memory index maintain karta hai aur cosine similarity se top-k results nikalta hai.

### G. Response generation
[RagGenerator](backend/app/rag/generator.py) retrieved chunks ko lekar answer build karta hai. Yeh abhi actual local LLM path bhi support karta hai via Ollama, aur agar model available nahi ho to fallback response deta hai.

---

## 3. Is session mein kya implement kiya gaya?

Is session mein yeh cheezein add ki gayi hain:
- Real RAG answer generation path via local Ollama model
- Default config for Ollama base URL aur model name
- Fallback logic jab Ollama unavailable ho
- Endpoint documentation aur local run steps
- Generator tests for LLM aur fallback behavior

### Current runtime behavior
- Agar Ollama available hai aur model pulled hai, to response LLM-se generate hota hai.
- Agar Ollama nahi chal raha ya model missing hai, to app heuristic fallback answer de deta hai.

---

## 4. File-wise responsibility

```text
backend/app/
├── rag/
│   ├── chunker.py      # DB rows ko readable chunks mein convert karta hai
│   ├── embedder.py     # Text ko vector mein convert karta hai
│   ├── vector_store.py # In-memory vector index + similarity search
│   └── generator.py    # Retrieved context se answer form karta hai
├── services/
│   └── rag_service.py  # RAG pipeline ka coordinator
├── api/
│   └── rag.py          # FastAPI endpoints /rag/query aur /rag/reindex
└── core/
    └── config.py       # Ollama settings aur app config
```

---

## 5. Data flow in simple form

```text
PostgreSQL DB
   ↓
TelemetryChunker
   ↓
Text chunks + metadata
   ↓
TextEmbedder
   ↓
Vector embeddings
   ↓
VectorStore (in-memory index)
   ↓
User query
   ↓
Similarity search
   ↓
RagGenerator
   ↓
Final answer + retrieved context
```

---

## 6. Kaise updates hote hain?

### Current behavior
- Database mein data update ho jaye to RAG index automatically refresh nahi hota.
- Index ek baar build ho jata hai aur service ke andar cached rehta hai.

### Jab index refresh karna ho
Aapko ye endpoint use karna hota hai:
- POST /rag/reindex

Isse service phir se:
1. DB se data read karta hai
2. Naye chunks banata hai
3. Vector store ko rebuild karta hai

### Practical rule
- Agar new telemetry data aa gaya hai to /rag/reindex call karo
- Agar server restart ho jaye to index phir se build hoga jab pehli query aayegi

---

## 7. Example flow

Example:
1. User query: "Which function has high duration?"
2. Query ko vector mein convert kiya jata hai
3. Vector store top-3 similar chunks nikalta hai
4. Generator un chunks ka use karke answer deta hai
5. Response me retrieved context bhi bheja jata hai

Example output:
```json
{
  "query": "Which function has high duration?",
  "answer": "Based on retrieved telemetry data, send_message shows important duration-related records.",
  "retrieved_context": [
    {
      "source": "CloudWatch Metrics (send_message)",
      "item": "CloudWatch Metric: Function='send_message'..."
    }
  ],
  "confidence_score": "95%"
}
```

---

## 8. Debugging tips

Agar RAG kaam nahi kar raha ho to ye check karo:
- Database connect ho rahi hai ya nahi
- ETL data imported hai ya nahi
- /rag/reindex call kiya gaya hai ya nahi
- Ollama server chal raha hai ya nahi
- Query me relevant function name ya metric term use ho raha hai ya nahi

---

## 9. Summary

Is project mein RAG ka working simple aur understandable structure mein hai:
- DB se telemetry data leke aana
- Chunks banana
- Vectors banana
- Similarity search karna
- Context-based answer banana
- Agar available ho to real local LLM se answer banana

Yeh flow future mein aur improve ho sakta hai, jaise:
- pgvector ya FAISS use karna
- better semantic embeddings
- auto-refresh index
- production-grade model integration
