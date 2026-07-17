from typing import Dict, Any, Callable
from loguru import logger
from langgraph.graph import StateGraph

class WorkflowRegistry:
    """
    Registry pattern for dynamically instantiating workflows.
    """
    _workflows: Dict[str, Callable[[], StateGraph]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a workflow factory function."""
        def decorator(factory_func: Callable[[], StateGraph]):
            cls._workflows[name] = factory_func
            logger.debug(f"Registered workflow: {name}")
            return factory_func
        return decorator

    @classmethod
    def get_workflow(cls, name: str) -> StateGraph:
        """Retrieve and instantiate a workflow by name."""
        if name not in cls._workflows:
            logger.warning(f"Workflow '{name}' not found.")
            raise ValueError(f"Workflow '{name}' not found.")
        return cls._workflows[name]()

    @classmethod
    def list_workflows(cls) -> list[str]:
        return list(cls._workflows.keys())
        
    @classmethod
    def get_all_workflows(cls) -> Dict[str, StateGraph]:
        """Retrieve and instantiate all registered workflows."""
        return {name: factory() for name, factory in cls._workflows.items()}
