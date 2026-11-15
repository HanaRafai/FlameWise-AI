# FlameWise AI

**AI-powered research assistant for NASA microgravity combustion research.**

FlameWise AI helps researchers and learners explore NASA's Flame
Extinguishment Experiment (FLEX) through experimental dataset analysis
and scientific document retrieval.

## Features

- Dataset Analysis: explore NASA FLEX experimental records.
- Document Retrieval: retrieve relevant passages from NASA research.
- Combined Analysis: connect experimental data with research documents.
- Automatic Selection: select an appropriate answering approach.
- Evidence-grounded responses with source references.

## Technology Stack

- Python
- Streamlit
- Google Gemini API
- LangGraph
- FAISS
- Sentence Transformers
- Pandas and NumPy

## Project Structure

```text
FlameWise-AI/
├── app.py
├── flamewise_backend.py
├── requirements.txt
├── data/
│   ├── NASA_FLEX_Analysis_Data.csv
│   └── NASA_FLEX_Research_Findings.csv
└── knowledge_base/
    ├── faiss_index.bin
    └── chunks.json
```

## Installation

1. Clone the repository:

   git clone https://github.com/HanaRafai/FlameWise-AI.git

2. Enter the project directory:

   cd FlameWise-AI

3. Install dependencies:

   pip install -r requirements.txt

4. Set your Gemini API key.

   Linux / Google Colab:
   export GEMINI_API_KEY="YOUR_API_KEY"

   Windows PowerShell:
   $env:GEMINI_API_KEY="YOUR_API_KEY"

5. Run the application:

   streamlit run app.py

Never commit your API key or `.env` files.

## Data and Research

The prototype analyzes 274 supplied NASA FLEX experimental records
and uses a knowledge base containing 614 text chunks from two NASA
research documents.

NASA FLEX research:
https://ntrs.nasa.gov/citations/20150023456

Observed dataset results:
- Methanol: 126/157 extinction outcomes (80.25%).
- Heptane: 60/117 extinction outcomes (51.28%).
- Overall: 186/274 extinction outcomes (67.88%).

These are descriptive results from the supplied dataset, not claims
of causal physical behaviour.

## Limitations

FlameWise AI is an experimental research-support prototype.
Its answers depend on the supplied data and documents and should be
independently verified. It is not a certified spacecraft fire-safety
system or a substitute for expert scientific judgement.

## Team

Team Flame AI

NASA Space Apps Challenge
Challenge 08 – Flame in Freefall
