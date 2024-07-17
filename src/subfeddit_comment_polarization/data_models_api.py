from pydantic import BaseModel
from typing import List, Optional

class Comment(BaseModel):
    """
    Represents a single comment with its sentiment analysis.

    Attributes:
        id (int): The unique identifier of the comment.
        text (str): The text of the comment.
        polarity (float): The polarity score of the comment.
        classification (str): The classification of the comment (positive or negative).
    """
    id: int
    text: str
    polarity: float
    classification: str

class CommentsRequest(BaseModel):
    """
    Represents a request to fetch and analyze comments from a subfeddit.

    Attributes:
        subfeddit_name (str): The name of the subfeddit.
        start_time (Optional[str]): The start time for filtering comments.
        end_time (Optional[str]): The end time for filtering comments.
        sort_by_polarity (Optional[bool]): Whether to sort the comments by polarity.
    """
    subfeddit_name: str
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    sort_by_polarity: Optional[bool] = False

class CommentsResponse(BaseModel):
    """
    Represents the response containing analyzed comments.

    Attributes:
        comments (List[Comment]): A list of analyzed comments.
    """
    comments: List[Comment]
