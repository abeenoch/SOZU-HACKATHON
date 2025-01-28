import os
import typer
from mantle_agent import MantleAgentWorkflow
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from dotenv import load_dotenv

load_dotenv()
app =typer.Typer()
# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
PHI_API_KEY = os.getenv("PHI_API_KEY")

# Initialize the workflow
workflow = MantleAgentWorkflow(
    session_id="mantle_agent_session",
    storage=SqlWorkflowStorage(
        table_name="mantle_agent_workflows",
        db_file="mantle_agent_workflows.db",
    ),
)
@app.command()
def main():
    """
    Entry point for the CLI application.
    """
    while True:
        user_query = input("Ask your question about Mantle (or type 'exit' to quit): ")

        if user_query.lower() == 'exit':
            print("Exiting the session.")
            break  # Exit the loop

        # Run the workflow with the user's query
        for response in workflow.run(user_query):
            print(response.content)

if __name__ == "__main__":
    app()                               