import os

from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langsmith import Client

from tools.tools import get_profile_url_tavily

load_dotenv()



def lookup(name: str, place_of_work:str) -> str:
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")

    template = """
    Given the full name {name_of_person} and where they work {place_of_work}, I want you to get me a link to their LinkedIn profile page. Your answers should contain ONLY a url.
    """

    prompt_template = PromptTemplate(
        template=template,input_variables=["name_of_person"]
    )

    client = Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    react_prompt = client.pull_prompt("hwchase17/react", include_model=True)

    tools_for_agents = [
        Tool(
            name="Crawl google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the LinkedIn profile page URL",
        )
    ]

    react_agent = create_react_agent(llm=llm, tools=tools_for_agents, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=react_agent, tools=tools_for_agents, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name, place_of_work=place_of_work)}
    )

    linkedin_profile_url_result = result["output"]
    return linkedin_profile_url_result

if __name__ == "__main__":
    linkedin_profile_url = lookup(name = "Joel Peter", place_of_work="Ather Energy")
    print(linkedin_profile_url)