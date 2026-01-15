# Fund Analytics RAG Chatbot

## Overview

This project implements a **production-grade Retrieval-Augmented Generation (RAG) chatbot** designed to answer analytical questions strictly based on structured financial data. The chatbot is trained exclusively on two datasets — `holdings.csv` and `trades.csv` — and is intentionally constrained to **only generate answers that can be derived from these files**.

If a question cannot be answered using the provided data, the system responds deterministically with:

> **“Sorry can not find the answer”**

This design ensures **accuracy, auditability, and zero hallucination**, making the solution suitable for controlled and data-sensitive environments.

---

## Key Capabilities

- Fund-level analytics (holdings count, trade count)
- Aggregated performance metrics (e.g. Year-to-Date P&L)
- Comparative analysis across funds
- Natural-language question answering via a local LLM
- Deterministic refusal for unsupported or out-of-scope queries
- Web-based chat UI and REST API
- Fully local deployment (no external APIs, no internet dependency)

---

## Architecture Summary

The system follows a **layered, industry-standard RAG architecture**:

1. **Data Layer**
   - Loads and validates CSV files at startup
   - Enforces strict schema validation
   - Acts as the single source of truth

2. **Retrieval Layer**
   - Performs deterministic operations (counting, aggregation, comparison)
   - Contains no AI logic
   - Fully testable and reproducible

3. **Context Augmentation Layer**
   - Converts retrieval results into structured, minimal context
   - Explicitly handles empty or invalid results

4. **Generation Layer**
   - Uses a local Large Language Model (LLM) for:
     - Intent understanding
     - Natural-language response generation
   - The LLM never accesses raw data or external knowledge

5. **Application Layer**
   - FastAPI-based backend exposed on localhost
   - Lightweight browser-based chat UI

This separation ensures **scalability, maintainability, and correctness**, and aligns with real-world enterprise RAG implementations.

---

## Technology Stack

- **Python 3.10+**
- **FastAPI** – API orchestration
- **Pandas** – deterministic data processing
- **Ollama (local LLM)** – offline language model execution
- **HTML / CSS / JavaScript** – chat UI
- **Git** – version control

All components are **free, open, and locally deployable**.

## Future Enhancements

- **Dockerised Deployment**  
  Package the application using Docker to ensure consistent environments across development, testing, and production, and to simplify deployment in cloud or on-premise infrastructure.

- **Authentication and Access Control**  
  Introduce role-based access control (RBAC) and authentication mechanisms to restrict data access and secure the chatbot in multi-user or enterprise environments.

- **Streaming LLM Responses**  
  Enable token-by-token streaming of responses to improve perceived latency and provide a more interactive chat experience.

- **Support for Additional Financial Metrics**  
  Extend the retrieval and aggregation layer to support additional metrics such as MTD/QTD performance, exposure analysis, and risk-related indicators.

- **Integration with SQL or Data Warehouses**  
  Replace or augment CSV-based data sources with SQL databases or data warehouses (e.g. PostgreSQL, Snowflake, BigQuery) for larger-scale and real-time datasets.

- **Frontend Framework Integration (React / Vue)**  
  Replace the lightweight HTML/JavaScript UI with a modern frontend framework to support richer user interactions, state management, and enterprise-grade UX.

---

## License

This project is provided for educational and demonstration purposes and can be adapted for commercial use with appropriate data governance, security, and compliance controls.

---

## Author Notes

This project demonstrates a **disciplined RAG implementation**, prioritising correctness, traceability, and production readiness over experimental shortcuts.

It intentionally reflects architectural and engineering patterns used in real-world AI systems rather than toy or proof-of-concept examples.




