import streamlit as st
from summarizer import summarize_meeting

st.set_page_config(page_title="Meeting Summarizer", page_icon="🎙️")
st.title("🎙️ AI Meeting Summarizer")
st.caption("Paste a transcript → get structured notes instantly")

transcript = st.text_area(
    "Meeting transcript",
    height=250,
    placeholder="Paste your meeting transcript here..."
)

if st.button("Summarize", type="primary"):
    if not transcript.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("Analysing meeting..."):
            result = summarize_meeting(transcript)

        st.subheader("📋 Summary")
        st.write(result["summary"])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Key Decisions")
            for d in result["key_decisions"]:
                st.markdown(f"- {d}")

        with col2:
            st.subheader("💬 Sentiment")
            emoji = {"positive":"😊","neutral":"😐","negative":"😟"}
            st.markdown(f"### {emoji.get(result['sentiment'],'')} {result['sentiment'].title()}")

        st.subheader("📌 Action Items")
        for item in result["action_items"]:
            deadline = f" — due **{item['deadline']}**" if item["deadline"] else ""
            st.markdown(f"- **{item['owner']}**: {item['task']}{deadline}")

        if result["follow_up_questions"]:
            st.subheader("❓ Open Questions")
            for q in result["follow_up_questions"]:
                st.markdown(f"- {q}")

        st.download_button(
            "⬇️ Download JSON",
            data=str(result),
            file_name="meeting_notes.json"
        )