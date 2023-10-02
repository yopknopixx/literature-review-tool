from metaphor_python import Metaphor
import math
import scidownl
import arxiv
import os
from haystack.nodes import PDFToTextConverter, EmbeddingRetriever, PreProcessor
from haystack.document_stores import InMemoryDocumentStore
from prompts import *
from generation import *


metaphor = Metaphor("")

paper_domains = [
    "scholar.google.com",
    "jstor.org",
    "ncbi.nlm.nih.gov",
    "springer.com",
    "ieeexplore.ieee.org",
    "sciencedirect.com",
    "onlinelibrary.wiley.com",
    "journals.sagepub.com",
    "ebscohost.com",
    "nature.com",
    "pnas.org",
    "sciencedirect.com",
    "academic.oup.com",
    "cambridge.org",
    "taylorandfrancis.com",
    "journals.plos.org",
    "biomedcentral.com",
    "arxiv.org",
    "sciencemag.org",
    "ssrn.com",
    "muse.jhu.edu",
    "emerald.com",
    "royalsocietypublishing.org",
    "jstage.jst.go.jp",
    "annualreviews.org",
    "frontiersin.org",
    "journals.aps.org",
    "dl.acm.org",
    "zbmath.org",
]

PAPER_DOWNLOAD_PATH = "./papers/"


def get_relevant_papers(queries):
    num_docs_per_query = math.ceil(30 / len(queries))
    papers = []
    for query in queries:
        papers.extend(
            metaphor.search(
                query,
                num_results=num_docs_per_query,
                include_domains=paper_domains,
                use_autoprompt=True,
            ).results
        )
    return papers


def download_paper(paper):
    if "arxiv.org" in paper.url:
        doi = paper.url.split("/")[-1].split("?")[0].split("v")[0].strip(".pdf")
        paper = next(arxiv.Search(id_list=[doi]).results())
        paper.download_pdf(dirpath=PAPER_DOWNLOAD_PATH, filename=f"{paper.title}.pdf")
    else:
        scidownl.scihub_download(
            paper.title,
            paper_type="title",
            out=PAPER_DOWNLOAD_PATH,
        )
    if paper.title + ".pdf" in os.listdir(PAPER_DOWNLOAD_PATH):
        return True
    else:
        return False


def get_context(context_queries):
    context_ids = []
    for query in context_queries:
        search_response = metaphor.search(
            query,
            num_results=1,
            use_autoprompt=True,
        )
        context_ids.append(search_response.results[0].id)
    return metaphor.get_contents(context_ids)


def preprocess_and_insert_papers(
    paper_filenames, progress_bar, converter, preprocessor, retriever, document_store
):
    titles = []
    document_store.delete_documents()
    for idx, docname in enumerate(paper_filenames):
        print("Processing", idx, "of", len(paper_filenames))
        progress_bar.progress(idx / len(paper_filenames))
        if docname.endswith(".pdf"):
            print("Converting document")
            doc = converter.convert(file_path=f"papers/{docname}")
            doc[0].meta["title"] = docname.strip(".pdf")
            print("Adding titel to list")
            if doc[0].meta["title"] not in titles:
                titles.append(doc[0].meta["title"])
            print("Preprocessing document")
            doc = preprocessor.process(doc)
            print("Writing document to store")
            document_store.write_documents(doc)
            print("Updating embeddings")
            document_store.update_embeddings(
                retriever, update_existing_embeddings=False
            )
    progress_bar.progress(1.0)
    return titles


def generate_review(paper_title, retriever):
    gen = Generator(model="gpt-4", prompt=generate_literature_survey)
    relevant_docs = retriever.retrieve(
        get_relevant_paper_content, top_k=12, filters={"title": paper_title}
    )
    context = "".join([doc.content for doc in relevant_docs])
    review = gen.generate(context)
    return review
