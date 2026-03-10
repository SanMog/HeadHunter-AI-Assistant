
---

### 🚀 Готовый README.md для HeadHunter-AI-Assistant

Скопируй этот код и замени текущий README в репозитории.

***

# 🤖 Agentic Pipeline: Automated Job Scoring & AI Generation

**Autonomous AI Agent for HeadHunter (API)** — is a multi-stage data pipeline designed to automate the process of parsing, scoring, and analyzing large volumes of unstructured job market data. It utilizes Google Gemini (LLM) to make complex semantic decisions based on custom engineering filters.

![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Data Pipeline](https://img.shields.io/badge/Architecture-Data%20Pipeline-blue?style=for-the-badge)
![License MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> *"Automating cognitive load: from unstructured HTML to AI-driven semantic decision making."*

---

## 🏛 Architecture: 4-Stage Autonomous Workflow

This project is structured as a robust **Data Engineering Pipeline**. Each script acts as a micro-service, handling a specific state of data transformation before passing it to the Large Language Model.

### 🔄 Stage 1: API Ingestion (`step1_get_urls.py`)
*   Connects to the official HeadHunter REST API.
*   Executes complex search queries based on hardcoded engineering filters (role, region, experience, schedule).
*   Outputs structured endpoints for deep-dive extraction.

### 🧹 Stage 2: Data Extraction & Sanitization (`step2_get_details.py`)
*   Performs secondary API calls to retrieve full JSON payloads for each endpoint.
*   Sanitizes the data by stripping raw HTML tags from the descriptions using `BeautifulSoup4`.
*   Outputs a clean, structured `vacancies_data.json` dataset.

### 🧠 Stage 3: Algorithmic Scoring (`step3_analyze.py`)
*   Acts as the **Deterministic Filter Engine** before invoking the LLM (saving token costs).
*   Applies a custom weighted scoring algorithm based on targeted technical stacks (e.g., Python, Selenium, API) and "Golden Keywords".
*   Applies penalty scores for irrelevant tech stacks (e.g., Java, C#) or misaligned roles.
*   Outputs `ranked_vacancies.json`, sorted by highest relevance probability.

### 🤖 Stage 4: LLM Semantic Analysis (`step4_generate_letters.py`)
*   The final stage acts as an **AI Agent**. It takes the top-N results from the ranked dataset and feeds them into **Google Gemini**.
*   **Prompt Engineering:** The LLM is provided with a strict system prompt containing the candidate's profile, "Red/Green flags" strategy, and the raw job description.
*   **Output:** The LLM acts as an evaluator, returning a binary verdict ("Fit" / "No Fit") and generating a highly personalized, context-aware cover letter in Markdown format.

---

## 🛠 Technical Stack

*   **Language:** Python 3.9+
*   **Data Extraction:** `requests`, `beautifulsoup4`
*   **LLM Integration:** `google-generativeai` (Gemini API)
*   **Data Serialization:** JSON, Markdown

---

## 🚀 Setup & Execution

### 1. Environment Initialization
```bash
git clone https://github.com/SanMog/HeadHunter-AI-Assistant.git
cd HeadHunter-AI-Assistant

python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
```

### 2. API Security
**Never hardcode API keys.** The system expects the Google Gemini API key to be passed securely via environment variables.
```powershell
# Windows PowerShell
$env:GOOGLE_API_KEY = "YOUR_GEMINI_API_KEY"

# Linux/macOS
export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

### 3. Pipeline Execution
Run the pipeline sequentially to process the data:
```bash
python step1_get_urls.py
python step2_get_details.py
python step3_analyze.py
python step4_generate_letters.py
```

---

## ⚙️ Customization (Configuring the "Brain")

The scoring engine is highly decoupled and can be tuned for any engineering role:
*   **Weights & Penalties:** Edit `SKILLS_KEYWORDS`, `GOLDEN_KEYWORDS`, and `PENALTY_KEYWORDS` in `step3_analyze.py` to adjust the deterministic scoring algorithm.
*   **LLM Persona:** Modify the `PROMPT_TEMPLATE` in `step4_generate_letters.py` to dictate the AI's analytical behavior and writing style.

---

**Architect:** SanMog 
**Domain:** AI Automation / Agentic Workflows  
**License:** MIT  

***
