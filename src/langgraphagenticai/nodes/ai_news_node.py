from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate

class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNodewith API keys for tavily and qroq
        """
        self.tavily=TavilyClient()
        self.llm=llm

        self.state={}

    def fetch_news(self, state: dict)->dict:
        """
        Fetch AI news based on specified frequency.

        Args:
            state (dict):The state dictionary containing frequency
        Returns:
            dict:update state with 'news data' key conatining fetched news.

        """
        print("inside fetch news")
        frequency=state['messages'][0].content.lower()
        print(frequency)
        print("frequency result")
        self.state['frequency']=frequency
        print(self.state['frequency'])
        time_range_map={'daily':'d', 'weekly':'w', 'monthly':'m', 'year':'y'}
        days_map={'daily':1, 'weekly':7, 'monthly':30, 'year':366}
        
        response=self.tavily.search(
            query="Top Artificila news (AI) in India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=15,
            days=days_map[frequency],
        )

        state['news_data']=response.get('results',[])
        self.state['news_data']=state['news_data']
        print("the news data is",self.state['news_data'])
        return state
    
    def summarize_news(self,state:dict)->dict:
        """
        Summarize the fetched news using llm
        Args:
            state (dict):The state dictionary containing news data
        
        Returns:
            dict:update state with 'summary' key conatining summarized news.
                   
        """
        news_item=self.state["news_data"]
        prompt_template=ChatPromptTemplate([
            ("system", """Summarize ai news articals into markdown format.for each item include:
             -  Date in **YYYY-MM-DD** format in IST timezone
             -Concise sentecnes summary from latest news
             -Sort news by date wise
             -Source urls as link
             Use format:
             ### [date]
             [summary](urls)"""),
             ("user","Articles:\n{articals}")
        ])

        articles_str="\n\n".join([
            f"Content:{item.get('content','')}\nURL:{item.get('url','')}\nDate:{item.get('published_date','')}"
            for item in news_item
        ])

        response=self.llm.invoke(prompt_template.format(articals=articles_str))
        state['summary']=response.content
        self.state['summary']=state['summary']
        print("the summarized news data is",self.state['summary'])
        return self.state
    
    def save_result(self,state):
        frequency=self.state['frequency']
        summary=self.state['summary']
        filename = f"./AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename']=filename
        return self.state




