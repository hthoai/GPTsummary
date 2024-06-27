import json

import requests

TYPE_LINK = {
    "Flowchart": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/flowchart.md",
    "Block Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/block.md",
    "C4 Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/c4.md",
    "Class Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/classDiagram.md",
    "Entity Relationship Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/entityRelationshipDiagram.md",
    "Mindmap": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/mindmap.md",
    "Sequence Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/sequenceDiagram.md",
    "Timeline Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/timeline.md",
    "User Journey Diagram": "https://raw.githubusercontent.com/mermaid-js/mermaid/develop/packages/mermaid/src/docs/syntax/userJourney.md",
}


def download_mermaid_examples():
    mermaid_example_dict = {}
    for mtype, url in TYPE_LINK.items():
        response = requests.get(url)
        if response.status_code == 200:
            mermaid_example_dict[mtype] = response.text
        else:
            raise Exception(f"Failed to download file from {url}")

    with open("resources/mermaid_examples.json", "w", encoding="utf-8") as f:
        json.dump(mermaid_example_dict, f, ensure_ascii=False)


if __name__ == "__main__":
    download_mermaid_examples()
