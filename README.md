# World War 1 Rag Agent

A retrieval-augmented research assistant that answers **World War I** questions using a document collection
The app is built with a **RAG pipeline** so answers are based in articles and media from duck.db database.

---
## Domain Overview & Problem Statement

### Domain
World War I which is an extremely important confilict in world history:
- I has dense historical context (alliances, diplomacy, military doctrine, social factors, economic factors),
- conflicting interpretations (war guilt, inevitability, responsibility),
- frequent student-facing needs (timelines, key actors, primary-source grounding, templates, introductions).

### Problem Statement
Students and researchers often get:
- **surface-level summaries** without evidence,
- **uncited claims**,
- no visibility into **source disagreement**.

My project solves that by:
1) retrieving relevant passages from a well reaserched library,  
2) generating answers to prompts with **citations** ,  
3) explicitly noting **uncertainty and conflicting perspectives** when they exist.

---

## Architecture / Pipeline

1. **User question** enters the Streamlit UI  
2. Pipeline **retrieves** relevant chunks from the WWI corpus  
3. An **agent** synthesizes a response grounded in retrieved text  
4. UI shows the final answer + citations + sources

