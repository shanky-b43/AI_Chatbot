import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from core.config import settings
from graph.state import GraphState
from loguru import logger
from router.schema import RouterOutput
from router.prompt import ROUTER_SYSTEM_PROMPT
from langchain_core.runnables import RunnableConfig

async def run_intent_router(state: GraphState, config: RunnableConfig) -> GraphState:
    """
    Router node that analyzes the user's intent and decides the target workflow.
    """
    logger.info("Executing Intent Router Node")
    messages = state.get("messages", [])
    if not messages:
        return {"next_worker": "FINISH", "supervisor_reason": "No messages found"}

    # Keyword Pre-Router for common greetings to save LLM roundtrips
    latest_msg = messages[-1].content.strip().lower()
    cleaned_msg = re.sub(r'[^\w\s]', '', latest_msg)
    
    greeting_keywords = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings", "sup", "howdy", "hiya"}
    
    if cleaned_msg in greeting_keywords:
        logger.info("Pre-router caught a simple greeting. Routing directly to conversation.")
        return {
            "next_worker": "conversation",
            "sub_node": None,
            "supervisor_reason": "Pre-router matched greeting."
        }

    # We use ChatOllama with the configured router model
    # Using with_structured_output to force Pydantic schema
    llm = ChatOllama(
        model=settings.ROUTER_MODEL,
        base_url=settings.OLLAMA_URL,
        temperature=0.0
    ).with_config({"tags": ["intent_router"]})
    
    # We use LangChain's structured output capability.
    structured_llm = llm.with_structured_output(RouterOutput)
    
    try:
        # Pass the router prompt and the conversation history
        invoke_messages = [SystemMessage(content=ROUTER_SYSTEM_PROMPT)] + messages
        decision: RouterOutput = await structured_llm.ainvoke(invoke_messages, config=config)
        
        target_node = decision.agent
        if decision.agent in ["finance", "hr", "it"] and decision.sub_node:
            target_node = f"{decision.agent}_{decision.sub_node.lower().replace(' ', '_').replace('&', 'and')}"
            
        logger.info(f"Workflow Router decided: Agent={decision.agent}, SubNode={decision.sub_node} -> Node={target_node}")
        
        return {
            "next_worker": target_node,
            "sub_node": decision.sub_node,
            "supervisor_reason": "Routing successful"
        }
    except Exception as e:
        logger.error(f"Workflow Router failed: {e}")
        # Default to conversation on failure
        return {
            "next_worker": "conversation",
            "sub_node": None,
            "supervisor_reason": f"Routing failed, defaulting to conversation. Error: {str(e)}"
        }
