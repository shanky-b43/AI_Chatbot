from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from graph.state import GraphState
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger
from mcp_integration.clients import execute_sql_tool, search_documents_tool

def _build_it_agent(specialty: str, description: str):
    sub_node = specialty.lower().replace(" ", "_").replace("&", "and")
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.2
    ).with_config({"tags": ["worker"]})
    
    tools = [execute_sql_tool, search_documents_tool]
    
    system_prompt = (
        f"You are an expert IT Support AI assistant specializing in {specialty}. "
        f"{description} "
        f"Your specific sub_node identifier is '{sub_node}'. When using the search_documents_tool, "
        "you MUST pass this sub_node identifier to filter for relevant documents.\n"
        "You have access to a database (for IT assets and tickets) and Elasticsearch (for IT guides). "
        "Ask for error codes or specific system details if troubleshooting.\n"
        "CRITICAL INSTRUCTION: If the database or document search returns empty results or you cannot find the requested information in the provided context, you MUST politely decline to answer. Do NOT generate mockup data, hallucinate, or guess. State clearly that the information is not available in the company records."
    )
    
    # We use LangGraph's built-in ReAct agent for tool execution
    return create_react_agent(llm, tools=tools, prompt=system_prompt)

@WorkflowRegistry.register("it_it_helpdesk_support")
def build_it_helpdesk():
    return _build_it_agent("IT Helpdesk Support", "You assist with general IT tickets, password resets, and tech support.")

@WorkflowRegistry.register("it_user_account_management")
def build_it_accounts():
    return _build_it_agent("User Account Management", "You assist with creating/modifying accounts and access control.")

@WorkflowRegistry.register("it_hardware_asset_management")
def build_it_hardware():
    return _build_it_agent("Hardware Asset Management", "You assist with laptops, monitors, phones, and physical assets.")

@WorkflowRegistry.register("it_software_management")
def build_it_software():
    return _build_it_agent("Software Management", "You assist with software licenses, installations, and updates.")

@WorkflowRegistry.register("it_network_management")
def build_it_network():
    return _build_it_agent("Network Management", "You assist with VPN, Wi-Fi, internet connectivity, and network issues.")

@WorkflowRegistry.register("it_system_administration")
def build_it_sysadmin():
    return _build_it_agent("System Administration", "You assist with server maintenance, infrastructure, and backend systems.")

@WorkflowRegistry.register("it_cybersecurity_operations")
def build_it_cybersec():
    return _build_it_agent("Cybersecurity Operations", "You assist with security incidents, phishing, and threat management.")

@WorkflowRegistry.register("it_monitoring_and_alerting")
def build_it_monitoring():
    return _build_it_agent("Monitoring & Alerting", "You assist with system uptime, alerts, and performance monitoring.")

@WorkflowRegistry.register("it_backup_and_disaster_recovery")
def build_it_backup():
    return _build_it_agent("Backup & Disaster Recovery", "You assist with data backups, restoration, and continuity planning.")

@WorkflowRegistry.register("it_it_policy_management")
def build_it_policy():
    return _build_it_agent("IT Policy Management", "You assist with IT security policies, compliance, and guidelines.")
