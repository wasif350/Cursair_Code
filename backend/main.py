# from fastapi import FastAPI, WebSocket, HTTPException
# from pydantic import BaseModel
# from anthropic import AsyncAnthropic
# import uvicorn
# import subprocess
# from typing import List
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Add CORS middleware to allow requests from any origin (Can specify if necessary)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Update this list with the frontend URL if necessary
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Configure Anthropic API key
# client = AsyncAnthropic(
#     api_key=
#     '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'
# )


# # Request Schemas
# class CodeRequest(BaseModel):
#     prompt: str
#     language: str


# class CodeOptimizeRequest(BaseModel):
#     code: str


# class CodeExplainRequest(BaseModel):
#     code: str


# class CodeDebugRequest(BaseModel):
#     code: str


# class CodeTestRequest(BaseModel):
#     code: str


# class ProjectSummaryRequest(BaseModel):
#     activities: List[str]


# # Helper function to generate Claude response
# async def get_claude_response(prompt: str):
#     try:
#         response = await client.completions.create(
#             model="claude-3-sonnet-20240229",
#             prompt=prompt,
#             max_tokens_to_sample=1024)
#         return response.completion
#     except Exception as e:
#         print("An error occurred while generating the response.")
#         print(f"Error details: {str(e)}")
#         return f"Error generating response: {str(e)}"


# # Add a root endpoint
# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the AI Code Assistant API!"}


# # Endpoints for code generation, optimization, explanation, debugging, etc.
# @app.post("/generate_code/")
# async def generate_code(request: CodeRequest):
#     print(f"Received request: {request}")
#     prompt = f"Write {request.language} code for the following prompt: {request.prompt}"
#     return {"code": await get_claude_response(prompt)}


# @app.post("/optimize_code/")
# async def optimize_code(request: CodeOptimizeRequest):
#     prompt = f"Optimize the following code for readability and performance:\n{request.code}"
#     return {"optimized_code": await get_claude_response(prompt)}


# @app.post("/explain_code/")
# async def explain_code(request: CodeExplainRequest):
#     prompt = f"Explain the following code in simple terms:\n{request.code}"
#     return {"explanation": await get_claude_response(prompt)}


# @app.post("/debug_code/")
# async def debug_code(request: CodeDebugRequest):
#     try:
#         with open("temp_debug_code.py", "w") as file:
#             file.write(request.code)
#         result = subprocess.run(["python", "temp_debug_code.py"],
#                                 capture_output=True,
#                                 text=True)
#         return {"output": result.stdout, "error": result.stderr}
#     except Exception as e:
#         print(f"Error debugging code: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.post("/generate_unit_tests/")
# async def generate_unit_tests(request: CodeTestRequest):
#     prompt = f"Write unit tests for the following code:\n{request.code}"
#     return {"unit_tests": await get_claude_response(prompt)}


# @app.post("/project_summary/")
# async def project_summary(request: ProjectSummaryRequest):
#     activities_summary = "\n".join(request.activities)
#     prompt = f"Provide a project summary for the following activities:\n{activities_summary}"
#     return {"summary": await get_claude_response(prompt)}


# # WebSocket for real-time collaboration
# @app.websocket("/ws/{session_id}")
# async def websocket_endpoint(websocket: WebSocket, session_id: str):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message received: {data}")
#     except Exception as e:
#         print(f"Error with WebSocket communication: {str(e)}")
#         await websocket.close()


# # Run the backend server
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)



from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from pydantic import BaseModel
import google.generativeai as genai
import asyncio
import uvicorn
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from any origin (Can specify if necessary)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini API
genai.configure(api_key='AIzaSyAnfEvhg0Uz6Oahgvyoyy1FLGIWKzd6LhI')
model = genai.GenerativeModel('gemini-1.5-flash')

# Request Schemas
class CodeRequest(BaseModel):
    prompt: str
    language: str

class CodeOptimizeRequest(BaseModel):
    code: str

class CodeExplainRequest(BaseModel):
    code: str

class CodeDebugRequest(BaseModel):
    code: str

class CodeTestRequest(BaseModel):
    code: str

class ProjectSummaryRequest(BaseModel):
    activities: List[str]

# Helper function to generate Gemini response
async def get_claude_response(prompt: str):
    try:
        # Use asyncio to run the synchronous Gemini API call in a separate thread
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
        return response.text
    except Exception as e:
        print("An error occurred while generating the response.")
        print(f"Error details: {str(e)}")
        return f"Error generating response: {str(e)}"

# Add a root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Code Assistant API!"}

# Endpoints for code generation, optimization, explanation, debugging, etc.
@app.post("/generate_code/")
async def generate_code(request: CodeRequest):
    print(f"Received request: {request}")
    prompt = f"Write {request.language} code for the following prompt: {request.prompt}"
    return {"code": await get_claude_response(prompt)}

@app.post("/optimize_code/")
async def optimize_code(request: CodeOptimizeRequest):
    prompt = f"Optimize the following code for readability and performance:\n{request.code}"
    return {"optimized_code": await get_claude_response(prompt)}

@app.post("/explain_code/")
async def explain_code(request: CodeExplainRequest):
    prompt = f"Explain the following code in simple terms:\n{request.code}"
    return {"explanation": await get_claude_response(prompt)}

@app.post("/debug_code/")
async def debug_code(request: CodeDebugRequest):
    try:
        # Prepare the prompt for the AI model
        prompt = f"""Analyze the following code for issues and suggest improvements:

{request.code}

Please provide:
1. A list of identified issues
2. Suggestions for fixing each issue
3. An updated version of the code with key changes highlighted

Format your response as follows:
ISSUES:
[List of issues]

SUGGESTIONS:
[Suggestions for each issue]

UPDATED CODE:
[Updated code with key changes highlighted]
"""

        # Get response from the AI model
        ai_response = await get_claude_response(prompt)

        return {"result": ai_response}

    except Exception as e:
        print(f"Error debugging code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_unit_tests/")
async def generate_unit_tests(request: CodeTestRequest):
    prompt = f"Write unit tests for the following code:\n{request.code}"
    return {"unit_tests": await get_claude_response(prompt)}

@app.post("/project_summary/")
async def project_summary(request: ProjectSummaryRequest):
    activities_summary = "\n".join(request.activities)
    prompt = f"Provide a project summary for the following activities:\n{activities_summary}"
    return {"summary": await get_claude_response(prompt)}

# WebSocket management for real-time collaboration
active_connections: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    if session_id not in active_connections:
        active_connections[session_id] = []
    active_connections[session_id].append(websocket)

    try:
        while True:
            # Receive data from the WebSocket
            data = await websocket.receive_text()
            print(f"Received message from session {session_id}: {data}")

            # Broadcast the received message to all connected clients in the same session
            await broadcast_message(session_id, data)

    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
        active_connections[session_id].remove(websocket)
        if not active_connections[session_id]:
            del active_connections[session_id]

    except Exception as e:
        print(f"Error with WebSocket communication: {str(e)}")
        await websocket.close()

async def broadcast_message(session_id: str, message: str):
    """Broadcasts a message to all active connections in a given session."""
    if session_id in active_connections:
        for connection in active_connections[session_id]:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {str(e)}")

# Run the backend server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
