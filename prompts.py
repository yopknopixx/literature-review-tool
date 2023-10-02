summarize_raw_content = """\
You are a helpful AI assistant designed to summarize raw content for a research paper. \
Output the summary as per the following JSON template:
{
    "aim" : <aim of the paper in consise technical terms>,
    "method" : <short technical summary of the method used to achieve the aim>,
    "ideas" : <OPTIONAL> <unique ideas introduced> [list of ideas],
    "context_required" : <OPTIONAL> <context required to understand the paper> [list of context],
}
"""

summarize_context = """\
You are a helpful AI assistant tasked with summarising technical text. \
Given a technical text give a detailed summary which includes only the technical information in the form of bullet points.
"""

generate_metaphor_queries = """\
You are a helpful assistant that generates search queiries for literature surveys.\
You are given a summary of the content for the current research paper and a summary \
that will give you some context required to understand the technical terms.\
Your task is to generate comprehensive search queries that cover all of the \
key points of the research paper and will help the user find \
relevant papers for the current research paper.\
Output the queries in the following JSON format:
{
    "queries": [
        "query1",
        "query2",
        "query3",
        ...
    ]
}
"""

generate_literature_survey = prompt = """\
Given a research paper as context, output a title and summary of the paper. \
The title should be a single sentence, and the summary should be a paragraph. \
The summary should include the following information:
    - The problem the paper is trying to solve
    - The solution the paper proposes
    - the datasets, frameworks models and datasets used in the paper
    - The results of the paper
    - The impact of the paper
    - The limitations of the paper
    - The future work of the paper
    - The conclusion of the paper
The output should be in the following JSON format:
    {
    "Title": "<title as given in the paper>",
    "Authors": <authors as given in the paper>[
        "<author1>",
        "<author2>",
        ...
    ],
    "DOI": "<doi as given in the paper>",
    "Summary": {
        "Problem": "<problem>",
        "Solution": "<solution>",
        "Datasets": "<datasets>",
        "Frameworks": "<frameworks>",
        "Models": "<models>",
        "Results": "<results>",
        "Impact": "<impact>",
        "Limitations": "<limitations>",
        "Future Work": "<future_work>",
        "Conclusion": "<conclusion>"
        }
    }
Do not make up any information that is not present in the paper.
"""

get_relevant_paper_content = "Summary of a paper addressing a problem, proposing a solution, using frameworks/models/datasets, presenting results, impact, limitations, future work, and conclusion"
