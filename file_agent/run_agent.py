import asyncio
from mcp.agent import Agent
from mcp.llms.ollama import OllamaLLM
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.proxy import ProxyTool


async def main():
    # Step 1: Launch the tool server via stdio
    async with stdio_client(
        StdioServerParameters(command="python", args=["servery.py"])
    ) as (read, write):

        # Step 2: Start a session
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Step 3: Wrap tools as ProxyTools
            tools = await ProxyTool.list_from_session(session)

            # Step 4: Set up Ollama + Agent
            llm = OllamaLLM(model="llama3")  # or "mistral", etc.
            agent = Agent(tools=tools, llm=llm)

            # Step 5: Let the model decide what to do
            result = await agent.arun("Fetch the content of https://example.com")
            print("\n🤖 Result:", result)


asyncio.run(main())
