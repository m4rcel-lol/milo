# 🖥️ Milo: Retro Windows 98 AI Assistant

![Milo Screenshot](MiloBanner.png)

Milo is a friendly, blocky, 2.5D AI assistant desktop app inspired by classic Windows 98 UI—complete with chat, speech synthesis, and a charming avatar that blinks and waves!  
Milo runs Gemini AI locally to chat and uses pyttsx3 for retro text-to-speech, providing an instantly nostalgic experience with modern smarts.

---

## ✨ Features

- **Classic Windows 98 Look**: MS Sans Serif font, beveled controls, and gray backgrounds
- **2.5D Animated Milo Avatar**: Blocky, pixel-era robot with waving, blinking, and classic color shading
- **Voice Output**: Replies are spoken aloud using your system’s TTS (works offline!)
- **Gemini-Powered Chat**: AI replies using Google Gemini (requires an API key, see below)
- **All-in-One EXE**: Bundle as a single `.exe` file with icon and `.env` support—perfect for sharing with friends
- **.env Config**: API key is kept outside the code for safety and easy changes

---

## 🚀 Installation

### Windows Users

1. **Download the Release**
    - *(If using a prebuilt EXE, just grab `Milo.exe` and execute!)*

2. **Manual Build ([Python 3.8+ Required](https://www.python.org/downloads/)):**

    Requirements:
    ```
    tkinter
    google-generativeai
    pyttsx3
    python-dotenv
    ```

---

## ⚙️ Configuration

Create a `.env` file next to `Milo.py` with your Gemini API key:

