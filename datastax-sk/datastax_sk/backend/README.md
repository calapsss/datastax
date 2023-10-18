## DataStax API Backend
This backend application is designed to support the DataStax API for data processing and transformation. It utilizes the Semantic Kernel library and integrates with various AI services for chat completion and text embedding.

### Usage

#### Analyze DataFrame
- **Endpoint:** `/analyzeDataframe/`
 **Description:** Analyzes the provided DataFrame.
- **Method:** GET
- **Parameters:**
    - `dataframe` (string): The DataFrame to be analyzed.
- **Response:** The analysis result in string format.

#### Generate Questions

- **Endpoint:** `/generateQuestions/`
- **Description:** Generates questions based on the provided DataFrame.
- **Method:** GET
- **Parameters:**
    - `dataframe` (string): The DataFrame to generate questions from.
- **Response:** A list of questions generated as a JSON object.

#### Initialize Question-Query Pair

- **Endpoint:** `/initQuestionQueryPair/`
- **Description:** Initializes the question-query pair.
- **Method:** GET
- **Response:** The question-query pair in JSON format.

#### Simple Code Generation

- **Endpoint:** `/simpleCodeGeneration/`
- **Description:** Handles code generation and DataFrame transformation.
- **Method:** GET
- **Parameters:**
    - `dataframe` (string): The DataFrame to be transformed.
    - `prompt` (string): The prompt for code generation.
    - `code` (string): The code to be executed.
- **Response:** The transformation result as a JSON object.

### Setup

1. Set up Semantic Kernel API key and organization ID by creating a `.env` file with the following content:
     ```plaintext
     OPENAI_API_KEY=YOUR_OPENAI_API_KEY
     OPENAI_ORG_ID=YOUR_OPENAI_ORG_ID
     ```

2. Run the FastAPI application using:
     ```bash
     uvicorn your_app_name:app --host 0.0.0.0 --port 8000
     ```

Make sure to replace `YOUR_OPENAI_API_KEY` and `YOUR_OPENAI_ORG_ID` with your OpenAI API key and organization ID respectively.
