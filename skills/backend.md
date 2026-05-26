# Backend Engineering & Technical Skills

This document details the backend engineering skills, environment configuration, and database connection logic implemented for the conversational business intelligence engine.

## Core Stack & Environment
- **Language & Runtime:** Python 3.x.
- **Web API Framework:** FastAPI / Uvicorn (High-performance, asynchronous ASGI web routing).
- **Data Manipulation:** Pandas (DataFrame structures for cleaning and structuring SQL result sets).
- **Database Interfacing:** Snowflake Connector for Python (`snowflake.connector`).
- **Environment Management:** `python-dotenv` for secure decoupled runtime variable injection.

## Implemented Engineering Capabilities

### 1. Asynchronous API Design & Middleware
- Built modular endpoint configurations parsing JSON payloads under strict structural rules.
- Designed seamless connection pipelines exposing relational tables via standard routing methods (`/api/query`).

### 2. Secure Snowflake Data Warehousing Integration
- Structured scalable, secure connection handlers using local system environment variables (`os.environ.get`) to isolate sensitive passwords and access tokens.
- Provisioned functional data extraction logic connecting unique user profiles, virtual compute warehouses (`COMPUTE_WH`), databases (`NLP2SQL`), and schema namespaces (`TEST_SCHEMA`).
- Implemented structured cursor processing engines using `cur.fetchall()` and `cur.description` mappings to safely transform low-level database tuples into labeled datasets.

### 3. Relational Schema Data Modeling
- Maintained a production-ready schema semantic mapping system utilizing multi-table configurations across structured attributes:
  - Built comprehensive relational links across dimensional primary keys (`MATCH_ID`) and unique foreign indexes (`PLAYER_ID`).
  - Integrated detailed column descriptions, sample data values, and precise variable mapping keys to create structured lookup systems.