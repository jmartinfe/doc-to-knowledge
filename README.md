# Doc to Knowledge
An API to ingest documents and convert them into a categorized knowledge base for easy querying.

## Features
Given a document, will extract the text and use the font format to determine the document structure categories as well as the knowledge categories.
This categories will be stored and made available to be queried by other systems.

## Setup
**Clone the repository and navigate into the project directory.**

**Create and activate a virtual environment:**
```
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

**Install dependencies:**
```
pip install -r requirements.txt
```

**Environment Variables:**
Create a `.env` file in the root directory based on the example below:
    ```
    API_KEY=your-internal-api-key
    ALLOWED_ORIGINS=http://localhost:5500,https://your-frontend.vercel.app
    ENVIRONMENT=development
    LOG_LEVEL=INFO
    APP_TITLE=Doc to Knowledge API
    ```

**Create your system prompt file at data/system_prompt.txt with your agent instructions.**

## Running the Application
Start the development server with Uvicorn:
uvicorn main:app --reload

Access the interactive API documentation at http://127.0.0.1:8000/docs

## API Endpoints
Section pending to complete

## License
MIT