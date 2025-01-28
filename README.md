# MANTLE-ECO-AI-AGENT

This repository contains an AI agent built using FastAPI and the Phidata framework designed to answer Mantle Protocol-related technical questions. The agent leverages various tools, including custom Web3 functionality, to provide accurate and relevant information. The system uses caching to speed up responses and remembers previous conversations to offer a more context-aware experience.

## Project Overview

The Mantle Ecosystem Specialist AI Agent is a powerful assistant for developers and users working with the **Mantle Protocol**. This AI agent can answer a variety of technical questions related to the Mantle ecosystem, retrieve real-time blockchain data, and provide detailed code samples from Mantle's GitHub repositories.

### Key Features:
- **Mantle Protocol Expertise**: The agent specializes in technical queries related to the Mantle protocol.
- **Web3 Integration**: The agent can fetch real-time blockchain data, such as wallet balances, transaction details, and block information.
- **Caching**: The system caches responses to speed up repeated queries, improving efficiency and reducing latency.
- **Context Awareness**: The bot remembers previous conversations within a session, ensuring that follow-up questions are answered with proper context.
- **Custom Web3 Tools**: The agent integrates with Ethereum-compatible networks via Web3, providing live data and interactions.

## Tools

### 1. **Phi Framework**:
   The Phi framework is utilized to manage workflows, storage, and logging in the agent. It allows for seamless integration of multiple tools and services, enabling the agent to perform various actions based on user queries.

### 2. **OpenAI GPT-4**:
   OpenAI's GPT-4 is used as the conversational model. It handles natural language understanding, response generation, and context handling.

### 3. **Web3 Tools**:
   The `Web3Tools` class integrates with the Ethereum blockchain via the Web3 library. This class provides several functions to interact with blockchain data.

   #### Functions:
   - **get_balance(address: str)**: 
     Fetches the balance of an Ethereum address and returns it in ETH.
     ```python
     # Example usage:
     web3_tools.get_balance("0xAddress")
     ```

   - **get_transaction(tx_hash: str)**: 
     Retrieves the details of a transaction by its hash.
     ```python
     # Example usage:
     web3_tools.get_transaction("0xTransactionHash")
     ```

   - **get_block(block_identifier: str)**: 
     Retrieves details of a specific block by its number or hash.
     ```python
     # Example usage:
     web3_tools.get_block("0xBlockHash")
     ```

### 4. **TavilyTools**:
   This tool provides additional functionality related to online searches, helping the bot gather information from the web to provide answers. The bot searches for the top 3 relevant links and scrapes content from them.

### 5. **Crawl4aiTools**:
   This tool enables the agent to crawl the web and collect information from a broader range of sources, providing the bot with the ability to answer a wide array of questions beyond just the information in its training data.

## How the Bot Works

### Memory and Context
The agent remembers previous interactions within the same session. It stores conversations in the `conversation_history`, so if you ask a follow-up question, the agent uses the context of your prior question and answer to generate a more relevant response.

### Caching for Speed
To improve response times, the agent caches answers to previously asked questions. If a user asks the same question during the session, the agent can return the cached response, significantly speeding up the process.

Caching is implemented by storing responses in a dictionary, keyed by the query. If a cached response is found, it is returned immediately, otherwise, the agent performs the usual query processing.

## Endpoints

### 1. **POST /ask**
   - **Description**: This endpoint is used to ask the bot a technical question about the Mantle protocol.
   - **Request Body**: 
     ```json
     {
       "query": "What is the Mantle Protocol?",
       "session_id": "your-session-id"
     }
     ```
   - **Response**:
     - **session_id**: The unique session ID for tracking conversations.
     - **response**: The bot's response to the query.
   - **Example**:
     ```bash
     curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"query": "What is the Mantle Protocol?", "session_id": "12345"}'
     ```

### 2. **GET /sessions**
   - **Description**: Lists all active sessions.
   - **Response**:
     ```json
     {
       "sessions": ["session-id-1", "session-id-2"]
     }
     ```

### 3. **DELETE /session/{session_id}**
   - **Description**: Deletes a session by its ID.
   - **Response**:
     ```json
     {
       "message": "Session session-id-1 deleted."
     }
     ```

## Benefits of the Project

- **Real-Time Blockchain Data**: Integrates with Web3, providing real-time information directly from the blockchain, such as wallet balances, transaction histories, and block details.
- **Improved Efficiency**: By caching responses, the agent provides faster responses to repeated queries, reducing the load on the system.
- **Context-Aware**: The agent's memory ensures that follow-up questions can reference previous interactions, providing a more seamless conversational experience.
- **Customizable**: The system is highly extensible, allowing for the addition of more tools and functionality to support a wider range of queries.
