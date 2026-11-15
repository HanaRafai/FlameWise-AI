
import streamlit as st
import os
import sys

# Configure application
st.set_page_config(
    page_title="FlameWise AI",
    page_icon="🔥",
    layout="wide"
)

# Import backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flamewise_backend import (
    process_app_question,
    generate_app_data_answer,
    retrieve_app_documents,
    generate_app_answer,
    generate_app_combined_answer
)

# Application header
st.title("🔥 FlameWise AI")
st.subheader("NASA Microgravity Combustion Research Assistant")

st.write(
    "Explore NASA FLEX experimental data and scientific "
    "research through an AI-powered research assistant."
)

st.divider()

# Sidebar
with st.sidebar:
    st.title("🔥 FlameWise AI")
    st.write("NASA Combustion Research Assistant")

    st.divider()

    st.subheader("Research Capabilities")
    st.markdown("""
    - NASA document retrieval
    - Experimental data analysis
    - Combined research analysis
    - Flame extinction research
    - AI-powered question answering
    """)

    st.divider()

    st.subheader("Research Dataset")
    st.write("NASA FLEX Experiment")
    st.write("274 experimental records")
    st.caption("Research-support prototype")

# Analysis mode
analysis_mode = st.selectbox(
    "Select Analysis Method",
    [
        "Automatic Selection",
        "Dataset Analysis",
        "Document Retrieval",
        "Combined Analysis"
    ]
)

# Question input
user_question = st.text_area(
    "Ask FlameWise AI",
    placeholder="Example: Compare Methanol and Heptane flame extinction using both NASA data and research.",
    height=120
)

ask_button = st.button(
    "🔍 Ask FlameWise AI",
    type="primary"
)

# Process question
if ask_button:

    if user_question.strip():

        with st.spinner("FlameWise AI is analysing your question..."):

            try:

                if analysis_mode == "Automatic Selection":

                    result = process_app_question(user_question)

                elif analysis_mode == "Dataset Analysis":

                    result = {
                        "question": user_question,
                        "answer": generate_app_data_answer(user_question),
                        "answer_type": "Dataset Analysis",
                        "sources": [
                            {
                                "source": "NASA_FLEX_Analysis_Data.csv",
                                "page": "Dataset"
                            },
                            {
                                "source": "NASA_FLEX_Research_Findings.csv",
                                "page": "Research Findings"
                            }
                        ]
                    }

                elif analysis_mode == "Document Retrieval":

                    chunks = retrieve_app_documents(user_question)

                    result = {
                        "question": user_question,
                        "answer": generate_app_answer(
                            user_question, chunks
                        ),
                        "answer_type": "Document Retrieval",
                        "sources": [
                            {
                                "source": chunk["source"],
                                "page": chunk["page"]
                            }
                            for chunk in chunks
                        ]
                    }

                else:

                    answer, chunks = generate_app_combined_answer(
                        user_question
                    )

                    result = {
                        "question": user_question,
                        "answer": answer,
                        "answer_type": "Combined Analysis",
                        "sources": [
                            {
                                "source": "NASA_FLEX_Analysis_Data.csv",
                                "page": "Dataset"
                            },
                            {
                                "source": "NASA_FLEX_Research_Findings.csv",
                                "page": "Research Findings"
                            }
                        ] + [
                            {
                                "source": chunk["source"],
                                "page": chunk["page"]
                            }
                            for chunk in chunks
                        ]
                    }

                st.subheader("🤖 FlameWise AI Response")

                st.info(f"Answer Type: {result['answer_type']}")

                st.markdown(result["answer"])

                st.subheader("📚 Supporting Sources")

                for source in result["sources"]:
                    st.write(
                        f"- {source['source']} | {source['page']}"
                    )

            except Exception as error:
                st.error(f"Unable to process question: {error}")

    else:
        st.warning("Please enter a research question.")

# Disclaimer
st.divider()

st.caption(
    "FlameWise AI is an experimental research-support prototype. "
    "It does not certify spacecraft fire safety or replace "
    "professional engineering assessments."
)
