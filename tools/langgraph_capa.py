from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

from tools.chains import SummarizeChain, ClassifyChain, SuggestChain, RagSummarizeRunnable
from typing import TypedDict

class CAPAState(TypedDict):
    text: str
    summary: str
    root_cause: str
    corrective: str
    preventive: str

# Instantiate chains (assuming these are already LLMChain objects)
summarize_chain = RagSummarizeRunnable()
classify_chain = ClassifyChain
suggest_chain = SuggestChain

def summarize_node(state):
    summary =  summarize_chain.invoke({"text": state["text"]})["summary"]
    return {**state, "summary": summary}

def classify_node(state):
    root_cause = classify_chain.run(state["summary"])
    return {**state, "root_cause": root_cause}

def suggest_node(state):
    suggestions_text = suggest_chain.run(state["root_cause"])
    import json
    try:
        suggestions = json.loads(suggestions_text)
    except Exception:
        # fallback if parsing fails
        suggestions = {"corrective": suggestions_text, "preventive": suggestions_text}

    return {
        **state,
        "corrective": suggestions.get("corrective", ""),
        "preventive": suggestions.get("preventive", "")
    }

def build_capa_workflow_graph():
    builder = StateGraph(CAPAState)

    builder.add_node("summarize_deviation", RunnableLambda(summarize_node))
    builder.add_node("classify_root_cause", RunnableLambda(classify_node))
    builder.add_node("suggest_capa", RunnableLambda(suggest_node))

    builder.set_entry_point("summarize_deviation")
    builder.add_edge("summarize_deviation", "classify_root_cause")
    builder.add_edge("classify_root_cause", "suggest_capa")
    builder.add_edge("suggest_capa", END)

    return builder.compile()
