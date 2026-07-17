from pydantic import BaseModel, Field
from typing import Literal, Optional

class RouterOutput(BaseModel):
    agent: Literal["hr", "finance", "it", "conversation", "dbtalk", "summary"] = Field(
        description="The primary agent to route the query to."
    )
    sub_node: Optional[Literal[
        # Finance
        "Account Payable", "Account Receivable", "Expense Management", "Payroll", 
        "Budget Planning", "Taxation", "Financial Reporting", "Procurement Finance", 
        "Auditing and Compliance",
        # HR
        "Recruitment & Hiring", "Employee Onboarding", "Attendance & Leave Management",
        "HR Policy Management", "Employee Helpdesk", "Compliance Management & Exit Management",
        # IT
        "IT Helpdesk Support", "User Account Management", "Hardware Asset Management",
        "Software Management", "Network Management", "System Administration",
        "Cybersecurity Operations", "Monitoring & Alerting", "Backup & Disaster Recovery",
        "IT Policy Management"
    ]] = Field(
        default=None,
        description="The specific sub-node for the agent, if applicable. Required if agent is 'finance', 'hr', or 'it'."
    )
