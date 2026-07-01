\# 🚀 Global Trade Data Automation Pipeline



An automated, AI-powered data engineering pipeline designed to ingest messy, multilingual global trade data and standardize it into a strict 13-column "Golden Schema" for high-level PowerBI dashboarding.



\## 🧠 Architecture \& Tech Stack

\* \*\*Orchestration:\*\* \[n8n](https://n8n.io/) (Local Automation)

\* \*\*Data Processing Engine:\*\* \[KNIME Analytics Platform](https://www.knime.com/)

\* \*\*AI \& LLM Integration:\*\* Python, OpenRouter API (Claude-3)

\* \*\*Data Manipulation:\*\* Pandas, Regex, Fuzzy Matching



\## ⚠️ Disclaimer

\*This repository serves as a portfolio piece showcasing the pipeline architecture and code. \*\*No proprietary company data, real Excel files, or active API keys are included in this repository.\*\* All execution directories and live databases are strictly maintained locally.\*



\## 💡 The Problem vs. The Solution

\*\*The Problem:\*\* Global trade reports arrive with unpredictable, heavily nested, and multilingual column headers (e.g., 50+ columns of garbage data). Manually mapping these to a standard format for executive PowerBI dashboards (focusing on CIF Total Price and Competitor Data) is a massive time sink.



\*\*The Solution:\*\*

1\. \*\*n8n Orchestration:\*\* A trigger automatically detects new files and executes a local batch script (`run\_knime.bat`) in the background (headless mode).

2\. \*\*KNIME Processing:\*\* The workflow ingests the raw `.xlsx` files and extracts the chaotic column headers.

3\. \*\*AI Translation (Python/Claude-3):\*\* A Python script sends the headers to an LLM via OpenRouter, utilizing prompt engineering and fuzzy matching to dynamically map the chaotic headers to the 13-column Golden Standard.

4\. \*\*Data Cleansing:\*\* Irrelevant columns are stripped, and the final structured dataset is outputted for PowerBI ingestion.



\## 🛠️ Local Installation \& Handover Setup

To run this pipeline locally for execution:

1\. Clone this repository to your local machine.

2\. Ensure you have \*\*KNIME\*\* and \*\*n8n\*\* installed.

3\. Copy the `/local\_execution` folder (provided separately via internal ZIP) directly to your `C:\\` drive.

4\. Import the `Master\_Mapping\_Engine.knwf` into your KNIME workspace.

5\. Import the `trigger\_pipeline.json` into n8n.

6\. Update the OpenRouter API key in the Python node and execute!

