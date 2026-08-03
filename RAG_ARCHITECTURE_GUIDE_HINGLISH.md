# 🧠 RAG Architecture Guide (Hinglish)

Yeh document current implemented RAG system ka real flow explain karta hai. Is project mein RAG ka kaam sirf backend mein ho raha hai aur ye PostgreSQL se telemetry data leke, usko chunks mein tod ke, embeddings banake, aur phir user query ke hisaab se relevant context retrieve karke answer generate karta hai.

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
[TextEmbedder](backend/app/rag/embedder.py) har chunk ka vector banata hai. Current implementation simple bag-of-words based hai, matlab words ko count karke normalized vector banaya jata hai.

### F. Vector search
[VectorStore](backend/app/rag/vector_store.py) in-memory index maintain karta hai aur cosine similarity se top-k results nikalta hai.

### G. Response generation
[RagGenerator](backend/app/rag/generator.py) retrieved chunks ko lekar answer build karta hai. Yeh actual LLM API call nahi karta, balki context-based structured answer return karta hai.

---

## 3. File-wise responsibility

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
└── schemas/
    └── rag.py          # Request/response models
```

---

## 4. Data flow in simple form

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

## 5. Kaise updates hote hain?

Yeh important point hai:

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

## 6. Current implementation ki limitations

Yeh implementation lightweight aur demo-friendly hai. Isme kuch cheezein simple tarike se ki gayi hain:
- Embedding simple word-based vectorization hai, actual transformer embeddings nahi
- Vector store in-memory hai, database/jar file mein persistent nahi hai
- Response generator simple rule-based hai, actual LLM integration ke bina

Iska matlab hai ke yeh project ka RAG foundation hai, production-grade semantic search nahi.

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
- Query me relevant function name ya metric term use ho raha hai ya nahi

---

## 9. Summary

Is project mein RAG ka working simple aur understandable structure mein hai:
- DB se telemetry data leke aana
- Chunks banana
- Vectors banana
- Similarity search karna
- Context-based answer banana

Yeh flow future mein bada sakta hai, jaise:
- pgvector ya FAISS use karna
- real LLM API integration
- auto-refresh index
- better semantic embeddings

---

## 10. Important note for developers

Agar koi naya developer is project mein aaye to uske liye yaad rakhna:
- RAG ka data source PostgreSQL database hai
- Index memory mein cached hai
- Data update ke baad reindex zaroori hai
- Current implementation lightweight hai, lekin flow sahi hai
