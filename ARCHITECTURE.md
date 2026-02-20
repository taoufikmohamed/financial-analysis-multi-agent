# System Architecture

## Overview

The Financial Analysis Multi-Agent System utilizes a modular architecture driven by the **Model Context Protocol (MCP)**. This design decouples domain-specific logic into independent servers, allowing for scalability and easy integration of new capabilities. The core orchestrator manages the workflow, leveraging the **DeepSeek API** for advanced reasoning and synthesis.

## components

### 1. Main Orchestrator (`main.py`)
-   **Role**: Central controller that manages the execution flow.
-   **Responsibilities**:
    -   Initializes MCP clients.
    -   Orchestrates the sequence of operations (workflow).
    -   Interacts with the DeepSeek API for high-level reasoning.
    -   Aggregates results and handles specialized tasks like risk assessment and quality control.

### 2. DeepSeek Agent
-   **Role**: Primary reasoning engine.
-   **Capabilities**:
    -   Natural Language Understanding of complex financial texts.
    -   Contextual reasoning for risk assessment.
    -   Synthesizing disparate data points into coherent summaries.
    -   Quality control checks on generated outputs.

### 3. MCP Server Ecosystem (`mcp_servers.py`)

Each MCP server encapsulates specific functionality and exposes tools via a standardized protocol.

#### A. Document Processor MCP (`port 8001`)
-   **Tools**: `extract_financial_data`, `health_check`
-   **Function**: Parses PDF/Image documents, extracts tables and text, and performs OCR if necessary. It returns structured JSON data representing financial statements.

#### B. Compliance Database MCP (`port 8002`)
-   **Tools**: `check_regulatory_compliance`
-   **Function**: Validates extracted financial data against regulatory frameworks (e.g., SEC, SOX, IFRS). It flags potential violations and issues warnings.

#### C. Market Data MCP (`port 8003`)
-   **Tools**: `get_market_context`
-   **Function**: Retrieves real-time market data, sector performance, competitor analysis, and macroeconomic indicators.

#### D. Reporting MCP (`port 8004`)
-   **Tools**: `generate_financial_report`, `list_reports`
-   **Function**: Formats analysis results into polished reports (HTML, TXT, JSON). Manages the storage and retrieval of report artifacts.

## Data Flow

1.  **Input**: User provides document paths and company information.
2.  **Extraction**: `Main` calls `Document Processor` to get raw financial data.
3.  **Analysis**: `Main` uses `DeepSeek Agent` to analyze trends and ratios from the extracted data.
4.  **Compliance**: `Main` sends data to `Compliance MCP` for regulatory checks.
5.  **Market Context**: `Main` queries `Market Data MCP` for external factors.
6.  **Risk Assessment**: `Main` aggregates all prior outputs and uses `DeepSeek Agent` to calculate a comprehensive risk score.
7.  **Quality Control**: `Main` performs a final review of all outputs.
8.  **Reporting**: `Main` sends the final dataset to `Reporting MCP` to generate the deliverable documents.

## Production Considerations

-   **Scalability**: MCP servers can be deployed on separate containers or machines.
-   **Security**: API keys are managed via environment variables. Communication between components can be secured with TLS.
-   **Monitoring**: Each component logs activities, allowing for centralized logging and monitoring (e.g., ELK stack).
-   **Extensibility**: New agents (e.g., "Legal Analysis MCP") can be added without modifying the core logic significantly.
