# ShellHacks 2025 - AI-Powered Cognitive Assistance System

A comprehensive AI-powered assistance system designed to help individuals with Alzheimer's disease and their caregivers, featuring Google A2A ADK multimodal AI integration, specialized cognitive agents, and real-time communication capabilities.

## 🧠 System Overview

This project consists of two main components:

### 1. **Cognitive Assistance System (A2A)** - Alzheimer's Support
- **Google A2A ADK Integration**: Real-time multimodal AI with voice, video, and text processing
- **Specialized AI Agents**: Memory assistance, routine management, safety monitoring, and family communication
- **Professional Frontend**: Modern web interface with audio/video capabilities
- **Real-time Communication**: WebSocket-based interaction with Google's advanced AI

### 2. **Screen Capture System (Assist)** - Messenger Analysis
- **Cross-Platform Screen Capture**: Windows, macOS, and Linux support
- **Ollama AI Integration**: Local AI processing with vision and language models
- **Real-time Analysis**: Live conversation analysis and summarization
- **Professional GUI**: Easy-to-use interface for screen capture and AI processing

## 🚀 Quick Start

### Cognitive Assistance System (A2A)

```bash
# Navigate to A2A system
cd a2a

# Setup and install dependencies
python setup.py

# Configure your Google A2A ADK API key
# Edit backend/.env file with your API key

# Start the system
python start.py

# Open http://localhost:8000 in your browser
```

### Screen Capture System (Assist)

   ```bash
# Navigate to assist system
   cd assist

# Install dependencies
   pip install -r server/requirements.txt
   pip install -r screen_capture/requirements.txt

# Start Ollama (if not already running)
ollama serve
ollama pull gemma3:4b
ollama pull qwen3:8b

# Start the system
   python start.py
   ```

## 🏗️ Architecture

### Cognitive Assistance System (A2A)

```
Frontend (HTML/JS) → WebSocket → FastAPI Backend → Google A2A ADK
                                    ↓
                            Cognitive Agents
                    ├── Memory Assistance
                    ├── Routine Management  
                    ├── Safety Monitoring
                    └── Family Communication
```

### Screen Capture System (Assist)

```
Screen Capture → FastAPI Backend → Ollama AI → Analysis & Storage
     ↓              ↓                ↓
  Audio/Video    WebSocket      Vision + Language
  Processing     Streaming       Models
```

## 🎯 Key Features

### Cognitive Assistance System

- **🤖 Multimodal AI**: Voice, video, and text interaction with Google A2A ADK
- **🧠 Memory Assistance**: Reminiscence therapy and cognitive support
- **📅 Routine Management**: Medication reminders and daily schedules
- **🛡️ Safety Monitoring**: Emergency detection and fall monitoring
- **👨‍👩‍👧‍👦 Family Communication**: Facilitated communication with caregivers
- **🎤 Real-time Interaction**: Natural conversation with interruption handling
- **📱 Modern Interface**: Professional web interface with audio/video capabilities

### Screen Capture System

- **🖥️ Cross-Platform**: Windows, macOS, and Linux support
- **🎥 Screen Capture**: High-quality video and audio capture
- **🤖 AI Analysis**: Real-time conversation analysis with Ollama
- **📊 Summarization**: Automatic conversation summaries
- **💾 File Management**: Organized storage and session management
- **🔧 Professional GUI**: Easy-to-use interface

## 📋 Requirements

### Cognitive Assistance System

- **Python 3.8+**
- **Google A2A ADK API Key** (from Google Cloud Console)
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Microphone and Camera** (for multimodal interaction)

### Screen Capture System

- **Python 3.8+**
- **Ollama** (local AI models)
- **Audio/Video Drivers**
- **Browser** (Chrome, Firefox, Safari, Edge)

## 🔧 Installation

### Cognitive Assistance System

```bash
cd a2a
python setup.py
# Configure API key in backend/.env
python start.py
```

### Screen Capture System

```bash
cd assist
pip install -r server/requirements.txt
pip install -r screen_capture/requirements.txt
# Install Ollama and models
python start.py
```

## 📚 Documentation

- **[A2A README](a2a/README.md)**: Cognitive assistance system documentation
- **[A2A Deployment Guide](a2a/DEPLOYMENT_GUIDE.md)**: Production deployment guide
- **[Assist README](assist/README.md)**: Screen capture system documentation
- **[Ollama Integration](assist/OLLAMA_INTEGRATION_README.md)**: Ollama setup guide

## 🧪 Testing

### Cognitive Assistance System

```bash
cd a2a
python tests/test_cognitive_system.py
```

### Screen Capture System

```bash
cd assist
python server/test_ollama_client.py
python server/integration_test.py
```

## 🚀 Deployment

### Production Deployment

Both systems support production deployment with:

- **Docker containers**
- **Reverse proxy (Nginx)**
- **Environment configuration**
- **Health monitoring**
- **Logging and analytics**

See individual deployment guides for detailed instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is part of the ShellHacks 2025 competition.

## 🆘 Support

For technical support:

1. Check the troubleshooting sections in the documentation
2. Review the logs for error messages
3. Test with minimal configuration
4. Create an issue with detailed information

## 🏆 Impact

This system is designed to:

- **Improve Quality of Life**: Enhanced daily living for individuals with Alzheimer's
- **Reduce Caregiver Stress**: Support for family members and caregivers
- **Increase Safety**: Proactive safety monitoring and emergency response
- **Maintain Independence**: Help individuals maintain their independence longer
- **Strengthen Family Bonds**: Facilitate meaningful family connections

---

*Built with compassion and understanding for the unique challenges of Alzheimer's disease. This system represents a commitment to improving the lives of individuals with Alzheimer's and their families through innovative AI technology.*
