from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
import asyncio
from dotenv import load_dotenv
from tools import extract_text_from_pdf

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(model=model, model_provider=external_client, tracing_disabled=True)


async def main(file_path: str):
    agent = Agent(
        name="StudyNotesAgent",
        instructions=f"Read the PDF file at {file_path}, generate a summary and a mcq's quiz based on its content.",
        model=model,
        tools=[extract_text_from_pdf],
    )

    result = await Runner.run(
        agent,
        f"Extract text from {file_path} and generate a summary and mcq's quiz and provide it's answers.",
        run_config=config,
    )
    return result.final_output


if __name__ == "__main__":
    # This part is for testing the agent directly, not used by the Streamlit app
    # You would need to provide a file path to a PDF to test this.
    # For example:
    # asyncio.run(main("path/to/your/pdf.pdf"))
    pass
