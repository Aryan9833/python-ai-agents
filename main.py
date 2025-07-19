from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os
from openai import OpenAI
from tools import search_tool, wiki_tool , save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    thinking: str
    language: str

# Environment variables
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")
model = os.getenv("OPENROUTER_MODEL")

# Initialize LLM
llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)

# Initialize parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Correct prompt construction using from_messages()
prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a research assistant that will help generate a research paper.\n
     Answer the user query and use necessary tools.\n
     Wrap the output in this format and provide no other text:
     {format_instructions}"""),
    MessagesPlaceholder("chat_history", optional=True),
    ("human","{input}"),
    MessagesPlaceholder("agent_scratchpad")
]).partial(format_instructions=parser.get_format_instructions())


tools =[search_tool, wiki_tool, save_tool]
# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools  # Add your tools here if you have any
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
input =input("what can help with reserch ?")
raw_response = agent_executor.invoke({"input": input,
        "chat_history":[]                             })
# Execute the agent
try:
    structured_reponse = parser.parse(raw_response.get("output"))

    print(structured_reponse)
except Exception as e:
    print(f"An error occurred: {e}")