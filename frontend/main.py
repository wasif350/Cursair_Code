import streamlit as st
import requests
import asyncio
import websockets

# Update this URL to match the backend's URL and port
BASE_URL = "https://af6ccaaf-6921-4850-91d7-0d98af7748b4-00-2l7zztr4ienub.riker.replit.dev:8000/"

WS_URL = "ws://af6ccaaf-6921-4850-91d7-0d98af7748b4-00-2l7zztr4ienub.riker.replit.dev:8000/ws"

# Streamlit App
st.title('Enhanced Code Editor')

def api_call(endpoint, data):
    """Helper function for making API calls."""
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error during API call to {endpoint}: {e}")
        return None

# Code Generation
st.header("Code Generator")
prompt = st.text_area("Enter prompt here...")
language = st.selectbox("Select language", ["python", "javascript"])
if st.button("Generate Code"):
    result = api_call("generate_code/", {"prompt": prompt, "language": language})
    if result:
        st.code(result.get("code", ""), language=language)

# Code Optimizer
st.header("Code Optimizer")
code_to_optimize = st.text_area("Enter code to optimize")
if st.button("Optimize Code"):
    result = api_call("optimize_code/", {"code": code_to_optimize})
    if result:
        st.code(result.get("optimized_code", ""), language="python")

# Code Explainer
st.header("Code Explainer")
code_to_explain = st.text_area("Enter code to explain")
if st.button("Explain Code"):
    result = api_call("explain_code/", {"code": code_to_explain})
    if result:
        st.write(result.get("explanation", ""))

# Collaboration
# st.header("Code Collaboration")
# session_id = st.text_input("Enter Collaboration Session ID")
# collab_input = st.text_input("Enter message to collaborate")

# # A place to display received collaboration messages
# if 'received_messages' not in st.session_state:
#     st.session_state.received_messages = []

# async def connect_and_receive(session_id):
#     """Function to receive messages from the WebSocket."""
#     uri = f"{WS_URL}/{session_id}"
#     try:
#         async with websockets.connect(uri) as websocket:
#             while True:
#                 response = await websocket.recv()
#                 st.session_state.received_messages.append(response)  # Store received messages
#                 st.experimental_rerun()  # Refresh the app to show new messages
#     except Exception as e:
#         st.error(f"Error receiving messages: {e}")

# async def send_ws_message(session_id, collab_input):
#     """Function to send messages through WebSocket."""
#     uri = f"{WS_URL}/{session_id}"
#     try:
#         async with websockets.connect(uri) as websocket:
#             await websocket.send(collab_input)
#             st.success(f"Message sent: {collab_inp
#                                 ut}")
#     except Exception as e:
#         st.error(f"Error sending collaboration message: {e}")

# # Start receiving messages when the user joins the collaboration
# if session_id and st.button("Join Collaboration"):
#     asyncio.run(connect_and_receive(session_id))

# if st.button("Send Collaboration Message"):
#     if session_id and collab_input:
#         asyncio.run(send_ws_message(session_id, collab_input))
#     else:
#         st.warning("Please enter a session ID and message.")

# # Display received messages
# if st.session_state.received_messages:
#     st.subheader("Received Collaboration Messages:")
#     for message in st.session_state.received_messages:
#         st.write(message)

# Debug Assistant
st.header("Debug Assistant")
debug_code = st.text_area("Enter code to debug")
if st.button("Debug Code"):
    result = api_call("debug_code/", {"code": debug_code})
    if result:
        issues_start = result['result'].find("ISSUES:")
        suggestions_start = result['result'].find("SUGGESTIONS:")
        updated_code_start = result['result'].find("UPDATED CODE:")

        if issues_start != -1:
            st.subheader("Issues Identified:")
            st.write(result['result'][issues_start:suggestions_start])

        if suggestions_start != -1:
            st.subheader("Suggestions:")
            st.write(result['result'][suggestions_start:updated_code_start])

        if updated_code_start != -1:
            st.subheader("Updated Code:")
            st.code(result['result'][updated_code_start:], language="python")

# Testing Assistance
st.header("Testing Assistant")
test_code = st.text_area("Enter code for which you need unit tests")
if st.button("Generate Unit Tests"):
    result = api_call("generate_code/", {"prompt": f"Write unit tests for the following code:\n{test_code}", "language": "python"})
    if result:
        st.code(result.get("code", ""), language="python")

# Educational Mode
st.header("Educational Mode")
edu_code = st.text_area("Enter code for educational explanation")
if st.button("Explain for Non-Technical Audience"):
    result = api_call("explain_code/", {"code": edu_code})
    if result:
        st.write("Educational Explanation: " + result.get("explanation", ""))
