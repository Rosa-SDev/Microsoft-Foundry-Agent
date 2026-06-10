# Before running the sample:
#    pip install azure-ai-projects>=2.1.0 python-dotenv

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

endpoint = os.getenv("AGENT_ENDPOINT")

if not endpoint:
    raise ValueError("AGENT_ENDPOINT not found in .env file")

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "computing-historian"
my_version = "1"

openai_client = project_client.get_openai_client()

while True:
    user_prompt = input("Enter a prompt for the agent (or type 'quit' to exit): ").strip()

    if user_prompt.lower() == "quit":
        break

    if not user_prompt:
        continue

    response = openai_client.responses.create(
        input=[{"role": "user", "content": user_prompt}],
        extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
    )

    print(f"Response output: {response.output_text}")