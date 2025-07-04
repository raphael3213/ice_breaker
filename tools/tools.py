from langchain_tavily import TavilySearch


def get_profile_url_tavily(name: str):
    "Searches for LinkedIn or Twitter Profile pages"
    search = TavilySearch()
    res = search.run(f"{name}")
    return res