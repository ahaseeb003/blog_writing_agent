from langgraph.graph import StateGraph, END
from blog_writing_agent.core.state import BlogState
from blog_writing_agent.agents.planning import PlanningAgents
from blog_writing_agent.agents.execution import ExecutionAgents
from blog_writing_agent.agents.review import ReviewAgents

def create_blog_graph():
    planning = PlanningAgents()
    execution = ExecutionAgents()
    review = ReviewAgents()
    
    workflow = StateGraph(BlogState)
    
    # Add Nodes
    workflow.add_node("router", planning.router_node)
    workflow.add_node("planner", planning.planner_node)
    workflow.add_node("researcher", execution.research_agent)
    workflow.add_node("writer", execution.writer_agent)
    workflow.add_node("imager", execution.image_agent)
    workflow.add_node("reviewer", review.reviewer_agent)
    workflow.add_node("editor", review.final_editor_agent)
    
    # Define Edges
    workflow.set_entry_point("router")
    workflow.add_edge("router", "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "imager")
    workflow.add_edge("imager", "reviewer")
    workflow.add_edge("reviewer", "editor")
    workflow.add_edge("editor", END)
    
    return workflow.compile()
