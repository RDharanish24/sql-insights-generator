# AI Core & LLM Engineering Skills

This document details the Artificial Intelligence implementation, semantic prompting strategies, and Large Language Model (LLM) workflows driving the Natural Language to SQL execution pipeline.

## Core Stack & Tools
- **LLM Engine:** Google GenAI Client Platform.
- **Model Target:** `gemini-2.5-flash` (Optimized for low-latency reasoning and precise structure output).
- **Semantic Mapping Configuration:** Custom YAML parsing via `pyyaml`.

## Implemented Engineering Capabilities

### 1. Advanced Prompt Engineering & Few-Shot Instruction Design
- Engineered a deterministic system prompt framework (`SCHEMA_PROMPT`) that injects complete, serializable database definitions directly into the model's inference window using structured markdown blocks.
- Implemented strict behavioral rules ensuring output predictability:
  - Eradication of formatting artifacts (forcing clean, pure code returns without markdown enclosing blocks like ` ```sql `).
  - Explicit instruction enforcement avoiding conversational filler text, remarks, or descriptive preamble summaries.
  - Strict compliance rules mapping queries against exact database column structures.

### 2. Real-Time Semantic Context Injection
- Utilized automated system instructions to steer model behavior on complex sports domain logic rules:
  - Defined explicit context categorization rules (e.g., distinguishing a tournament "cup winner" from the team with the most total match wins).
  - Configured structural routing logic, instructing the model to rely on precise granular records (`BALL_BY_BALL`) for deep match commentary over static summaries.

### 3. Raw Response Normalization & Pipeline Cleaning
- Implemented robust regex-based text processing chains (`re.sub`) inside the application layer to intercept, sanitize, and validate incoming AI strings before handing them down to data connectors.
- Configured temperature thresholds (`temperature=0.4`) within generation configs to optimize output consistency, balancing syntactic accuracy with structural problem-solving.