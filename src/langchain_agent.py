from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from playwright.sync_api import sync_playwright
import os

class LangChainBrowserAgent:
    def __init__(self):
        # Initialize Playwright browser
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        
        # Initialize Playwright toolkit with the browser
        self.toolkit = PlayWrightBrowserToolkit(sync_browser=self.browser)
        self.tools = self.toolkit.get_tools()

        # Initialize LLM (requires OpenAI API key)
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.llm = ChatOpenAI(
                model="gpt-4",
                temperature=0,
                openai_api_key=api_key
            )
        else:
            self.llm = None

        # Create a simple prompt for basic tool usage
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a web automation assistant. Use the available tools to help with web tasks.
            
Available tools: navigate_browser, click_element, current_web_page, etc.

For navigation: Use navigate_browser with a URL.
For clicking: Use click_element with a selector or text.
For getting page content: Use current_web_page.

Keep responses concise."""),
            ("user", "{input}"),
        ])

    def execute_instruction(self, instruction):
        """Execute a natural language instruction using LangChain tools"""
        try:
            if not self.llm:
                return {
                    "success": False,
                    "error": "OpenAI API key not found. Please set OPENAI_API_KEY environment variable to use AI Agent mode."
                }
            
            # For now, provide a simple response indicating the toolkit is available
            # In a full implementation, this would use the agent to call tools
            return {
                "success": True,
                "result": f"LangChain agent received: {instruction}. Browser initialized with {len(self.tools)} tools available.",
                "tools_available": [tool.name for tool in self.tools]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def cleanup(self):
        """Clean up browser resources"""
        if hasattr(self, 'browser'):
            self.browser.close()
        if hasattr(self, 'playwright'):
            self.playwright.stop()

# Global instance
langchain_agent = None

def get_langchain_agent():
    global langchain_agent
    if langchain_agent is None:
        langchain_agent = LangChainBrowserAgent()
    return langchain_agent