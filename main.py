from tools.langgraph_capa import build_capa_workflow_graph
import streamlit as st

def main():
    st.title("CAPA Deviation Reasoning Agent with LangChain + LangGraph")

    user_input = st.text_area("Paste Deviation Report Here")

    if st.button("Run CAPA Workflow"):
        if not user_input.strip():
            st.warning("Please enter deviation report text.")
            return

        workflow = build_capa_workflow_graph()  # returns compiled graph (Runnable)

        initial_state = {"text": user_input}
        result = workflow.invoke(initial_state)  # run workflow passing initial state dict

        st.markdown("### Summary:")
        st.write(result["summary"])

        st.markdown("### Root Cause Classification:")
        st.write(result["root_cause"])

        st.markdown("### Corrective Action:")
        st.write(result["corrective"])

        st.markdown("### Preventive Action:")
        st.write(result["preventive"])

if __name__ == "__main__":
    main()
