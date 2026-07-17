from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger
from mcp_integration.clients import execute_sql_tool, search_documents_tool

def _build_hr_agent(specialty: str, description: str):
    sub_node = specialty.lower().replace(" ", "_").replace("&", "and")
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.2
    ).with_config({"tags": ["worker"]})
    
    tools = [execute_sql_tool, search_documents_tool]
    
    system_prompt = (
        f"You are an expert HR AI assistant specializing in {specialty}. "
        f"{description} "
        f"Your specific sub_node identifier is '{sub_node}'. When using the search_documents_tool, "
        "you MUST pass this sub_node identifier to filter for relevant documents.\n"
        "You have access to a database (for employee records) and Elasticsearch (for HR policies). "
        "CRITICAL INSTRUCTION: You MUST ALWAYS use the `search_documents_tool` to look up accurate policies, timetables, or rules before answering a user's question. Never say you don't have access; always search the knowledge base first!\n"
        "CRITICAL INSTRUCTION 2: If the database or document search returns empty results or you cannot find the requested information in the provided context, you MUST politely decline to answer. Do NOT generate mockup data, hallucinate, or guess. State clearly that the information is not available in the company records."
    )
    
    # We use LangGraph's built-in ReAct agent for tool execution
    return create_react_agent(llm, tools=tools, prompt=system_prompt)

@WorkflowRegistry.register("hr_recruitment_and_hiring")
def build_hr_recruitment():
    return _build_hr_agent("Recruitment & Hiring", "You assist with job openings, interviews, and the hiring process.")

@WorkflowRegistry.register("hr_employee_onboarding")
def build_hr_onboarding():
    return _build_hr_agent("Employee Onboarding", "You assist with new hire setup, orientation, and training.")

@WorkflowRegistry.register("hr_attendance_and_leave_management")
def build_hr_attendance():
    return _build_hr_agent("Attendance & Leave Management", "You assist with tracking time, PTO, paid leaves, and sick days.")

@WorkflowRegistry.register("hr_hr_policy_management")
def build_hr_policy():
    return _build_hr_agent("HR Policy Management", "You assist with company policies, rules, and guidelines.")

@WorkflowRegistry.register("hr_employee_helpdesk")
def build_hr_helpdesk():
    return _build_hr_agent("Employee Helpdesk", "You provide general HR support and answer employee inquiries.")

@WorkflowRegistry.register("hr_compliance_management_and_exit_management")
def build_hr_compliance():
    return _build_hr_agent("Compliance Management & Exit Management", "You assist with legal compliance, offboarding, and resignations.")
