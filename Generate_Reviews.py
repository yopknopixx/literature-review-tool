import streamlit as st
from streamlit_wizard import components
import streamlit_scrollable_textbox as stx
from generation import *
from prompts import *
import json
from metaphor_python import Metaphor
from utils import *


openai.api_key = ""
metaphor = Metaphor("")


st.title("Literature Survey Tool")


class GetAndSummarizeRawContent(components.Page):
    def render(self) -> dict:
        st.title("Lets get started!")
        st.write(
            "Please upload any raw content you have for the paper in the form of a .txt file."
        )

        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # read text file
            bytes_data = uploaded_file.getvalue()
            with st.container():
                stx.scrollableTextbox(bytes_data.decode("utf-8"), height=300)
            return {"raw_content": bytes_data.decode("utf-8")}
        else:
            return {}


class GetPaperSummary(components.Page):
    def render(self) -> dict:
        st.header("Paper Summary")
        if "raw_content" in st.session_state["page_state"]["intro"]:
            raw_content = st.session_state["page_state"]["intro"]["raw_content"]
            gen = Generator(model="gpt-4", prompt=summarize_raw_content)
            summary = json.loads(gen.generate(raw_content))
            # write the elements of the dictionary
            with st.container():
                st.write("Aim: ", summary["aim"])
            with st.container():
                st.write("Method: ", summary["method"])
            with st.container():
                st.write("Ideas: ")
                for idea in summary["ideas"]:
                    st.markdown("- " + idea)
            with st.container():
                st.write("Context Required: ")
                for context in summary["context_required"]:
                    st.markdown("- " + context)

            context = get_context(summary["context_required"])
            gen = Generator(model="gpt-4", prompt=summarize_context)
            context_summary = gen.generate(
                "\n".join(
                    [context.contents[i].extract for i in range(len(context.contents))]
                )
            )

            return {"summary": summary, "context_summary": context_summary}
        else:
            st.write("Please upload a file first.")
            return {}


class DownloadPapers(components.Page):
    def render(self) -> dict:
        st.header("Download Papers")
        if "summary" in st.session_state["page_state"]["summary"]:
            st.write("The tool will now download the papers for you. Sit tight!")
            summary = st.session_state["page_state"]["summary"]["summary"]
            context_summary = st.session_state["page_state"]["summary"][
                "context_summary"
            ]
            gen = Generator(model="gpt-4", prompt=generate_metaphor_queries)
            query = f"""\
                Aim: {summary["aim"]}
                Method: {summary["method"]}
                Ideas: {summary["ideas"]}
                Context: {context_summary}
                """
            metaphor_queries = json.loads(gen.generate(query))
            relevant_papers = get_relevant_papers(metaphor_queries["queries"])
            st.write(
                "Found",
                len(relevant_papers),
                'relevant papers. Click the "Start Download" button to download them.',
            )
            if st.button("Download Now!", type="primary"):
                download_progress = st.progress(0, text="Downloading papers")
                download_progress.progress(0)
                downloaded_papers_count = 0
                for i, paper in enumerate(relevant_papers):
                    if download_paper(paper):
                        downloaded_papers_count += 1
                    download_progress.progress(i / len(relevant_papers))
                download_progress.progress(1.0)
                st.write("Successfully downloaded", downloaded_papers_count, "papers.")
                return {"downloaded_papers_count": downloaded_papers_count}
        else:
            st.write("Please generate summary first.")
        return {}


class GenerateLiteratureSurvey(components.Page):
    def render(self) -> dict:
        document_store = InMemoryDocumentStore(embedding_dim=1536)
        document_converter = PDFToTextConverter()
        preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="word",
            split_length=120,
            split_overlap=0,
            split_respect_sentence_boundary=False,
        )

        retriever = EmbeddingRetriever(
            document_store=document_store,
            batch_size=128,
            embedding_model="text-embedding-ada-002",
            api_key="",
            max_seq_len=1024,
        )
        st.header("Generate Literature Survey")
        st.write("The tool will now generate the literature survey for you. Sit tight!")
        paper_files = os.listdir(PAPER_DOWNLOAD_PATH)
        st.write(
            "Found",
            len(paper_files),
            "papers.",
        )
        if st.button("Start Generating", type="primary"):
            st.write("Preprocessing papers...")
            preprocess_progress = st.progress(0, text="Preprocessing papers")
            preprocess_progress.progress(0)
            titles = preprocess_and_insert_papers(
                paper_files,
                preprocess_progress,
                document_converter,
                preprocessor,
                retriever,
                document_store,
            )
            preprocess_progress.progress(1.0)
            st.write("Generating paper reviews...")
            generate_progress = st.progress(0, text="Generating paper reviews")
            st.session_state["paper_reviews"] = {}
            for idx, title in enumerate(titles):
                generate_progress.progress(idx / len(titles))
                st.session_state["paper_reviews"][title] = json.loads(
                    generate_review(title, retriever)
                )
            generate_progress.progress(1.0)
            st.write("Generated", len(titles), "papers.")

        return {}


first_page = GetAndSummarizeRawContent(name="intro")
second_page = GetPaperSummary(name="summary")
third_page = DownloadPapers(name="download")
fourth_page = GenerateLiteratureSurvey(name="generate")

wizard = components.Wizard([first_page, second_page, third_page, fourth_page])

wizard.render()
