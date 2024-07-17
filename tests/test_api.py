import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.subfeddit_comment_polarization.api import app

client = TestClient(app)

@pytest.fixture
def mock_get_comments():
    with patch('src.subfeddit_comment_polarization.tools.get_comments') as mock:
        yield mock

@pytest.fixture
def mock_analyze_comments_sentiment():
    with patch('src.subfeddit_comment_polarization.tools.analyze_comments_sentiment') as mock:
        yield mock

def test_comment_endpoint(mock_get_comments, mock_analyze_comments_sentiment):
    # Arrange
    mock_get_comments.return_value = {"subfeddit_id": 1,
                                      "limit": 2,
                                      "skip": 0,
                                      "comments": [{"id": 1, "username": "user_0", "text": "It looks great!",
                                                    "created_at": 1721226986},
                                                   {"id": 2, "username": "user_1", "text": "Love it.",
                                                    "created_at": 1721223386}]
}
    mock_analyze_comments_sentiment.return_value = [
        {"id": 8,"text": "Like it a lot!","polarity": 0.9998447895050049,"classification": "positive"},
        {"id": 9,"text": "Good work.","polarity": 0.9998396635055542,"classification": "positive"},
        {"id": 6,"text": "What you did was right.","polarity": 0.9997642636299133,"classification": "positive"},
        {"id": 7,"text": "Thumbs up.","polarity": 0.9996517896652222,"classification": "positive"}]

    payload = {
        "subfeddit_name": "Dummy Topic 1",
        "start_time": 1721212586,
        "end_time": 1721226987,
        "sort_by_polarity": "True"
    }

    # Act
    response = client.post("/comments", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"comments": [
        {"id": 8,"text": "Like it a lot!","polarity": 0.9998447895050049,"classification": "positive"},
        {"id": 9,"text": "Good work.","polarity": 0.9998396635055542,"classification": "positive"},
        {"id": 6,"text": "What you did was right.","polarity": 0.9997642636299133,"classification": "positive"},
        {"id": 7,"text": "Thumbs up.","polarity": 0.9996517896652222,"classification": "positive"}]
}

def test_comment_endpoint_invalid_dates(mock_get_comments, mock_analyze_comments_sentiment):
    # Arrange
    mock_get_comments.return_value = {"subfeddit_id": 1,
                                      "limit": 2,
                                      "skip": 0,
                                      "comments": [{"id": 1, "username": "user_0", "text": "It looks great!",
                                                    "created_at": 1721226986},
                                                   {"id": 2, "username": "user_1", "text": "Love it.",
                                                    "created_at": 1721223386}]
                                      }

    mock_analyze_comments_sentiment.return_value = [
        {"id": 8,"text": "Like it a lot!","polarity": 0.9998447895050049,"classification": "positive"},
        {"id": 9,"text": "Good work.","polarity": 0.9998396635055542,"classification": "positive"},
        {"id": 6,"text": "What you did was right.","polarity": 0.9997642636299133,"classification": "positive"},
        {"id": 7,"text": "Thumbs up.","polarity": 0.9996517896652222,"classification": "positive"}]

    payload = {
        "subfeddit_name": "Dummy Topic 1",
        "start_time": "1618318000",
        "end_time": "1618317000",
        "sort_by_polarity": True
    }

    # Act
    response = client.post("/comments", json=payload)

    # Assert
    assert response.status_code == 422  # or appropriate error handling