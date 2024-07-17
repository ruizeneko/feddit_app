from transformers import pipeline
from fastapi import FastAPI
import torch
from src.subfeddit_comment_polarization.data_models_api import CommentsResponse, CommentsRequest
from src.subfeddit_comment_polarization.tools import get_comments, analyze_comments_sentiment

from fastapi import HTTPException
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
sentiment_analysis_pipeline = pipeline("sentiment-analysis",
                                       model="distilbert-base-uncased-finetuned-sst-2-english",
                                       device=device)
app = FastAPI()
FEDDIT_API_URL = "http://localhost:8080/api/v1"

@app.post("/comments", response_model=CommentsResponse)
def comment(request: CommentsRequest) -> CommentsResponse:
    """
    Endpoint to fetch and analyze comments from a specified subfeddit.

    Args:
        request (CommentsRequest): The request containing subfeddit name and optional filters.

    Returns:
        CommentsResponse: The response containing analyzed comments.
    """

    # Filter comments by start_time and end_time if provided
    if request.start_time and request.end_time:
        try:
            start_time = int(request.start_time)
            end_time = int(request.end_time)
            if start_time > end_time:
                raise HTTPException(status_code=422,
                                    detail="Invalid date range: start_time must be less than or equal to end_time")

            comments_data = get_comments(request.subfeddit_name,
                                         FEDDIT_API_URL,
                                         start_date=request.start_time,
                                         end_date=request.end_time)
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid start_time or end_time format")

    else:
        comments_data = get_comments(request.subfeddit_name, FEDDIT_API_URL)

    # Check if comments_data is None or empty
    if not comments_data or not comments_data.comments or len(comments_data.comments) == 0:
        return CommentsResponse(comments=[])

    analyzed_comments = analyze_comments_sentiment(comments_data,
                                                   sentiment_analysis_pipeline=sentiment_analysis_pipeline)
    if not analyzed_comments:
        raise HTTPException(status_code=500, detail="Error analyzing comments or no comments analyzed")

    # Sort comments by polarity if requested
    if request.sort_by_polarity:
        analyzed_comments.sort(key=lambda x: x.polarity, reverse=True)

    return CommentsResponse(comments=analyzed_comments)
