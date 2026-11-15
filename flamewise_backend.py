
# 12.26 Create the FlameWise AI Backend File

import os
import json
import faiss
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from google import genai

# Load application resources
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

faiss_index = faiss.read_index(
    os.path.join(BASE_DIR, "knowledge_base", "faiss_index.bin")
)

with open(
    os.path.join(BASE_DIR, "knowledge_base", "chunks.json"),
    "r",
    encoding="utf-8"
) as file:
    knowledge_chunks = json.load(file)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

app_df = pd.read_csv(
    os.path.join(BASE_DIR, "data", "NASA_FLEX_Analysis_Data.csv")
)

app_findings = pd.read_csv(
    os.path.join(BASE_DIR, "data", "NASA_FLEX_Research_Findings.csv")
)

# Initialize Gemini
app_client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

# Retrieve NASA research passages
def retrieve_app_documents(question, top_k=5):

    question_embedding = embedding_model.encode([question])

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    distances, indices = faiss_index.search(
        question_embedding,
        top_k
    )

    return [
        knowledge_chunks[index]
        for index in indices[0]
        if index != -1
    ]

# Generate research document answers
def generate_app_answer(question, retrieved_chunks):

    context = "\n\n".join(
        f"Source: {chunk['source']}\n"
        f"Page: {chunk['page']}\n"
        f"Content: {chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are FlameWise AI, a NASA combustion research assistant.

Answer using only the supplied NASA research passages.

- Use clear and scientifically cautious language.
- Do not invent facts.
- Include supporting source filenames and page numbers.
- State clearly if the evidence is insufficient.

Research passages:
{context}

Question:
{question}
"""

    response = app_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

# Analyze NASA FLEX experimental data
def analyze_app_dataset():

    outcome_by_fuel = pd.crosstab(
        app_df["Fuel"],
        app_df["Test end"]
    )

    extinction_percentages = (
        outcome_by_fuel["Extinction"] /
        outcome_by_fuel.sum(axis=1) * 100
    ).round(2).to_dict()

    return {
        "total_experiments": len(app_df),
        "fuel_distribution": app_df["Fuel"].value_counts().to_dict(),
        "experimental_outcomes": app_df["Test end"].value_counts().to_dict(),
        "outcomes_by_fuel": outcome_by_fuel.to_dict(),
        "extinction_percentage_by_fuel": extinction_percentages,
        "mean_pressure": round(
            app_df["Ambient pressure; mmHg"].mean(), 2
        ),
        "mean_oxygen_composition": round(
            app_df["O initial ambient composition; mole fraction"].mean(), 3
        ),
        "mean_burning_rate": round(
            app_df["Burning rate; mm"].mean(), 3
        ),
        "mean_burn_time": round(
            app_df["Burn time; s - Numeric"].mean(), 3
        )
    }

# Generate dataset analysis answers
def generate_app_data_answer(question):

    data_summary = analyze_app_dataset()

    prompt = f"""
You are FlameWise AI, a NASA combustion research assistant.

Answer using only the supplied NASA FLEX dataset summary.

- Use numerical values accurately.
- Do not invent scientific information.
- Do not claim correlation or causation without evidence.
- State if the available data is insufficient.

Dataset summary:
{json.dumps(data_summary, indent=2)}

Question:
{question}
"""

    response = app_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

# Process user questions
def process_app_question(question):

    data_keywords = [
        "dataset", "data", "percentage", "average", "mean",
        "count", "how many", "which fuel", "correlation",
        "statistics", "experiments", "burning rate"
    ]

    is_data_question = any(
        keyword in question.lower()
        for keyword in data_keywords
    )

    if is_data_question:

        answer = generate_app_data_answer(question)

        sources = [
            {"source": "NASA_FLEX_Analysis_Data.csv", "page": "Dataset"},
            {"source": "NASA_FLEX_Research_Findings.csv", "page": "Research Findings"}
        ]

        answer_type = "Dataset Analysis"

    else:

        retrieved_chunks = retrieve_app_documents(question)

        answer = generate_app_answer(question, retrieved_chunks)

        sources = [
            {"source": chunk["source"], "page": chunk["page"]}
            for chunk in retrieved_chunks
        ]

        answer_type = "Research Document"

    return {
        "question": question,
        "answer": answer,
        "answer_type": answer_type,
        "sources": sources
    }

print("FlameWise AI backend module created successfully!")

# 12.43 Combined Analysis

def generate_app_combined_answer(question):

    retrieved_chunks = retrieve_app_documents(question)
    data_summary = analyze_app_dataset()

    context = "\n\n".join(
        f"Source: {chunk['source']}\n"
        f"Page: {chunk['page']}\n"
        f"Content: {chunk['text']}"
        for chunk in retrieved_chunks
    )

    prompt = f"""
You are FlameWise AI, a NASA combustion research assistant.

Answer the question using BOTH the supplied NASA FLEX dataset
summary and NASA research passages.

Instructions:
- Use dataset values accurately.
- Use research passages to provide scientific context.
- Clearly distinguish experimental results from research explanations.
- Do not invent facts or unsupported causal relationships.
- Include relevant PDF filenames and page numbers.
- State clearly when either source lacks sufficient evidence.
- Present a clear, integrated answer.

NASA FLEX dataset summary:
{json.dumps(data_summary, indent=2)}

NASA research passages:
{context}

Question:
{question}
"""

    response = app_client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text, retrieved_chunks


# 12.44 Updated Question Router

def process_app_question(question):

    question_lower = question.lower()

    combined_keywords = [
        "both sources",
        "both the dataset and",
        "dataset and research",
        "compare the dataset",
        "compare experimental results",
        "according to the data and",
        "combined analysis",
        "together with nasa research"
    ]

    data_keywords = [
        "dataset", "data", "percentage", "average", "mean",
        "count", "how many", "which fuel", "correlation",
        "statistics", "experiments", "burning rate"
    ]

    is_combined_question = any(
        keyword in question_lower
        for keyword in combined_keywords
    )

    is_data_question = any(
        keyword in question_lower
        for keyword in data_keywords
    )

    if is_combined_question:

        answer, retrieved_chunks = generate_app_combined_answer(question)

        sources = [
            {
                "source": "NASA_FLEX_Analysis_Data.csv",
                "page": "Dataset"
            },
            {
                "source": "NASA_FLEX_Research_Findings.csv",
                "page": "Research Findings"
            }
        ]

        sources.extend([
            {
                "source": chunk["source"],
                "page": chunk["page"]
            }
            for chunk in retrieved_chunks
        ])

        answer_type = "Combined Analysis"

    elif is_data_question:

        answer = generate_app_data_answer(question)

        sources = [
            {"source": "NASA_FLEX_Analysis_Data.csv", "page": "Dataset"},
            {"source": "NASA_FLEX_Research_Findings.csv", "page": "Research Findings"}
        ]

        answer_type = "Dataset Analysis"

    else:

        retrieved_chunks = retrieve_app_documents(question)

        answer = generate_app_answer(question, retrieved_chunks)

        sources = [
            {"source": chunk["source"], "page": chunk["page"]}
            for chunk in retrieved_chunks
        ]

        answer_type = "Research Document"

    unique_sources = []
    seen_sources = set()

    for source in sources:
        source_key = (source["source"], source["page"])

        if source_key not in seen_sources:
            unique_sources.append(source)
            seen_sources.add(source_key)

    return {
        "question": question,
        "answer": answer,
        "answer_type": answer_type,
        "sources": unique_sources
    }

print("Combined Analysis backend added successfully!")
