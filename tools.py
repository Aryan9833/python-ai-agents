

from langchain_community.tools import WikipediaQueryRun , DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime



def save_to_txt(data: str, filename: str = "result.txt"):
    timestamp = datetime.now().strftime("%Y%m-%d_%H%M%S")
    formatted_text = f"---- Research Output ----\ntimestamp: {timestamp}\n{data}\n\n"

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)
        print(f"✅ File successfully saved to {filename}")
    except Exception as e:
        print(f"❌ Failed to save to {filename}: {e}")


save_tool = Tool(
    name="save_to_text_file",
    func=save_to_txt,
    description="Save structured file to  file",

)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name ="Serach",
    func = search.run,
    description="Serach the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=5, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)