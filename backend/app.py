# import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

from dotenv import load_dotenv
load_dotenv()
# Initialize search tool
search_tool = SerperDevTool()

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:3000",  # Next.js frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#duckduckgo_search = DuckDuckGoSearchRun()

class ProductRequest(BaseModel):
    product_name: str

@app.post("/run-crewai")
async def run_crewai(product_request: ProductRequest):
    product_name = product_request.product_name

    # Define Agents
    market_research_analyst = Agent(
        role="Market Research Analyst",
        goal=f"Analyze the market demand for {product_name} and suggest marketing strategies",
        backstory=f"Expert at understanding market demand, target audience, and competition for products like {product_name}. Skilled in developing marketing strategies to reach a wide audience.",
        verbose=True,
        allow_delegation=True,
        #tools=[duckduckgo_search],
        tools=[search_tool],
    )

    technology_expert = Agent(
        role="Technology Expert",
        goal=f"Assess technological feasibilities and requirements for producing high-quality {product_name}",
        backstory=f"Visionary in current and emerging technological trends, especially in products like {product_name}. Identifies which technologies are best suited for different business models.",
        verbose=True,
        allow_delegation=True,
    )

    business_consultant = Agent(
        role="Business Development Consultant",
        goal=f"Evaluate the business model for {product_name}, focusing on scalability and revenue streams",
        backstory=f"Seasoned in shaping business strategies for products like {product_name}. Understands scalability and potential revenue streams to ensure long-term sustainability.",
        verbose=True,
        allow_delegation=True,
    )

    # Define Tasks
    task1 = Task(
        description=f"Analyze the market demand for {product_name}. Current month is Jan 2024. Write a report on the ideal customer profile and marketing strategies to reach the widest possible audience. Include at least 10 bullet points addressing key marketing areas.",
        agent=market_research_analyst,
        expected_output="Report with ideal customer profile and marketing strategies."
    )

    task2 = Task(
        description=f"Assess the technological aspects of manufacturing high-quality {product_name}. Write a report detailing necessary technologies and manufacturing approaches. Include at least 10 bullet points on key technological areas.",
        agent=technology_expert,
        expected_output="Report with necessary technologies and manufacturing approaches."
    )

    task3 = Task(
        description=f"Summarize the market and technological reports and evaluate the business model for {product_name}. Write a report on the scalability and revenue streams for the product. Include at least 10 bullet points on key business areas. Give Business Plan, Goals and Timeline for the product launch. Current month is Jan 2024.",
        agent=business_consultant,
        expected_output="Report on scalability, revenue streams, business plan, goals, and timeline."
    )

    # Create and Run the Crew
    product_crew = Crew(
        agents=[market_research_analyst, technology_expert, business_consultant],
        tasks=[task1, task2, task3],
        verbose=2,
        process=Process.sequential,
    )

    crew_result = product_crew.kickoff()
    return {"result": crew_result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from crewai import Agent, Task, Crew, Process
# #from langchain.tools import DuckDuckGoSearchRun
# import os
# from crewai_tools import SerperDevTool

# # Initialize search tool
# search_tool = SerperDevTool()

# app = FastAPI()

# # Set up CORS
# origins = [
#     "http://localhost:3000",  # Next.js frontend URL
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# #duckduckgo_search = DuckDuckGoSearchRun()

# class ProductRequest(BaseModel):
#     product_name: str

# @app.post("/run-crewai")
# async def run_crewai(product_request: ProductRequest):
#     product_name = product_request.product_name

#     # Define Agents
#     market_research_analyst = Agent(
#         role="Market Research Analyst",
#         goal=f"Analyze the market demand for {product_name} and suggest marketing strategies",
#         backstory=f"Expert at understanding market demand, target audience, and competition for products like {product_name}. Skilled in developing marketing strategies to reach a wide audience.",
#         verbose=True,
#         allow_delegation=True,
#         #tools=[duckduckgo_search],
#         tools=[search_tool],
#     )

#     technology_expert = Agent(
#         role="Technology Expert",
#         goal=f"Assess technological feasibilities and requirements for producing high-quality {product_name}",
#         backstory=f"Visionary in current and emerging technological trends, especially in products like {product_name}. Identifies which technologies are best suited for different business models.",
#         verbose=True,
#         allow_delegation=True,
#     )

#     business_consultant = Agent(
#         role="Business Development Consultant",
#         goal=f"Evaluate the business model for {product_name}, focusing on scalability and revenue streams",
#         backstory=f"Seasoned in shaping business strategies for products like {product_name}. Understands scalability and potential revenue streams to ensure long-term sustainability.",
#         verbose=True,
#         allow_delegation=True,
#     )

#     # Define Tasks
#     task1 = Task(
#         description=f"Analyze the market demand for {product_name}. Current month is Jan 2024. Write a report on the ideal customer profile and marketing strategies to reach the widest possible audience. Include at least 10 bullet points addressing key marketing areas.",
#         agent=market_research_analyst,
#         expected_output="Report with ideal customer profile and marketing strategies."
#     )

#     task2 = Task(
#         description=f"Assess the technological aspects of manufacturing high-quality {product_name}. Write a report detailing necessary technologies and manufacturing approaches. Include at least 10 bullet points on key technological areas.",
#         agent=technology_expert,
#         expected_output="Report with necessary technologies and manufacturing approaches."
#     )

#     task3 = Task(
#         description=f"Summarize the market and technological reports and evaluate the business model for {product_name}. Write a report on the scalability and revenue streams for the product. Include at least 10 bullet points on key business areas. Give Business Plan, Goals and Timeline for the product launch. Current month is Jan 2024.",
#         agent=business_consultant,
#         expected_output="Report on scalability, revenue streams, business plan, goals, and timeline."
#     )

#     # Create and Run the Crew
#     product_crew = Crew(
#         agents=[market_research_analyst, technology_expert, business_consultant],
#         tasks=[task1, task2, task3],
#         verbose=2,
#         process=Process.sequential,
#     )

#     crew_result = product_crew.kickoff()
#     return {"result": crew_result}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# from crewai import Agent, Task, Crew, Process
# from crewai_tools import SerperDevTool
# #from langchain.tools import DuckDuckGoSearchRun
# import gradio as gr


# os.environ["OPENAI_API_KEY"] = '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'
# os.environ["SERPER_API_KEY"] = "239ace87a7bf0c234c93217ed61ccfa3b832245b"  # serper.dev API key

# # Initialize search tool
# search_tool = SerperDevTool()

# def create_crewai_setup(product_name):
#     # Define Agents
#     market_research_analyst = Agent(
#         role="Market Research Analyst",
#         goal=f"""Analyze the market demand for {product_name} and 
#                 suggest marketing strategies""",
#         backstory=f"""Expert at understanding market demand, target audience, 
#                     and competition for products like {product_name}. 
#                     Skilled in developing marketing strategies 
#                     to reach a wide audience.""",
#         verbose=True,
#         allow_delegation=True,
#         tools=[search_tool],
#     )
    
#     technology_expert = Agent(
#         role="Technology Expert",
#         goal=f"Assess technological feasibilities and requirements for producing high-quality {product_name}",
#         backstory=f"""Visionary in current and emerging technological trends, 
#                     especially in products like {product_name}. 
#                     Identifies which technologies are best suited 
#                     for different business models.""",
#         verbose=True,
#         allow_delegation=True,
#     )
    
#     business_consultant = Agent(
#         role="Business Development Consultant",
#         goal=f"""Evaluate the business model for {product_name}, 
#             focusing on scalability and revenue streams""",
#         backstory=f"""Seasoned in shaping business strategies for products like {product_name}. 
#                     Understands scalability and potential 
#                     revenue streams to ensure long-term sustainability.""",
#         verbose=True,
#         allow_delegation=True,
#     )
    
#     # Define Tasks
#     task1 = Task(
#         description=f"""Analyze the market demand for {product_name}. Current month is Jan 2024.
#                         Write a report on the ideal customer profile and marketing 
#                         strategies to reach the widest possible audience. 
#                         Include at least 10 bullet points addressing key marketing areas.""",
#         agent=market_research_analyst,
#         expected_output="Report with ideal customer profile and marketing strategies."
#     )
    
#     task2 = Task(
#         description=f"""Assess the technological aspects of manufacturing 
#                     high-quality {product_name}. Write a report detailing necessary 
#                     technologies and manufacturing approaches. 
#                     Include at least 10 bullet points on key technological areas.""",
#         agent=technology_expert,
#         expected_output="Report with necessary technologies and manufacturing approaches."
#     )
    
#     task3 = Task(
#         description=f"""Summarize the market and technological reports 
#                     and evaluate the business model for {product_name}. 
#                     Write a report on the scalability and revenue streams 
#                     for the product. Include at least 10 bullet points 
#                     on key business areas. Give Business Plan, 
#                     Goals and Timeline for the product launch. Current month is Jan 2024.""",
#         agent=business_consultant,
#         expected_output="Report on scalability, revenue streams, business plan, goals, and timeline."
#     )
    
#     # Create and Run the Crew
#     product_crew = Crew(
#         agents=[market_research_analyst, technology_expert, business_consultant],
#         tasks=[task1, task2, task3],
#         verbose=2,
#         process=Process.sequential,
#     )
    
#     crew_result = product_crew.kickoff()
#     return crew_result

# # Gradio interface
# def run_crewai_app(product_name):
#     crew_result = create_crewai_setup(product_name)
#     return crew_result

# iface = gr.Interface(
#     fn=run_crewai_app, 
#     inputs="text", 
#     outputs="text",
#     title="CrewAI Business Product Launch",
#     description="Enter a product name to analyze the market and business strategy."
# )

# iface.launch()

## new modifie code 
# app.py
