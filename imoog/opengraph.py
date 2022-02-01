from typing import Dict, List


BASE_TAG = r'<meta property="{property}" content="{content}" />'

def generate_opengraph_tag(property: str, content: str) -> str:
    property = "og:" + property
    
    tag = BASE_TAG.format(
        property=property,
        content=content
    )

    return tag

def generate_tags_from_dict(properties: Dict[str, str]) -> List[str]:
    tags = []

    for property, content in properties.items():
        tag = generate_opengraph_tag(property, content)
        tags.append(tag)

    return tags