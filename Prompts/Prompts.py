import yaml
from langchain.utilities import WikipediaAPIWrapper 

wiki = WikipediaAPIWrapper(wiki_client=None,top_k_results=1,doc_content_chars_max=1000)


def load_prompt_from_yaml(file_path: str) -> str:
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config




def wikipedia_search(keywords):
    wiki_research = wiki.run(keywords) 
    return wiki_research
