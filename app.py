from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import uuid
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.log import logger
from mantle_agent import MantleAgentWorkflow
from fastapi.middleware.cors import CORSMiddleware



# Initialize FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)



session_workflows: Dict[str, MantleAgentWorkflow] = {}

# User query model
class UserQuery(BaseModel):
    query: str
    session_id: str = None

@app.post("/ask")
def ask_question(user_query: UserQuery):
    """
    Endpoint to handle user queries.
    """
    # Generate a new session ID if not provided
    if not user_query.session_id:
        user_query.session_id = str(uuid.uuid4())

    # Initialize workflow for the session if it doesn't exist
    if user_query.session_id not in session_workflows:
        session_workflows[user_query.session_id] = MantleAgentWorkflow(
            session_id=user_query.session_id,
            storage=SqlWorkflowStorage(
                table_name="mantle_agent_workflows",
                db_file="mantle_agent_workflows.db",
            ),
        )

    # Get the workflow for the session
    workflow = session_workflows[user_query.session_id]

    # Process the query using the workflow
    responses = []
    for response in workflow.run(user_query.query):
        responses.append(response.content)

    return {
        "session_id": user_query.session_id,
        "response": "\n".join(responses),
    }

@app.get("/sessions")
def list_sessions():
    """
    Endpoint to list all active sessions.
    """
    return {"sessions": list(session_workflows.keys())}

@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    """
    Endpoint to delete a session.
    """
    if session_id in session_workflows:
        del session_workflows[session_id]
        return {"message": f"Session {session_id} deleted."}
    else:
        raise HTTPException(status_code=404, detail="Session not found.")
