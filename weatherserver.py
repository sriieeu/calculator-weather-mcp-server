from mcp.server.fastmcp import FastMCP
mcp = FastMCP("Weather") 
@mcp.tool()
async def get_weather(city:str)->dict:
    """Get the weather of a city with additional info"""
    # Example static data; in a real app, fetch from an API
    return {
        "description": f"The weather of {city} is sunny",
        "temperature": "25°C",
        "humidity": "60%",
        "wind_speed": "10 km/h"
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")