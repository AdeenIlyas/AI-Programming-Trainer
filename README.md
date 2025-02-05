# AI Coding Interviewer & Competitive Programming Trainer 

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0B0B0B?style=for-the-badge)](https://www.crewai.com/)

An AI-powered platform for practicing coding interviews and competitive programming challenges, featuring automated problem generation, code evaluation, and personalized feedback.

![Screenshot 2025-02-05 131727](https://github.com/user-attachments/assets/dcf5172c-9869-41ad-bf8d-613183a54582)

<p align="center">
  
![Screenshot 2025-02-05 131808](https://github.com/user-attachments/assets/143d48df-cc9f-4bca-b984-e86808d7c4e7)

![Screenshot 2025-02-05 131825](https://github.com/user-attachments/assets/4eb0b924-81a2-4deb-ac12-cbce8243a1d5)

![Screenshot 2025-02-05 131836](https://github.com/user-attachments/assets/fa338840-1002-443c-b1bf-73c20c50289a)

</p>


## Key Features ✨

- **Smart Problem Generation**
  - Customizable by difficulty (Easy/Medium/Hard)
  - Topic-specific challenges (Arrays, Graphs, DP, etc)
  - Real-world interview question patterns
  - Real time debugging and syntax analysis

- **AI-Powered Evaluation** 🔍
  - Code correctness verification
  - Time/space complexity analysis
  - Edge case detection
  - Code quality assessment

- **Personalized Feedback** 🚀
  - Step-by-step solution explanations
  - Optimization suggestions
  - Alternative approach recommendations
  - Learning Resources
  - 

## Tech Stack ⚙️

- **Core AI**
  - 🧠 gemma2-9b-it (via Groq)
  - 🤖 CrewAI Agent Orchestration

- **Frontend**
  - 🎨 Streamlit Web Interface
  - 📊 Interactive Code Editor

- **Backend**
  - 🐍 Python 3.10+
  - 📦 Poetry Package Management

## Getting Started 🚀

### Prerequisites
- Python 3.10+
- [Groq Cloud API Key](https://console.groq.com/keys)

### Installation
```bash
# Clone repository
git clone https://github.com/AdeenIlyas/AI-Competitive-Programming-Trainer.git
cd ai-coding-interviewer

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys to .env
