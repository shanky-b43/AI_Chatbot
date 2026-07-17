from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from workflows.registry import WorkflowRegistry
from core.config import settings
from loguru import logger
from mcp_integration.clients import execute_sql_tool, search_documents_tool

def _build_finance_agent(specialty: str, description: str):
    sub_node = specialty.lower().replace(" ", "_").replace("&", "and")
    llm = ChatOllama(
        model=settings.CHAT_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.2
    ).with_config({"tags": ["worker"]})
    
    tools = [execute_sql_tool, search_documents_tool]
    
    system_prompt = (
        f"You are an expert Finance AI assistant specializing in {specialty}. "
        f"{description} "
        f"Your specific sub_node identifier is '{sub_node}'. When using the search_documents_tool, "
        "you MUST pass this sub_node identifier to filter for relevant documents.\n"
        "You have access to a database (for financial records) and Elasticsearch (for Finance policies).\n"
        "CRITICAL INSTRUCTION: If the database or document search returns empty results or you cannot find the requested information in the provided context, you MUST politely decline to answer. Do NOT generate mockup data, hallucinate, or guess. State clearly that the information is not available in the company records."
    )
    
    return create_react_agent(llm, tools=tools, prompt=system_prompt)

@WorkflowRegistry.register("finance_account_payable")
def build_account_payable():
    return _build_finance_agent("Account Payable", "You assist with paying vendors, bills, and managing outgoing money.")

@WorkflowRegistry.register("finance_account_receivable")
def build_account_receivable():
    return _build_finance_agent("Account Receivable", "You assist with incoming money, client payments, and sent invoices.")

@WorkflowRegistry.register("finance_expense_management")
def build_expense_management():
    return _build_finance_agent("Expense Management", "You assist with employee reimbursements, travel expenses, and expense reports.")

@WorkflowRegistry.register("finance_payroll")
def build_payroll():
    return _build_finance_agent("Payroll", "You assist with employee salaries, tax deductions, and pay slips.")

@WorkflowRegistry.register("finance_budget_planning")
def build_budget_planning():
    return _build_finance_agent("Budget Planning", "You assist with department budgets, forecasting, and cost planning.")

@WorkflowRegistry.register("finance_taxation")
def build_taxation():
    return _build_finance_agent("Taxation", "You assist with corporate taxes, compliance with tax laws, and GST/VAT.")

@WorkflowRegistry.register("finance_financial_reporting")
def build_financial_reporting():
    return _build_finance_agent("Financial Reporting", "You assist with balance sheets, P&L statements, and quarterly reports.")

@WorkflowRegistry.register("finance_procurement_finance")
def build_procurement_finance():
    return _build_finance_agent("Procurement Finance", "You assist with purchasing hardware/software and vendor negotiations.")

@WorkflowRegistry.register("finance_auditing_and_compliance")
def build_auditing():
    return _build_finance_agent("Auditing and Compliance", "You assist with internal audits, financial regulations, and compliance checks.")
