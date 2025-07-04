from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather") 
@mcp.tool()
async def get_weather(city:str)->str:
    """Get the weather of a city"""
    return f"The weather of {city} is sunny" 

if __name__ == "__main__":
    mcp.run(transport="streamable-http")