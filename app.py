import streamlit as st
import pandas as pd

from cleaner import (
    clean_data,
    calculate_profit
)

from analyst import (
    analyze_question
)

st.set_page_config(
    page_title="Insight Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Insight Agent")
st.caption("Ask Questions. Get Insights.")

# Session state
if "df" not in st.session_state:
    st.session_state.df = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Upload CSV

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(
        uploaded_file
    )

    df = clean_data(df)

    df = calculate_profit(df)

    df = df.fillna(0)

    st.session_state.df = df

    st.success(
        f"CSV Loaded: {len(df)} rows"
    )

    st.dataframe(
        df.head()
    )

# Chat Interface

if st.session_state.df is not None:

    st.divider()

    st.subheader(
        "Ask Questions"
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    question = st.chat_input(
        "Ask about your CSV..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):
            st.write(question)

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Analyzing..."
            ):

                answer = analyze_question(
                    st.session_state.df,
                    question
                )

                st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )