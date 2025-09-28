import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict

from gemini.client import A2AADKConnection

# Create router
router = APIRouter()

# Store active connections
connections: Dict[str, A2AADKConnection] = {}

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for real-time communication with Google A2A ADK API
    
    Args:
        websocket: WebSocket connection
        client_id: Unique client identifier
    """
    await websocket.accept()
    print(f"Client connected: {client_id}")

    # Create Google A2A ADK connection for this client
    a2a_adk = A2AADKConnection()
    connections[client_id] = a2a_adk

    try:
        # 1) The first message from front-end must be "config"
        initial_msg = await websocket.receive_json()
        if initial_msg.get("type") != "config":
            raise ValueError("First WebSocket message must be configuration.")
        
        # Extract and apply configuration
        config_data = initial_msg.get("config", {})
        a2a_adk.set_config(config_data)
        print(f"Received config for client {client_id}")

        # 2) Connect to Google A2A ADK (sends 'setup' message)
        await a2a_adk.connect()
        print(f"Google A2A ADK connected for client {client_id}")

        # 3) Start tasks: reading from client and reading from Google A2A ADK
        receive_task = asyncio.create_task(receive_from_client(websocket, a2a_adk, client_id))
        send_task = asyncio.create_task(send_to_frontend(websocket, a2a_adk))

        # Wait for either task to complete (or fail)
        done, pending = await asyncio.wait(
            [receive_task, send_task],
            return_when=asyncio.FIRST_EXCEPTION
        )
        
        # Cancel any pending tasks
        for task in pending:
            task.cancel()
            
        # Re-raise exceptions from completed tasks
        for task in done:
            if task.exception():
                raise task.exception()

    except WebSocketDisconnect:
        print(f"Client disconnected: {client_id}")
    except ValueError as e:
        print(f"Validation error for client {client_id}: {e}")
        await websocket.send_json({"type": "error", "message": str(e)})
    except Exception as e:
        print(f"Error in WebSocket handler for client {client_id}: {e}")
        try:
            await websocket.send_json({"type": "error", "message": f"Server error: {str(e)}"})
        except:
            pass
    finally:
        # Clean up resources
        await a2a_adk.close()
        if client_id in connections:
            del connections[client_id]
        
        print(f"Connection closed for client {client_id}")


async def receive_from_client(websocket: WebSocket, a2a_adk: A2AADKConnection, client_id: str = None):
    """
    Process incoming messages from the client browser
    
    Args:
        websocket: WebSocket connection
        a2a_adk: A2AADKConnection instance for this client
    """
    while True:
        try:
            # Receive WebSocket message
            message = await websocket.receive()
            
            # Handle disconnection
            if message["type"] == "websocket.disconnect":
                print("Client disconnected.")
                return
            
            # Parse the message content
            content = json.loads(message["text"])
            msg_type = content["type"]

            # Route to appropriate handler based on message type
            if msg_type == "audio":
                # Send to Google A2A ADK for response generation
                await a2a_adk.send_audio(content["data"])
            elif msg_type == "image":
                # Send to Google A2A ADK
                await a2a_adk.send_image(content["data"])
            elif msg_type == "text":
                await a2a_adk.send_text(content["data"])
            elif msg_type == "interrupt":
                await a2a_adk.send_interrupt()
            else:
                print(f"Unknown message type from client: {msg_type}")

        except json.JSONDecodeError:
            print("Received invalid JSON from client")
        except KeyError as e:
            print(f"Missing required field in client message: {e}")
        except Exception as e:
            print(f"Error processing client message: {e}")
            break


async def send_to_frontend(websocket: WebSocket, a2a_adk: A2AADKConnection):
    """
    Forward Google A2A ADK responses to the client browser
    
    Args:
        websocket: WebSocket connection
        a2a_adk: A2AADKConnection instance for this client
    """
    while True:
        try:
            # Get next message from Google A2A ADK
            msg = await a2a_adk.receive()
            if not msg:
                continue

            # Parse response
            response = json.loads(msg)
            
            # Extract and forward parts (audio or text)
            try:
                parts = response["serverContent"]["modelTurn"]["parts"]
                for part in parts:
                    if "inlineData" in part:
                        # Audio data from Google A2A ADK (base64 PCM)
                        audio_data = part["inlineData"]["data"]
                        await websocket.send_json({"type": "audio", "data": audio_data})
                    elif "text" in part:
                        # Text from Google A2A ADK
                        text_data = part["text"]
                        print("Google A2A ADK text part:", text_data)
                        await websocket.send_json({"type": "text", "text": text_data})
            except KeyError:
                # Not all responses have parts
                pass

            # Handle turn completion
            try:
                if response["serverContent"]["turnComplete"]:
                    await websocket.send_json({"type": "turn_complete", "data": True})
            except KeyError:
                # Not all responses indicate turn completion
                pass

        except Exception as e:
            print(f"Error processing Google A2A ADK response: {e}")
            break
