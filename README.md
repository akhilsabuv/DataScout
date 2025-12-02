# DataScout - Enterprise SQL Intelligence

DataScout is a powerful web-based application designed to simplify database management and schema exploration. It provides a unified interface to connect to various SQL databases (SQLite, MySQL, PostgreSQL, MSSQL), visualize their schemas, and interact with an intelligent AI agent for natural language queries (Text-to-SQL).

**The Problem**
In every enterprise, valuable data is locked inside SQL databases. Business stakeholders (Marketing, HR, Sales) constantly need answers from this data, but they don't know SQL. They rely on data analysts for every small request, creating a massive bottleneck.

Existing "Text-to-SQL" AI solutions often fail in enterprise environments for two reasons:

Security Risks: Giving an LLM unfettered access to a database is dangerous.

Privacy Concerns: Uploading actual customer rows to an LLM context window violates privacy compliance (GDPR/SOC2).

The Solution: DataScout (Change name to your title)
I built a Privacy-First Enterprise Agent that acts as a secure bridge between business users and their databases.

Unlike standard agents that blindly ingest data, my solution uses a "Schema-Handshake" architecture:

Human-in-the-Loop: The user connects a database and explicitly selects only the relevant tables via the Angular frontend.

Metadata Only: The Agent receives the table schema (column names/types) but NEVER the actual data rows during the reasoning phase.

Secure Execution: The Agent generates the SQL, which is executed by a sandboxed Python backend with strict "Read-Only" enforcement (blocking DROP/DELETE/UPDATE).

Visual Results: The data is returned to the frontend, where Angular dynamically renders tables and charts, keeping the raw data out of the LLM's final response text where possible.

Architecture & Tech Stack
This is a full-stack application designed for real-world deployment, not just a notebook script.

Frontend: Angular. chosen for its robust state management. It handles the database connection UI, table selection (the "Gatekeeper" feature), and visualizes the JSON responses.

Backend: Python (FastAPI). Acts as the orchestration layer. It manages the database connections using SQLAlchemy.

The Agent: Powered by Google Gemini (via google-genai SDK). I utilized Gemini's advanced reasoning capabilities to understand complex table relationships (e.g., joins between Sales and Regions) based solely on column names.

Tooling: The system uses a custom "Safe SQL Tool" that parses queries before execution to ensure read-only compliance.

Key Features
Universal Connector: Works with SQLite (demoed), PostgreSQL, and MySQL.

Safety Guardrails: A custom logic layer that rejects destructive SQL commands before they hit the database.

Context Optimization: By feeding Gemini only the schema (and not the data), I significantly reduce token usage and latency while maintaining 100% data privacy.

Dynamic Visualization: The agent doesn't just talk; it returns structured data that the UI renders into interactive tables.

> **Note**: This project is currently under active development. Some features, such as the full AI agent integration, are in the prototype stage.

## Key Features

-   **Multi-Database Support**: Seamlessly connect to SQLite, MySQL, PostgreSQL, and Microsoft SQL Server.
-   **Interactive Schema Viewer**: Visualize database tables, columns, and relationships in a clean, modern interface.
-   **Context Management**: Add descriptions and context to tables and columns to enhance the AI's understanding of your data.
-   **Robust Error Handling**: Clear and visible error reporting via high-contrast modals.
-   **Secure AI Integration**: Confirmation prompts before initiating secure sessions with the AI agent.

## Technology Stack

-   **Frontend**: Angular 18, TailwindCSS (via CDN/custom styles), RxJS
-   **Backend**: Python, FastAPI, SQLAlchemy
-   **Database**: SQLite (internal metadata), plus support for external SQL databases
-   **Containerization**: Docker & Docker Compose

## Getting Started

### Prerequisites
-   Node.js (v18+)
-   Python (v3.10+)
-   Docker (optional, for running test databases)

### Backend Setup
1.  Navigate to the root directory.
2.  Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    uvicorn backend.main:app --reload
    ```

### Frontend Setup
1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm start
    ```
4.  Open your browser at `http://localhost:4200`.

## Project Structure

-   `backend/`: FastAPI application and database models.
-   `frontend/`: Angular application source code.
-   `scripts/`: Utility scripts for database management and testing.
-   `mysql&phpmyadmin/`: Docker Compose setup for local MySQL testing.

---
*Generated by DataScout AI Assistant*
