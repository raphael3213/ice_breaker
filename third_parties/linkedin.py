import os
import pprint

import requests
from dotenv import load_dotenv
from langchain.output_parsers import ResponseSchema

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from a Linkedin profile
    Manually scrape the information from the Linkedin profile"""

    if mock:
        linkedin_profile_url = os.getenv("LINKEDIN_SCRAPER_PROFILE_MOCK_URL")
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPIN_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }

        response = requests.get(api_endpoint, params, timeout=10)

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }
    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/joel-peter-d-souza-5807a2146/", True
        )
    )
