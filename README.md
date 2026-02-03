AI Study Helper – Backend API (V1)
What is this project?

This is a V1 of a study helper backend API. It makes it easier to study a topic by taking the subject and difficulty level as input and generating an explanation adapted to that level. The project is built using FastAPI, integrates a local LLM via Ollama, and is designed to be extended later with more functionality such as RAG.

What problem does it solve?

Students often have to rely on multiple tools or LLM interfaces to study a topic and still struggle to get explanations that match their understanding level. This system solves that problem by providing a single structured API that adapts explanations based on the learner’s difficulty level, making studying more focused and accessible for students at any stage.

How do I run it locally?

To run the project locally, clone the repository and install the required Python dependencies from requirements.txt. Make sure Ollama is installed on your system and that the llama3 model is available. Once Ollama is running, start the FastAPI server by running main.py, and access the API through the provided endpoints.

What endpoints exist?

The API currently exposes a single endpoint.

POST /generate
This endpoint accepts a topic and difficulty level as input and returns an AI-generated explanation based on the provided parameters.

High-level architecture

A client sends a request containing a topic and difficulty level to a FastAPI endpoint. The input is validated using request schemas, after which the topic and level are passed to the service layer. The service layer is responsible for calling the LLM through Ollama and generating an explanation. The generated output is then sent back to the client wrapped inside a response schema.