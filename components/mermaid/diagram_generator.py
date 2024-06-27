import json
from typing import Any, Dict, Optional

from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import END, StateGraph
from loguru import logger


class DiagramTypeOutput(BaseModel):
    diagram_type: str = Field(
        description="The type of diagram",
        enum=[
            "Flowchart",
            "Block Diagram",
            "C4 Diagram",
            "Class Diagram",
            "Entity Relationship Diagram",
            "Mindmap",
            "Sequence Diagram",
            "Timeline Diagram",
            "User Journey Diagram",
        ],
        examples={
            "Flowchart": "A diagram that represents a process or workflow.",
            "Block Diagram": "A diagram that shows the main parts or functions of a system.",
            "C4 Diagram": "A diagram that shows the context, containers, components, and code of a system.",
            "Class Diagram": "A diagram that shows the classes in a system and their relationships.",
            "Entity Relationship Diagram": "A diagram that shows the entities in a system and their relationships.",
            "Mindmap": "A diagram that represents ideas and concepts branching from a central idea.",
            "Sequence Diagram": "A diagram that shows how objects interact in a particular sequence.",
            "Timeline Diagram": "A diagram that shows events in chronological order.",
            "User Journey Diagram": "A diagram that shows the steps a user takes to achieve a goal.",
        },
    )


class DiagramState(BaseModel):
    text: str
    diagram_type: Optional[str]
    mermaid_code: Optional[str]


class DiagramGenerator:
    def __init__(
        self,
        llm,
        language: str,
        examples_filepath: str,
    ) -> None:
        """
        Initialize the DiagramGenerator with the given language model, parser, and path to Mermaid examples.

        Args:
            llm (ChatGoogleGenerativeAI): The language model used for generating diagrams.
            language (str): The language to use for generating diagrams.
            examples_filepath (str): The path to the JSON file containing Mermaid examples.
        """
        self.llm = llm
        self.language = language
        self.load_mermaid_examples(filepath=examples_filepath)

    def load_mermaid_examples(self, filepath: str):
        """
        Load Mermaid examples from a JSON file.

        Args:
            filepath (str): The path to the JSON file containing Mermaid examples.

        Returns:
            Dict[str, Any]: A dictionary containing Mermaid examples.
        """
        with open(filepath, "r", encoding="utf-8") as file:
            self.mermaid_examples = json.load(file)
        with open("resources/flowchart.txt", "r", encoding="utf-8") as file:
            self.mermaid_examples["Flowchart"] = file.read()
            logger.info(f"Flowchart: {self.mermaid_examples['Flowchart']}")

    def analyze_text(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the text to decide the most suitable type of diagram.

        Args:
            state (Dict[str, Any]): The current state containing the text to be analyzed.

        Returns:
            Dict[str, Any]: The updated state with the chosen diagram type.
        """
        parser = PydanticOutputParser(pydantic_object=DiagramTypeOutput)
        prompt = PromptTemplate(
            template="You are a highly skilled visual content generator. Based on the following text, determine the most suitable type of diagram to visually represent the information.\n{format_instructions}\n{text}\n",
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.llm | parser
        output = chain.invoke({"text": state.text})
        logger.info(f"Chain output: ({type(output)}) {output}")
        diagram_type = output.diagram_type
        logger.info(f"Diagram type: {diagram_type}")
        diagram_type = (
            diagram_type if diagram_type in self.mermaid_examples else "Mindmap"
        )

        return {"diagram_type": diagram_type}

    def generate_mermaid_code(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate the Mermaid code based on the diagram type.

        Args:
            state (Dict[str, Any]): The current state containing the text and diagram type.

        Returns:
            Dict[str, Any]: The updated state with the generated Mermaid code.
        """
        diagram_type = state.diagram_type
        example_usage = self.mermaid_examples.get(
            diagram_type, "Example not found for the specified diagram type."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert in Mermaid diagramming. Your task is to generate Mermaid code for a {diagram_type} diagram based on the provided summary text. The summary may include an introduction and conclusion, but focus only on the key information for the visual representation.",
                ),
                (
                    "user",
                    "**Instructions:**\n"
                    "1. Extract and summarize the core information necessary for the diagram.\n"
                    "2. Generate concise and accurate Mermaid code that reflects the main points.\n"
                    '3. Enclose text component in quotation marks ""\n'
                    "4. Name all subgraphs for using later.\n"
                    "5. Always use the vertical direction (TD) if possible.\n"
                    "6. Use {language} language to generate the content of the diagram.\n"
                    "**Text:**\n"
                    "{text}\n"
                    "**Example Usage:**\n"
                    "{example_usage}",
                ),
            ]
        )
        parser = StrOutputParser()
        chain = prompt | self.llm | parser
        mermaid_code = chain.invoke(
            {
                "language": self.language,
                "text": state.text,
                "diagram_type": diagram_type,
                "example_usage": example_usage,
            }
        )

        return {"mermaid_code": mermaid_code}

    def build_graph(self) -> StateGraph:
        """
        Build the state graph for the diagram generation workflow.

        Returns:
            StateGraph: The compiled state graph.
        """
        workflow = StateGraph(DiagramState)
        workflow.add_node("analyze_text", self.analyze_text)
        workflow.add_node("generate_mermaid_code", self.generate_mermaid_code)
        workflow.set_entry_point("analyze_text")
        workflow.add_edge("analyze_text", "generate_mermaid_code")
        workflow.add_edge("generate_mermaid_code", END)

        return workflow.compile()
