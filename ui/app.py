import streamlit as st
import requests

API = "http://127.0.0.1:8000/api/ask"
METRICS = "http://127.0.0.1:8000/api/metrics"

st.title("RAG Chatbot with Caching")

question = st.text_input("Ask a question")

if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            r = requests.post(API, json={"question": question})
            data = r.json()

            st.write("### Answer")

            if "answer" in data:
                st.write(data["answer"])

                if data.get("cache_used"):
                    st.success("Cache Hit ⚡")
                else:
                    st.warning("Cache Miss")

                st.write("Response time:", data.get("response_time", 0), "ms")

            else:
                st.error("Backend returned an error")
                st.write(data)

        except Exception as e:
            st.error("Failed to connect to backend")
            st.write(str(e))


if st.button("Show Metrics"):

    try:
        m = requests.get(METRICS).json()

        st.write("### System Metrics")

        st.write("Total Queries:", m.get("total_queries", 0))
        st.write("Cache Hit Rate:", f"{m.get('cache_hit_rate',0):.2f}%")
        st.write("Average Response Time:", m.get("avg_response_time", 0), "ms")

    except Exception as e:
        st.error("Could not fetch metrics")
        st.write(str(e))