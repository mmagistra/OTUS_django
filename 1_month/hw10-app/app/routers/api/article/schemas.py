from typing import Any, Annotated

from fastapi import Form
from pydantic import BaseModel


class CreateFormData():
    def __init__(
            self,
            title: Annotated[str, Form()],
            subtitle: Annotated[str, Form()],
            text: Annotated[str, Form()],
            tags: Annotated[list, Form()] = None,
    ):
        if tags is None:
            tags = []
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.tags = tags
        # print('Create data:', title, subtitle, text, tags)


class DeleteFormData():
    def __init__(
            self,
            post_id: Annotated[int, Form()],
            author_id: Annotated[int, Form()]
    ):
        self.post_id = post_id
        self.author_id = author_id
