from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

async def main():
    # Get absolute paths for the servers
    mathserver_path = os.path.abspath("mathserver.py")
    # Weather server assumed to be running at http://localhost:8000/mcp
    client = MultiServerMCPClient(
        connections={
            "math": {
                "command": "python",
                "args": [mathserver_path],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            },
        }
    )
    # Print all available tools from both servers
    tools = await client.get_tools()
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

    # Call mathserver tools
    print("\nCalling mathserver tools:")
    async with client.session("math") as math_session:
        math_tools = await load_mcp_tools(math_session)
        add_tool = next(t for t in math_tools if t.name == "add")
        add_result = await add_tool.ainvoke({"a": 5, "b": 3})
        print(f"add(5, 3) = {add_result}")
        subtract_tool = next(t for t in math_tools if t.name == "subtract")
        subtract_result = await subtract_tool.ainvoke({"a": 10, "b": 4})
        print(f"subtract(10, 4) = {subtract_result}")

    # Call weatherserver tool
    print("\nCalling weatherserver tool:")
    async with client.session("weather") as weather_session:
        weather_tools = await load_mcp_tools(weather_session)
        get_weather_tool = next(t for t in weather_tools if t.name == "get_weather")
        weather_result = await get_weather_tool.ainvoke({"city": "New York"})
        print(f"get_weather('New York') = {weather_result}")

if __name__ == "__main__":
    asyncio.run(main())
