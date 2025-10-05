# 🔐 AI Security Monitor  

An **AI-powered real-time security system** using computer vision and YOLOv8.  
The system continuously monitors a camera feed, detects people (or other objects), saves alert snapshots, and sends notifications to **Telegram**.

---

## ✨ Features
- 🔍 Real-time object detection with **YOLOv8**.  
- 📲 **Telegram alerts** with snapshots.  
- 📸 Automatic saving of detected frames to an `alerts/` folder.  
- ⚙️ Configurable target class (e.g., `person`, `car`, `dog`).  

---

## ⚙️ Installation

1. Clone the project:
   ```bash
   git clone https://github.com/username/ai-security-monitor.git
   cd ai-security-monitor
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
    python -m venv .venv
    .venv\Scripts\activate     # Windows
    source .venv/bin/activate  # Linux/Mac
    
    pip install -r requirements.txt
    ```

3. **Set up your Telegram Bot:**

   
        Open BotFather and create new bot
        Copy your Bot Token.
        Send a message to your bot.
        Get your Chat ID from:
        https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
5.  **Create a config.json file in the project root:**
   
        {
          "TELEGRAM_TOKEN": "your_bot_token_here",
          "CHAT_ID": "your_chat_id_here"
        }
7.   **▶️ Usage**
   
        python security_ai.py
        Press ESC to quit the live feed.
        All alerts are stored in the alerts/ folder.
        Telegram bot sends real-time alerts with pictures.

8. **📲 Example Telegram Alert**
    🚨 Person detected!



