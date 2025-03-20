import asyncio
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import Agent, Controller
from pydantic import BaseModel

# dotenv
load_dotenv()

required_envs = ["DEEPSEEK_API_KEY", "CHROME_PATH"]
for env in required_envs:
    if not os.getenv(env):
        raise ValueError(f"{env} is not set")


browser = Browser(
    config=BrowserConfig(headless=False, chrome_instance_path=os.getenv("CHROME_PATH"))
)

controller = Controller()


class Content(BaseModel):
    file_name: str
    content: str


@controller.action("Save the content to a file", param_model=Content)
def save_file(content: Content):
    with open(content.file_name, "w", encoding="utf-8") as f:
        f.write(content.content)

    return content.file_name


async def run_search():
    agent = Agent(
        task=(
            """
			1. 构造一个mcp服务，提供浏览器操作的功能
               1. 打开网站 https://admin-sit.xuangubao.com.cn/
               2. 点击文章，点击发布文章，进入发布文章的页面。
               3. 从文本中解析文章标题，副标题，输入文章摘要。
			"""
        ),
        llm=ChatOpenAI(
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            api_key=SecretStr(os.getenv("DEEPSEEK_API_KEY")),
        ),
        controller=controller,
        tool_call_in_content=True,
        use_vision=False,
        generate_gif=False,
        browser=browser,
    )

    await agent.run()


if __name__ == "__main__":
    asyncio.run(run_search())
