Directory structure:
└── lschirripa-capture-to-vlm/
    ├── README.md
    ├── LICENSE
    ├── client/
    │   ├── client.py
    │   ├── client_prompt_only.py
    │   ├── requirements.txt
    │   ├── summarize_video_audio.py
    │   └── utils/
    │       └── utils.py
    └── server/
        ├── requirements.txt
        └── server.py

================================================
FILE: README.md
================================================
# Real Time Video Analysis and Summarization System



This project provides a comprehensive system for analyzing real-time videos using Vision Language Models (VLM) and generating summaries of the content. The system works in two main phases: real-time frame analysis and post-processing summarization.

The server component uses Ollama to run the VLM and LLM models, providing real-time analysis and summarization capabilities.

## Demo

<!-- VLM Analysis Demo -->
*Real-time VLM analysis output from `client.py`*

![VLM Analysis Demo](docs/demos/vlm_analysis.gif)


<!-- Summarization Demo -->
*Comprehensive video summary from `summarize_video_audio.py`*

![Summarization Demo](docs/demos/summarize_audio.gif)



## Features

- Real-time video frame analysis using Vision Language Models
- Frame-by-frame descriptions with timestamps
- Multi-modal summarization combining visual and audio transcription content
- Text-only chat capabilities
- Rich console output formatting
- Configurable system prompts for different use cases

## Components

### 1. Server (`server.py`)
- Runs FastAPI server to handle client requests
- Manages Ollama VLM and LLM models
- Processes video frames and generates descriptions
- Handles text-based chat interactions
- Provides API endpoints for all client operations

### 2. Real-time Frame Analysis (`client.py`)
- Captures video frames from webcam in real-time
- Sends frames to server for VLM analysis
- Receives and displays frame descriptions
- Saves timestamped descriptions to a file

### 4. Audio-Video Summary Generation (`summarize_video_audio.py`)
- Generates chronological summaries of video and audio content
- Combines saved frame descriptions with audio transcription
- Provides comprehensive summaries integrating both visual and audio content

### 5. Text Chat (`prompt_only.py`)
- Enables text-only interactions with the LLM
- Supports system prompts for different roles and contexts
- Example use cases included

## Setup and Configuration

1. Install required packages for both server and client:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure server settings:
   - Update `UBUNTU_SERVER_IP` and `UBUNTU_SERVER_PORT` in the configuration section of each script

3. Prepare input stream and files:
   - Ensure your web camera is accessible and properly configured
   - For audio analysis, prepare audio transcription files at AUDIO_TRANSCRIPTION_FILE_PATH

4. Start the server:
   ```bash
   # Run the FastAPI server with uvicorn
   uvicorn server.server:app --host 0.0.0.0 --port 8000 --workers 1
   ```



================================================
FILE: LICENSE
================================================
MIT License

Copyright (c) 2025 lschirripa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



================================================
FILE: client/client.py
================================================
import cv2
import requests
import time
from datetime import datetime
import os # Import the os module for path manipulation
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich import box
from utils.utils import print_framed_output


# --- Configuration ---
# URL of your FastAPI server on Ubuntu
# IMPORTANT: Replace with the actual IP address of your Ubuntu server
UBUNTU_SERVER_IP = "10.147.17.37"
UBUNTU_SERVER_PORT = 8000

SERVER_ENDPOINT = f"http://{UBUNTU_SERVER_IP}:{UBUNTU_SERVER_PORT}/process_frame_with_prompt"

# Desired frames per second to process.
# BASED ON YOUR SERVER LOGS (average ~1.8s processing time per frame),
# setting TARGET_FPS to 0.5 means sending a frame every 2 seconds (1/0.5).
# This gives the server enough time to process and avoid building up a queue.
TARGET_FPS = 0.5

# Calculate the ideal delay needed between sending requests
IDEAL_SEND_INTERVAL = 1.0 / TARGET_FPS

# Timeout for the HTTP request to the server. Should be longer than your server's VLM processing time.
REQUEST_TIMEOUT_SECONDS = 5

# --- Output File Configuration ---
# Define the directory to save the output file
OUTPUT_DIR = "vlm_outputs"
# Define the name of the output text file
OUTPUT_FILENAME = "vlm_responses.txt"
# Full path for the output file
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
# --- End Configuration ---

# --- Customizable Prompts ---
BANK_ASSISTANT_SYSTEM_PROMPT ="""You are a helpful and professional bank assistant. Focus your descriptions 
on financial documents, payment methods, banking activities, or anything related to banking. Your response should be as short and concise as possible within 200 characters more or less"""
BANK_ASSISTANT_USER_QUERY = "What financial documents or activities are visible?"

GENERAL_SCENE_SYSTEM_PROMPT = None # No specific role, just general instructions
GENERAL_SCENE_USER_QUERY = "Describe the overall scene in detail. Your response should be as short and concise as possible within 200 characters more or less"

# Choose which prompt combination to use for testing
CURRENT_SYSTEM_PROMPT = GENERAL_SCENE_SYSTEM_PROMPT
CURRENT_USER_QUERY = GENERAL_SCENE_USER_QUERY
# --- End Customizable Prompts ---


def main():
    """
    Client that captures frames from the webcam and sends them to the VLM server.
    The server processes the frames and returns a response.
    The response is printed to the console and saved to a file.
    The client can be stopped by pressing Ctrl+C.
    """
    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Open video capture (e.g., webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream. Make sure your webcam is available or video path is correct.")
        return

    print(f"Client configured to target {TARGET_FPS} frame(s) per second (every {IDEAL_SEND_INTERVAL:.2f} seconds).")
    print(f"Server Endpoint: {SERVER_ENDPOINT}")
    print(f"VLM responses will be saved to: {OUTPUT_FILE_PATH}")

    frame_count = 0
    last_successful_send_time = time.time()
    
    output_file = None # Initialize to None
    try:
        output_file = open(OUTPUT_FILE_PATH, "w", encoding="utf-8")
        output_file.write(f"--- VLM Responses from {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n\n")

        while True:
            # --- Pacing Logic ---
            time_to_wait = IDEAL_SEND_INTERVAL - (time.time() - last_successful_send_time)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            # --- End Pacing Logic ---

            ret, frame = cap.read()
            if not ret:
                print("End of stream or error reading frame.")
                break

            frame_count += 1
            current_send_time = time.time()

            # print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Capturing and sending frame {frame_count}...")
            # if CURRENT_SYSTEM_PROMPT:
                # print(f"  System Prompt: '{CURRENT_SYSTEM_PROMPT}...'")
            # print(f"  User Query:    '{CURRENT_USER_QUERY}'")

            _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            img_bytes = img_encoded.tobytes()

            files = {'image': ('frame.jpg', img_bytes, 'image/jpeg')}
            data = {'system_prompt': CURRENT_SYSTEM_PROMPT, 'user_query': CURRENT_USER_QUERY}

            try:
                response = requests.post(SERVER_ENDPOINT, files=files, data=data, timeout=REQUEST_TIMEOUT_SECONDS)
                response.raise_for_status()

                response_data = response.json()
                end_time = time.time()
                latency = end_time - current_send_time

                llm_response_text = response_data.get("llm_response", "No LLM response key found.")
                
                # print(f"[{datetime.now().strftime('%H:%M:%S')}] Server response (Latency: {latency:.2f}s): {llm_response_text}")
                # print(f"[{datetime.now().strftime('%H:%M:%S')}] {llm_response_text}")
                print_framed_output(llm_response_text)
                # --- Save to file ---
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                output_file.write(f"--- Frame {frame_count} ({timestamp}, Latency: {latency:.2f}s) ---\n")
                output_file.write(f"User Query: {CURRENT_USER_QUERY}\n")
                output_file.write(f"VLM Response:\n{llm_response_text}\n\n")
                output_file.flush()
                # --- End Save to file ---

                last_successful_send_time = end_time

            except requests.exceptions.Timeout:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Request for frame {frame_count} timed out after {REQUEST_TIMEOUT_SECONDS} seconds. Server busy or model loading?")
                last_successful_send_time = time.time()
            except requests.exceptions.ConnectionError as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection error: {e}. Is the server running and accessible?")
                break
            except requests.exceptions.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] An unexpected request error occurred for frame {frame_count}: {e}")
                last_successful_send_time = time.time()
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] An unexpected error occurred during client processing for frame {frame_count}: {e}")
                last_successful_send_time = time.time()

    except KeyboardInterrupt:
        print("\nStopping stream due to user interrupt.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        if output_file:
            output_file.write(f"\n--- End of Stream ---")
            output_file.close() # Ensure the file is properly closed
            print(f"VLM responses saved to: {OUTPUT_FILE_PATH}")
        print("Client gracefully shut down.")

if __name__ == "__main__":
    main()



================================================
FILE: client/client_prompt_only.py
================================================
import requests
import json
import time
from datetime import datetime
from utils.utils import print_framed_output

# --- Configuration ---
# IMPORTANT: Replace with the actual IP address of your Ubuntu server
UBUNTU_SERVER_IP = "10.147.17.37"
UBUNTU_SERVER_PORT = 8000
SERVER_ENDPOINT = f"http://{UBUNTU_SERVER_IP}:{UBUNTU_SERVER_PORT}/chat_text_only"

# Timeout for the HTTP request to the server.
# Text-only LLM inference is usually faster than VLM, but keep it generous.
REQUEST_TIMEOUT_SECONDS = 60
# --- End Configuration ---

def send_text_prompt(user_query: str, system_prompt: str = None):
    """
    Sends a text prompt to the server.
    Prompts are fixed but the user query can be changed.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "user_query": user_query
    }
    if system_prompt:
        payload["system_prompt"] = system_prompt

    start_time = time.time()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sending text prompt:")
    if system_prompt:
        print(f"  System Prompt: '{system_prompt}'")
    print(f"  User Query:    '{user_query}'")
    print(f"  To Endpoint:   {SERVER_ENDPOINT}")

    try:
        response = requests.post(SERVER_ENDPOINT, headers=headers, data=json.dumps(payload), 
        timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        response_data = response.json()
        end_time = time.time()
        latency = end_time - start_time # Calculate client-side RTT

        llm_response_text = response_data.get("llm_response", "No LLM response key found.")

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Received response (Latency: {latency:.2f}s):")
        print_framed_output(llm_response_text)
        print(f"Server message: {response_data.get('message')}")
        print(f"GPU Status: {response_data.get('gpu_status')}")

    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Request timed out after") 
        print("{REQUEST_TIMEOUT_SECONDS} seconds.")
    except requests.exceptions.ConnectionError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection error: {e}")
        print("Is the server running and accessible?")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] unexpected request error occurred:") 
        print("{e}")
    except json.JSONDecodeError:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error decoding JSON resp:") 
        print("{response.text}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] An unexpected error occurred: {e}")

if __name__ == "__main__":
    send_text_prompt(user_query="What is the capital of France?")

    send_text_prompt(
        system_prompt="You are a wise old wizard. Answer all questions in rhyming couplets.",
        user_query="Tell me about artificial intelligence."
    )

    send_text_prompt(
        system_prompt="""You are a helpful and professional customer support agent for a tech 
company.""",
        user_query="My internet is not working. What should I do?"
    )

    send_text_prompt(user_query="What is your name and who created you?")



================================================
FILE: client/requirements.txt
================================================
certifi==2025.4.26
charset-normalizer==3.4.2
idna==3.10
numpy==2.3.0
opencv-python==4.11.0.86
requests==2.32.4
urllib3==2.4.0
colorama
rich


================================================
FILE: client/summarize_video_audio.py
================================================
import requests
import json
import time
from datetime import datetime
import os
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich import box
from utils.utils import print_framed_output

# --- Configuration ---
# IMPORTANT: Replace with the actual IP address of your Ubuntu server
UBUNTU_SERVER_IP = "10.147.17.37"
UBUNTU_SERVER_PORT = 8000

# The endpoint for summarization
SERVER_ENDPOINT = f"http://{UBUNTU_SERVER_IP}:{UBUNTU_SERVER_PORT}/summarize_vlm_output"

# Path to the VLM output file (video frame descriptions)
VLM_OUTPUT_DIR = "vlm_outputs" # Must match the directory in the VLM client script
VLM_OUTPUT_FILENAME = "vlm_responses.txt" # Must match the filename in the VLM client script
VLM_OUTPUT_FILE_PATH = os.path.join(VLM_OUTPUT_DIR, VLM_OUTPUT_FILENAME)

# NEW: Path to the audio transcription file
AUDIO_TRANSCRIPTION_FILE_PATH = "audio_transcription.txt"

# Adjust based on your model and hardware.
REQUEST_TIMEOUT_SECONDS = 300

# --- Customizable Prompts for Summarization ---
SUMMARIZATION_SYSTEM_PROMPT = """You are an AI assistant tasked with summarizing a chronological log of 
events described by a Vision Language Model (VLM) and an accompanying audio transcription.
The log contains descriptions of individual frames from a video stream, including timestamps and VLM 
observations. The audio transcription provides spoken content with timestamps.
Your goal is to provide a concise, coherent, and chronological summary of what occurred across all 
frames, integrating relevant information from the audio transcription.
Focus on identifying key actions, changes in the scene, significant objects or interactions, and important 
spoken events.
Do not invent information. If an action or spoken event is repeated, note its duration or recurrence.
Your summary should be presented as a flowing narrative, connecting the observations and spoken content naturally.
You should be as short and concise as possible within 400 characters more or less
"""

# The user query will implicitly be the content of the VLM output file + audio transcription.
# We don't need a separate user_query variable here as the file content serves as the main input.
# --- End Configuration ---

def main():
    # --- Read VLM output file ---
    if not os.path.exists(VLM_OUTPUT_FILE_PATH):
        print(f"Error: VLM output file not found at '{VLM_OUTPUT_FILE_PATH}'.")
        print("Please run the VLM client script (`client.py`) first to generate the descriptions.")
        return

    print(f"Reading VLM outputs from: {VLM_OUTPUT_FILE_PATH}")
    try:
        with open(VLM_OUTPUT_FILE_PATH, "r", encoding="utf-8") as f:
            vlm_output_content = f.read()
    except Exception as e:
        print(f"Error reading VLM output file: {e}")
        return

    audio_transcription_content = ""
    if not os.path.exists(AUDIO_TRANSCRIPTION_FILE_PATH):
        print(f"Warning: Audio transcription file not found at '{AUDIO_TRANSCRIPTION_FILE_PATH}'.")
        print("Proceeding with VLM output only.")
    else:
        print(f"Reading audio transcription from: {AUDIO_TRANSCRIPTION_FILE_PATH}")
        try:
            with open(AUDIO_TRANSCRIPTION_FILE_PATH, "r", encoding="utf-8") as f:
                audio_transcription_content = f.read()
        except Exception as e:
            print(f"Error reading audio transcription file: {e}")
            print("Proceeding with VLM output only.")

    combined_user_query = f"""
    VLM Observations (Video Frame Descriptions):
    {vlm_output_content}

    ---

    Audio Transcription:
    {audio_transcription_content}
    """

    # Prepare the payload for the summarization endpoint
    headers = {"Content-Type": "application/json"}
    payload = {
        "system_prompt": SUMMARIZATION_SYSTEM_PROMPT,
        "user_query": combined_user_query
    }

    start_time = time.time()
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Sending VLM output and audio transcription for summarization...")
    print(f"  To Endpoint: {SERVER_ENDPOINT}")
    print(f"  Using System Prompt: {SUMMARIZATION_SYSTEM_PROMPT[:100]}...") # Print a truncated version
    print(f"  User Query (first 100 chars): {combined_user_query[:100]}...") # Print a truncated version

    try:
        response = requests.post(SERVER_ENDPOINT, headers=headers, data=json.dumps(payload), timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()

        response_data = response.json()
        end_time = time.time()
        latency = end_time - start_time # Calculate client-side RTT

        summary_text = response_data.get("llm_response", "No summary text from LLM.")

        # print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Received summary (Latency: {latency:.2f}s):")
        print_framed_output(summary_text)
        
        # print(f"--- End Summarization Result ---")
        # print(f"Server message: {response_data.get('message')}")
        # print(f"GPU Status: {response_data.get('gpu_status')}")

    except requests.exceptions.Timeout:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Request timed out after {REQUEST_TIMEOUT_SECONDS} seconds.")
        print("The summarization model (llama3-70B-cool:latest) might be very slow or requires more resources.")
    except requests.exceptions.ConnectionError as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connection error: {e}. Is the server running and accessible?")
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] An unexpected request error occurred: {e}")
    except json.JSONDecodeError:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error decoding JSON response from server. Raw text: {response.text}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()


================================================
FILE: client/utils/utils.py
================================================
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich import box
from datetime import datetime

console = Console()


def format_colored(timestamp, description):
    """Formats an entry with colors for emphasis."""
    return (
        f"{Fore.CYAN}--- Image Analysis ({timestamp}) ---\n"
        f"{Style.BRIGHT}{description}\n"
        f"{Style.RESET_ALL}" # Resets all formatting
    )

def print_framed_output(response_text):
    try:
        """
        Prints a given response text encapsulated within a rich.Panel.
        """
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Create a Panel for the output
        # - title: The timestamp for the panel's top border
        # - border_style: Color for the border (e.g., "bold blue", "green")
        # - box: Defines the style of the border (e.g., box.DOUBLE, box.ROUNDED)
        # - padding: Adds space around the text inside the panel
        panel = Panel(
            f"[bold white]{response_text}[/bold white]",
            title=f"[bold yellow]VLM Analysis at {current_time}[/bold yellow]",
            border_style="bright_cyan",
            box=box.HEAVY,  # Or box.ROUNDED, box.SQUARE, box.HEAVY
            padding=(2, 4)
        )

        console.print(panel)
        console.print("\n")
    except Exception as e:
        print(e)


================================================
FILE: server/requirements.txt
================================================
annotated-types==0.7.0
anyio==4.9.0
certifi==2025.4.26
charset-normalizer==3.4.2
click==8.2.1
fastapi==0.115.12
filelock==3.18.0
fsspec==2025.5.1
h11==0.16.0
httptools==0.6.4
idna==3.10
Jinja2==3.1.6
MarkupSafe==3.0.2
mpmath==1.3.0
networkx==3.5
numpy==2.3.0
nvidia-cublas-cu12==12.6.4.1
nvidia-cuda-cupti-cu12==12.6.80
nvidia-cuda-nvrtc-cu12==12.6.77
nvidia-cuda-runtime-cu12==12.6.77
nvidia-cudnn-cu12==9.5.1.17
nvidia-cufft-cu12==11.3.0.4
nvidia-cufile-cu12==1.11.1.6
nvidia-curand-cu12==10.3.7.77
nvidia-cusolver-cu12==11.7.1.2
nvidia-cusparse-cu12==12.5.4.2
nvidia-cusparselt-cu12==0.6.3
nvidia-nccl-cu12==2.26.2
nvidia-nvjitlink-cu12==12.6.85
nvidia-nvtx-cu12==12.6.77
opencv-python==4.11.0.86
pydantic==2.11.5
pydantic_core==2.33.2
python-dotenv==1.1.0
python-multipart==0.0.20
PyYAML==6.0.2
requests==2.32.4
setuptools==80.9.0
sniffio==1.3.1
starlette==0.46.2
sympy==1.14.0
torch==2.7.1
triton==3.3.1
typing-inspection==0.4.1
typing_extensions==4.14.0
urllib3==2.4.0
uvicorn==0.34.3
uvloop==0.21.0
watchfiles==1.0.5
websockets==15.0.1


================================================
FILE: server/server.py
================================================
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
import numpy as np
import cv2
import torch
import base64
import requests
import json
from starlette.concurrency import run_in_threadpool
import time
from datetime import datetime



app = FastAPI()

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_VLM_MODEL = "qwen2.5vl:7b"  # change model as needed
OLLAMA_LLM_MODEL = "llama3:8b"

try:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dummy_model = torch.nn.Linear(10, 1).to(device)
    print(f"CUDA is available and dummy model loaded on GPU. device: {device}" if device.type == 'cuda' else f"CUDA not available, using CPU for dummy model. device: {device}")
except Exception as e:
    print(f"Error initializing GPU/PyTorch: {e}")
    device = "cpu"
    print("Falling back to CPU for dummy model due to error.")

class ProcessingResponse(BaseModel):
    message: str
    llm_response: str
    gpu_status: str = "N/A"

class TextPromptRequest(BaseModel):
    system_prompt: str = None # Optional system prompt
    user_query: str # Mandatory user query

def _call_ollama_api_sync(model: str, prompt: str, image_base64: str = None):
    """
    Helper function for Ollama API call (unified, accepts optional image_base64)
    model: str - The Ollama model to use
    prompt: str - The prompt to send to the model
    image_base64: str - The base64 encoded image to send to the model
    Returns:
        dict - The response from the Ollama API
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if image_base64:
        payload["images"] = [image_base64]

    try:
        ollama_response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            headers=headers,
            data=json.dumps(payload),
            timeout=300
        )
        ollama_response.raise_for_status()
        return ollama_response.json()
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Ollama request timed out. Model might be loading or busy.")
    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, "status_code", 500)
        detail = f"Error calling Ollama: {e}"
        if hasattr(e, 'response') and e.response is not None:
             detail += f" - Ollama Response: {getattr(e.response, 'text', 'No response body')}"
        raise HTTPException(status_code=status_code, detail=detail)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail=f"Error decoding Ollama response. Raw text: {ollama_response.text if 'ollama_response' in locals() else 'N/A'}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error during Ollama call: {e}")


@app.post("/process_frame", response_model=ProcessingResponse)
async def process_frame(image: UploadFile = File(...)):
    """
    Endpoint for processing a single image. It describes what is happening in the image in detail.
    Args:
        image: UploadFile - The image to process
    Returns:
        ProcessingResponse - The response from the Ollama API
    """

    request_start_time = time.time()
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    try:
        contents = await image.read()
        img_np = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Could not decode image.")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Received frame for /process_frame (shape: {img.shape})")
        gpu_status_msg = "No specific GPU processing performed for this image (CPU fallback)."
        try:
            img_tensor = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0).to(device)
            gpu_status_msg = "Image tensor moved to GPU."
        except Exception as e:
            print(f"GPU processing error: {e}")
            gpu_status_msg = f"GPU processing failed: {e}"
        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        prompt = "Describe what is happening in this image in detail. Focus on objects, actions, and the overall scene."
        llm_response_text = "VLM processing failed."
        ollama_call_start_time = time.time()
        try:
            ollama_response_json = await run_in_threadpool(_call_ollama_api_sync, OLLAMA_VLM_MODEL, prompt, img_base64)
            ollama_call_end_time = time.time()
            llm_response_text = ollama_response_json.get("response", "No response text from VLM.")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Ollama VLM Response for /process_frame (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {json.dumps(ollama_response_json, indent=2)[:500]}...")
        except HTTPException as e:
            ollama_call_end_time = time.time()
            llm_response_text = f"Ollama VLM error: {e.detail}"
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught Ollama HTTPException for /process_frame (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e.detail}")
        except Exception as e:
            ollama_call_end_time = time.time()
            llm_response_text = f"An unexpected error occurred during Ollama call for /process_frame: {e}"
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught unexpected error for /process_frame (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e}")
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time for /process_frame: {request_end_time - request_start_time:.2f}s")
        return ProcessingResponse(
            message="Frame processed successfully",
            llm_response=llm_response_text,
            gpu_status=gpu_status_msg
        )
    except HTTPException:
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time (HTTPError): {request_end_time - request_start_time:.2f}s")
        raise
    except Exception as e:
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time (Unexpected Error): {request_end_time - request_start_time:.2f}s")
        raise HTTPException(status_code=500, detail=f"Internal server error in frame processing: {e}")

@app.post("/process_frame_with_prompt", response_model=ProcessingResponse)
async def process_frame_with_prompt(
    image: UploadFile = File(...),
    system_prompt: str = Form(None),
    user_query: str = Form(...)
):
    """
    Endpoint for processing a single image with a custom prompt.
    Args:
        image: UploadFile - The image to process
        system_prompt: str - The system prompt to use
        user_query: str - The user query to use
    Returns:
        ProcessingResponse - The response from the Ollama API
    """
    request_start_time = time.time()
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    try:
        contents = await image.read()
        img_np = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Could not decode image.")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Received frame for /process_frame_with_prompt (shape: {img.shape})")
        gpu_status_msg = "No specific GPU processing performed for this image (CPU fallback)."
        try:
            img_tensor = torch.from_numpy(img).permute(2, 0, 1).float().unsqueeze(0).to(device)
            gpu_status_msg = "Image tensor moved to GPU."
        except Exception as e:
            print(f"GPU processing error: {e}")
            gpu_status_msg = f"GPU processing failed: {e}"
        _, buffer = cv2.imencode('.png', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        full_prompt = ""
        if system_prompt:
            full_prompt += f"{system_prompt}\n\n"
        full_prompt += user_query
        llm_response_text = "VLM processing failed."
        ollama_call_start_time = time.time()
        try:
            ollama_response_json = await run_in_threadpool(_call_ollama_api_sync, OLLAMA_VLM_MODEL, full_prompt, img_base64)
            ollama_call_end_time = time.time()
            llm_response_text = ollama_response_json.get("response", "No response text from VLM.")
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Ollama VLM Response for /process_frame_with_prompt (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {json.dumps(ollama_response_json, indent=2)[:500]}...")
        except HTTPException as e:
            ollama_call_end_time = time.time()
            llm_response_text = f"Ollama VLM error: {e.detail}"
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught Ollama HTTPException for /process_frame_with_prompt (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e.detail}")
        except Exception as e:
            ollama_call_end_time = time.time()
            llm_response_text = f"An unexpected error occurred during Ollama call for /process_frame_with_prompt: {e}"
            print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught unexpected error for /process_frame_with_prompt (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e}")
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time for /process_frame_with_prompt: {request_end_time - request_start_time:.2f}s")
        return ProcessingResponse(
            message="Frame processed successfully with custom prompt",
            llm_response=llm_response_text,
            gpu_status=gpu_status_msg
        )
    except HTTPException:
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time (HTTPError): {request_end_time - request_start_time:.2f}s")
        raise
    except Exception as e:
        request_end_time = time.time()
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time (Unexpected Error): {request_end_time - request_start_time:.2f}s")
        raise HTTPException(status_code=500, detail=f"Internal server error in frame processing with prompt: {e}")

@app.post("/chat_text_only", response_model=ProcessingResponse)
async def chat_text_only(request: TextPromptRequest):
    """
    Endpoint for processing a text-only prompt.
    Args:
        request: TextPromptRequest - The request containing the system prompt and user query
    Returns:
        ProcessingResponse - The response from the Ollama API
    """
    request_start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Received text-only request for /chat_text_only")
    full_prompt = ""
    if request.system_prompt:
        full_prompt += f"{request.system_prompt}\n\n"
    full_prompt += request.user_query
    llm_response_text = "LLM processing failed."
    ollama_call_start_time = time.time()
    try:
        ollama_response_json = await run_in_threadpool(_call_ollama_api_sync, OLLAMA_VLM_MODEL, full_prompt, image_base64=None)
        ollama_call_end_time = time.time()
        llm_response_text = ollama_response_json.get("response", "No response text from LLM.")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Ollama LLM Response for /chat_text_only (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {llm_response_text[:500]}...")
    except HTTPException as e:
        ollama_call_end_time = time.time()
        llm_response_text = f"Ollama LLM error: {e.detail}"
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught Ollama HTTPException for /chat_text_only (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e.detail}")
    except Exception as e:
        ollama_call_end_time = time.time()
        llm_response_text = f"An unexpected error occurred during Ollama call for /chat_text_only: {e}"
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught unexpected error for /chat_text_only (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e}")
    request_end_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time for /chat_text_only: {request_end_time - request_start_time:.2f}s")
    return ProcessingResponse(
        message="Text-only prompt processed successfully",
        llm_response=llm_response_text,
        gpu_status="N/A (Text-only request)"
    )

@app.post("/summarize_vlm_output", response_model=ProcessingResponse)
async def summarize_vlm_output(request: TextPromptRequest):
    """
    Endpoint for summarizing the frame-to-frame output of the VLM model.
    Args:
        request: TextPromptRequest - The request containing the system prompt and the user query with the VLM output of the frames captured during the frame-to-frame processing.
    Returns:
        ProcessingResponse - The response from the Ollama API
    """
    request_start_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Received summarization request for /summarize_vlm_output")

    full_prompt = ""
    if request.system_prompt:
        full_prompt += f"{request.system_prompt}\n\n"
    full_prompt += request.user_query # The VLM output content

    llm_summary_text = "Summarization failed."
    ollama_call_start_time = time.time()
    try:
        ollama_response_json = await run_in_threadpool(_call_ollama_api_sync, OLLAMA_LLM_MODEL, full_prompt, image_base64=None)
        ollama_call_end_time = time.time()
        llm_summary_text = ollama_response_json.get("response", "No response text from LLM.")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Ollama LLM Summary Response (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {llm_summary_text[:500]}...")
    except HTTPException as e:
        ollama_call_end_time = time.time()
        llm_summary_text = f"Ollama LLM error: {e.detail}"
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught Ollama HTTPException for summarization (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e.detail}")
    except Exception as e:
        ollama_call_end_time = time.time()
        llm_summary_text = f"An unexpected error occurred during Ollama summarization call: {e}"
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] FastAPI caught unexpected error for summarization (Ollama Time: {ollama_call_end_time - ollama_call_start_time:.2f}s): {e}")

    request_end_time = time.time()
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] Total request processing time for /summarize_vlm_output: {request_end_time - request_start_time:.2f}s")

    return ProcessingResponse(
        message="VLM output summarized successfully",
        llm_response=llm_summary_text,
        gpu_status="N/A (Text summarization)"
    )

@app.get("/")
async def read_root():
    return {"message": "FastAPI server is running and ready for VLM/LLM processing!"}
