import streamlit as st

st.title("Literature Survey Tool - View Reviews")
if "paper_reviews" not in st.session_state:
    st.write("Please generate paper reviews first.")
else:
    st.selectbox(
        "Select Paper",
        st.session_state["paper_reviews"].keys(),
        key="paper_review_select",
    )
    if "paper_review_select" in st.session_state:
        review = st.session_state["paper_reviews"][st.session_state["paper_review_select"]]
        st.title(review["Title"])
        with st.container():
            for author in review["Authors"]:
                st.markdown("- " + author)
        with st.container():
            st.markdown(f"DOI: {review['DOI']}")
        with st.container():
            st.markdown(f"Problem: {review['Summary']['Problem']}")
        with st.container():
            st.markdown(f"Solution: {review['Summary']['Solution']}")
        with st.container():
            st.markdown(f"Datasets: {review['Summary']['Datasets']}")
        with st.container():
            st.markdown(f"Frameworks: {review['Summary']['Frameworks']}")
        with st.container():
            st.markdown(f"Models: {review['Summary']['Models']}")
        with st.container():
            st.markdown(f"Results: {review['Summary']['Results']}")
        with st.container():
            st.markdown(f"Impact: {review['Summary']['Impact']}")
        with st.container():
            st.markdown(f"Limitations: {review['Summary']['Limitations']}")
        with st.container():
            st.markdown(f"Future Work: {review['Summary']['Future Work']}")
        with st.container():
            st.markdown(f"Conclusion: {review['Summary']['Conclusion']}")

        

