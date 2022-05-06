from typing import Dict, List


BASE_TAG = r'<meta property="{property}" content="{content}" />'

def generate_opengraph_tag(prop: str, content: str) -> str:
    prop = "og:" + prop
    
    tag = BASE_TAG.format(
        property=prop,
        content=content
    )

    return tag

def generate_tags_from_dict(properties: Dict[str, str]) -> List[str]:
    tags = []

    for prop, content in properties.items():
        tag = generate_opengraph_tag(prop, content)
        tags.append(tag)

    return tags
