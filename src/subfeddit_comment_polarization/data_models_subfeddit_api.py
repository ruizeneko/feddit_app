from pydantic import BaseModel
from typing import List, Optional

class CommentInfo(BaseModel):
    """
    Represents a single comment's information.

    Attributes:
        id (int): The unique identifier of the comment.
        username (str): The username of the commenter.
        text (str): The text of the comment.
        created_at (int): The timestamp when the comment was created.
    """
    id: int
    username: str
    text: str
    created_at: int

class CommentsResponse(BaseModel):
    """
    Represents the response containing comments information.

    Attributes:
        subfeddit_id (int): The unique identifier of the subfeddit.
        limit (Optional[int]): The limit for the number of comments.
        skip (Optional[int]): The number of comments to skip.
        comments (List[CommentInfo]): A list of comments information.
    """
    subfeddit_id: int
    limit: int = 10
    skip: int = 0
    comments: List[CommentInfo]

class SubfedditInfo(BaseModel):
    """
    Represents information about a subfeddit.

    Attributes:
        id (int): The unique identifier of the subfeddit.
        username (str): The username of the subfeddit creator.
        title (str): The title of the subfeddit.
        description (str): The description of the subfeddit.
    """
    id: int
    username: str
    title: str
    description: str

class SubfedditResponse(BaseModel):
    """
    Represents the response containing subfeddit information.

    Attributes:
        limit (Optional[int]): The limit for the number of subfeddits.
        skip (Optional[int]): The number of subfeddits to skip.
        subfeddits (List[SubfedditInfo]): A list of subfeddit information.
    """
    limit: Optional[int] = 10
    skip: Optional[int] = 0
    subfeddits: List[SubfedditInfo]
