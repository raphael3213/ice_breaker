import json

from dotenv import load_dotenv
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from output_parsers import summary_parser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str, place_of_work: str) -> str :
    # linkedin_url = linkedin_lookup_agent(name = name, place_of_work = place_of_work)
    linkedin_data = scrape_linkedin_profile("linkedin_url", True)

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

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")

    chain = (
        summary_prompt_template
        | llm
        | summary_parser
    )
    res = chain.invoke(input={"information": linkedin_data})

    return json.dumps(res, indent=2)


if __name__ == "__main__":
    load_dotenv()
    print(ice_break_with("Joel Peter Dsouza", "Ather Energy"))


