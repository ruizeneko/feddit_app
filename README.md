
# Subfeddit Comment Polarization

## Overview

This project provides an API endpoint (`/comments`) that fetches comments from a specified subfeddit, analyzes their sentiment using a pre-trained model, and optionally filters and sorts the comments based on provided criteria.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd subfeddit-comment-polarization
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

To start the FastAPI server, navigate to `src/main` and run:

```bash
python main.py
```

The server will start at `http://localhost:8081`.

### Endpoint (`/comments`)

#### Request

- **Method:** POST
- **URL:** `/comments`
- **Request Body:**

```json
{
  "subfeddit_name": "string",
  "start_time": "string",
  "end_time": "string",
  "sort_by_polarity": "boolean"
}
```

- **Parameters:**
  - `subfeddit_name` (required): The name of the subfeddit from which to fetch comments.
  - `start_time` (optional): Start time for filtering comments (timestamp).
  - `end_time` (optional): End time for filtering comments (timestamp).
  - `sort_by_polarity` (optional): Whether to sort comments by polarity (boolean).

#### Response

- **Status Codes:**
  - `200 OK`: Successful operation. Returns analyzed comments.
  - `422 Unprocessable Entity`: Invalid request data.

- **Response Body:**

```json
{
  "comments": [
    {
      "id": 1,
      "text": "string",
      "polarity": "float",
      "classification": "string"
    },
    {
      "id": 2,
      "text": "string",
      "polarity": "float",
      "classification": "string"
    }
  ]
}
```

- **Attributes:**
  - `id`: Unique identifier of the comment.
  - `text`: Text of the comment.
  - `polarity`: Sentiment polarity score.
  - `classification`: Sentiment classification (positive/negative).

### Dependencies

- `FastAPI`: Web framework for building APIs with Python.
- `Transformers`: Library for natural language processing using pre-trained models.
- `Pydantic`: Data validation and settings management using Python type annotations.
- `Requests`: HTTP library for making API requests.

## Testing

Unit tests are provided to validate the functionality of the `/comments` endpoint. Use `pytest` to run the tests:

```bash
pytest
```
