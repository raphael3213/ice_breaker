import json

from dotenv import load_dotenv
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from third_parties.linkedin import scrape_linkedin_profile

if __name__ == "__main__":
    load_dotenv()

    print("Hello LangChain")


    summary_template = """
           Given the information {information} about a person, I want you to create a JSON object with the following fields:
           - name: The person's full name
           - age: The person's age in years
           - summary : a long summary of the person
           - facts : two interesting facts about the person

           Also remove any non ascii characters from the result
           """

    response_schemas = [
        ResponseSchema(name="name", description="The person's full name"),
        ResponseSchema(name="age", description="The person's age in years"),
        ResponseSchema(name="summary", description="A long summary of the person"),
        ResponseSchema(
            name="facts", description="A list of two interesting facts about the person"
        ),
    ]

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash")
    linkedin_data = scrape_linkedin_profile(
        "https://www.linkedin.com/in/joel-peter-d-souza-5807a2146/", True
    )

    chain = summary_prompt_template | llm | StructuredOutputParser(response_schemas=response_schemas)
    res = chain.invoke(input={"information": linkedin_data})

    print(json.dumps(res, indent=2))