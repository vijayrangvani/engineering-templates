"""TEMPLATE: force the LLM to return validated JSON via a Pydantic model.

Why: downstream code needs fields, not free text. Validation catches bad outputs.
"""
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class Ticket(BaseModel):
    category: str = Field(description="billing | technical | account | other")
    priority: int = Field(ge=1, le=5)
    summary: str


def classify(text: str) -> Ticket:
    client = OpenAI()
    resp = client.beta.chat.completions.parse(  # .parse() validates into the Pydantic class
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Classify the support ticket."},
            {"role": "user", "content": text},
        ],
        response_format=Ticket,
    )
    return resp.choices[0].message.parsed  # a Ticket object, already validated


if __name__ == "__main__":
    print(classify("I was charged twice this month, please fix ASAP"))
