# server.py
from mcp.server.fastmcp import FastMCP
import asyncio
from crawl4ai import AsyncWebCrawler

# Create an MCP server
mcp = FastMCP("WebCrawler")

@mcp.tool()
async def crawl_website(url: str) -> str:
    """
    爬取指定网站的内容并返回其 markdown 格式的文本
    参数:
        url: 要爬取的网站URL
    返回:
        str: 网站内容的markdown格式文本
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

@mcp.resource("website://{url}")
async def get_website_content(url: str) -> str:
    """
    获取指定网站的内容作为资源
    参数:
        url: 要获取内容的网站URL
    返回:
        str: 网站内容的markdown格式文本
    """
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url)
        return result.markdown

if __name__ == "__main__":
    mcp.run()