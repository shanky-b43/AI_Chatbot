import pytest
from langchain_core.messages import HumanMessage
from router.router import run_intent_router
from graph.state import GraphState

def test_intent_router_doctalk():
    state: GraphState = {
        "messages": [HumanMessage(content="Explain the HR policy")],
        "next_worker": None,
        "supervisor_reason": None
    }
    result = run_intent_router(state)
    assert result["next_worker"] == "doctalk"

def test_intent_router_dbtalk():
    state: GraphState = {
        "messages": [HumanMessage(content="Show all employees in the database")],
        "next_worker": None,
        "supervisor_reason": None
    }
    result = run_intent_router(state)
    assert result["next_worker"] == "dbtalk"

def test_intent_router_summary():
    state: GraphState = {
        "messages": [HumanMessage(content="Summarize this chat so far")],
        "next_worker": None,
        "supervisor_reason": None
    }
    result = run_intent_router(state)
    assert result["next_worker"] == "summary"

def test_intent_router_fallback():
    # Ambiguous queries should default to doctalk
    state: GraphState = {
        "messages": [HumanMessage(content="Hello there")],
        "next_worker": None,
        "supervisor_reason": None
    }
    result = run_intent_router(state)
    assert result["next_worker"] == "doctalk"
