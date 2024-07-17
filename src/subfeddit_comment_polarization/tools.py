from fastapi import HTTPException
from transformers.pipelines import Pipeline
import requests
from typing import List, Tuple, Optional
from src.subfeddit_comment_polarization.data_models_subfeddit_api import SubfedditResponse, CommentsResponse, \
    CommentInfo
from src.subfeddit_comment_polarization.data_models_api import Comment

def get_subfeddit_name_from_id(feddit_api_url: str, subfeddit_name: str) -> int:
    """
    Fetches the subfeddit ID given its name.

    Args:
        feddit_api_url (str): The base URL of the Feddit API.
        subfeddit_name (str): The name of the subfeddit.

    Returns:
        int: The ID of the subfeddit.

    Raises:
        HTTPException: If there is an error fetching the subfeddits or the subfeddit does not exist.
    """
    response = requests.get(f"{feddit_api_url}/subfeddits")
    if response.status_code == 200:
        subfeddits_lst = SubfedditResponse(**response.json()).subfeddits
    else:
        raise HTTPException(status_code=500, detail="Error fetching subfeddits")

    for element in subfeddits_lst:
        if element.title == subfeddit_name:
            return element.id

    raise HTTPException(status_code=500, detail="Subfeddit does not exist")

def analyze_sentiment(comment_text: str, sentiment_analysis: Pipeline) -> Tuple[float, str]:
    """
    Analyzes the sentiment of the given comment text.

    Args:
        comment_text (str): The text of the comment.
        sentiment_analysis (Pipeline): The sentiment analysis pipeline.

    Returns:
        Tuple[float, str]: The polarity score and classification of the comment.
    """
    result = sentiment_analysis(comment_text)[0]
    polarity = result['score'] if result['label'] == 'POSITIVE' else -result['score']
    classification = result['label'].lower()
    return polarity, classification

def get_comments(subfeddit_name: str,
                 feddit_api_url: str,
                 start_date: Optional[int] = None,
                 end_date: Optional[int] = None) -> CommentsResponse:
    """
    Fetches comments from the specified subfeddit.

    Args:
        subfeddit_name (str): The name of the subfeddit.
        feddit_api_url (str): The base URL of the Feddit API.
        start_date (Optional[int]): The start date for filtering
        end_date (Optional[int]): The end date for filtering


    Returns:
        CommentsResponse: The response containing comments fetched from the subfeddit.

    Raises:
        HTTPException: If there is an error fetching the comments.
    """
    subfeddit_id = get_subfeddit_name_from_id(feddit_api_url, subfeddit_name)
    response = requests.get(f"{feddit_api_url}/comments/?subfeddit_id={subfeddit_id}")
    if response.status_code == 200:
        if not start_date or not end_date:
            return CommentsResponse(**response.json())

        comment_response_object = CommentsResponse(**response.json())
        filtered_comments = filter_comments(start_date, end_date, comment_response_object.comments)

        print(CommentsResponse(subfeddit_id=comment_response_object.subfeddit_id,
                                                       limit=comment_response_object.limit,
                                                       skip=comment_response_object.skip,
                                                       comments=filtered_comments))
        return CommentsResponse(subfeddit_id=comment_response_object.subfeddit_id,
                                                       limit=comment_response_object.limit,
                                                       skip=comment_response_object.skip,
                                                       comments=filtered_comments)
    else:
        raise HTTPException(status_code=500, detail="Error fetching comments")

def analyze_comments_sentiment(comments_data_lst: CommentsResponse,
                               sentiment_analysis_pipeline: Pipeline,
                               limit: int = 25) -> List[Comment]:
    """
    Analyzes the sentiment of a list of comments.

    Args:
        comments_data_lst (CommentsResponse): The response containing comments data.
        sentiment_analysis_pipeline (Pipeline): The sentiment analysis pipeline.
        limit (int): The limit on the number of comments to analyze.

    Returns:
        List[Comment]: A list of comments with their sentiment analysis.
    """
    analyzed_comments_lst: List[Comment] = []
    for comment in comments_data_lst.comments[:limit]:
        polarity, classification = analyze_sentiment(comment.text, sentiment_analysis_pipeline)
        analyzed_comments_lst.append(
            Comment(
                id=comment.id,
                text=comment.text,
                polarity=polarity,
                classification=classification
            )
        )
    print(analyzed_comments_lst)
    return analyzed_comments_lst

def do_filtering(start_date: float, end_date: float, comment: CommentInfo) -> bool:
    if start_date <= comment.created_at < end_date:
        return True
    return False

def filter_comments(start_date: float, end_date: float, comments_lst: List[CommentInfo]) -> List[CommentInfo]:
    filtered_comments: List[CommentInfo] = []
    for comment in comments_lst:
        if do_filtering(start_date, end_date, comment):
            filtered_comments.append(comment)
    return filtered_comments