# Financial Analysis Multi-Agent System (DeepSeek Edition)

A robust, enterprise-grade multi-agent system designed for automated financial document analysis, compliance checking, risk assessment, and report generation. This system leverages the **DeepSeek API** for advanced reasoning and **Model Context Protocol (MCP)** servers for modular, scalable architecture.

## 🚀 Key Features

-   **Multi-Agent Architecture**: Orchestrates specialized agents for document extraction, financial analysis, compliance checks, market context, and risk assessment.
-   **DeepSeek Integration**: Utilizes DeepSeek's powerful language models for deep financial insights and reasoning.
-   **MCP Server Ecosystem**: Modular servers handle specific domains (Document Processing, Compliance Database, Market Data, Reporting).
-   **Automated Workflow**: End-to-end processing from document ingestion to comprehensive report generation.
-   **Risk Assessment**: Calculates risk scores based on financial health, compliance status, and market conditions.
-   **Compliance Checks**: Verifies documents against major regulations (SEC, SOX, IFRS).
-   **Detailed Reporting**: Generates reports in HTML, TXT, and JSON formats.

## 🛠️ Prerequisites

-   **Python 3.8+**
-   **DeepSeek API Key**: You need a valid API key from [DeepSeek](https://platform.deepseek.com/).

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/financial-analysis-mcp.git
    cd financial-analysis-mcp
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    Create a `.env` file in the root directory and add your DeepSeek API key:
    ```env
    DEEPSEEK_API_KEY=your_deepseek_api_key_here
    ```

## ▶️ Usage

To start the system, simply run the main script:

```bash
python run.py
```

The system will:
1.  Verify your environment configuration.
2.  Start the local MCP servers.
3.  Execute the analysis workflow on sample financial documents.
4.  Generate reports in the `./generated_reports` directory.
5.  Wait for your command to shutdown (Ctrl+C).

## 📂 Project Structure

-   `main.py`: Core system logic and workflow orchestration.
-   `mcp_servers.py`: Implementation of the MCP servers (Document, Compliance, Market, Reporting).
-   `run.py`: Entry point for running the system.
-   `generated_reports/`: Directory where analysis reports are saved.
-   `data/`: Directory for input data (if applicable).
-   `logs/`: Application logs.

## 🤖 Agents & MCP Servers

The system uses the following specialized components:

1.  **Document Processor MCP**: Extracts structured data from financial documents (PDFs, etc.).
2.  **Financial Analyst Agent**: Performs ratio analysis, trend identification, and financial health assessment.
3.  **Compliance MCP**: Checks against regulatory databases (SEC, SOX).
4.  **Market Data MCP**: Retrieves real-time market context and competitor data.
5.  **Risk Assessor Agent**: Synthesizes all data to calculate risk scores.
6.  **Reporting MCP**: Compiles findings into professional reports.

## 📝 License

[MIT License](LICENSE)
