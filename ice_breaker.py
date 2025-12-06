import json
from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from output_parsers import summary_parser, Summary
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> Tuple[Summary, str] :
    linkedin_url = linkedin_lookup_agent(name = name)
    linkedin_data = scrape_linkedin_profile(linkedin_url, False)

    summary_template = """
             Given the information {information} about a person, I want you to create a JSON object with the following fields:
             - name: The person's full name
             - age: The person's age in years
             - summary : a long summary of the person
             - facts : two interesting facts about the person

             Also remove any non ascii characters from the result
             
             {format_instructions}
             """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template, partial_variables={"format_instructions": summary_parser.get_format_instructions()}
    )

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")

    chain = (
        summary_prompt_template
        | llm
        | summary_parser
    )
    res:Summary = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("photoUrl")


if __name__ == "__main__":
    load_dotenv()
    print(ice_break_with("Joel Peter Dsouza"))


