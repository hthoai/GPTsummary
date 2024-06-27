from typing import Any

import streamlit as st
from streamlit.components.v1 import html

from components.mermaid import DiagramGenerator


def mermaid(code: str) -> None:
    if "svg_height" not in st.session_state:
        st.session_state["svg_height"] = 1500

    html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=st.session_state["svg_height"] + 50,
    )


def mermaid_chart(code: str):
    html(
        f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css">
        <div class="mermaid">{code}</div>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
        """,
        height=1000,
        scrolling=True,
    )


def show_diagram(llm: Any, language: str, text: str):
    """
    Show the diagram for the given text.

    Args:
        llm (Any): The language model used for generating the diagram.
        language (str): The language to use for generating the diagram.
        text (str): The text to generate the diagram for.
    """
    generator = DiagramGenerator(
        llm=llm,
        language=language,
        examples_filepath="resources/mermaid_examples.json",
    )
    graph = generator.build_graph()
    state = {"text": text}
    show_type = True
    for event in graph.stream(state):
        state.update(event)
        if show_type and "analyze_text" in state:
            diagram_type = state["analyze_text"]["diagram_type"]
            st.markdown(f"Chosen Diagram Type: **{diagram_type}**")
            show_type = False
        if "generate_mermaid_code" in state:
            mermaid_code = state["generate_mermaid_code"]["mermaid_code"]
            with st.expander("See Mermaid code:"):
                st.markdown(mermaid_code)
            mermaid_code = mermaid_code.replace("`", "").lstrip("\n").lstrip("mermaid")

    try:
        # mermaid(mermaid_code)
        mermaid_chart(mermaid_code)
    except Exception as e:
        st.error(f"Failed to render the diagram. Please try again. Error:\n{e}")
