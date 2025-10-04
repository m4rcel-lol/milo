import tkinter as tk
import threading
from queue import Queue, Empty
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import pyttsx3
from pathlib import Path
import random

ICON = "app.ico" if Path("app.ico").exists() else None

# --- Google API and warnings ---
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

# --- .env handling for PyInstaller and normal runs
if getattr(sys, 'frozen', False):  # PyInstaller bundle
    bundle_dir = sys._MEIPASS
    dotenv_path = os.path.join(bundle_dir, ".env")
else:  # Normal script run
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(bundle_dir, ".env")

load_dotenv(dotenv_path=dotenv_path)

# --- pyttsx3: force new engine for each phrase for reliability ---
def speak_milo(msg):
    try:
        tts = pyttsx3.init()
        voices = tts.getProperty("voices")
        if len(voices) > 1:
            tts.setProperty("voice", voices[1].id)
        tts.setProperty("rate", 155)
        tts.setProperty("volume", 0.88)
        tts.say(msg)
        tts.runAndWait()
        tts.stop()
    except Exception:
        pass

# --- Gemini API ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))
gemini_model = genai.GenerativeModel("gemini-2.0-flash")
gemini_chat = gemini_model.start_chat()

def retro_font():
    return ("MS Sans Serif", 11)

class Milo2_5DBot:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cx = canvas.winfo_reqwidth() // 2
        self.cy = canvas.winfo_reqheight() // 2 + 10
        head_col, head_dark = "#7ab8f0", "#26507a"
        body_col, body_dark = "#b8dcf6", "#223357"
        arm_col, arm_dark = "#53a3d7", "#132437"
        leg_col, leg_dark = "#377ce8", "#202a45"
        highlight = "#e3f2fc"
        self.head_shadow = self.canvas.create_rectangle(self.cx-40+4, self.cy-55+4, self.cx+40+4, self.cy-15+4, fill=head_dark, outline="")
        self.head_main = self.canvas.create_rectangle(self.cx-40, self.cy-55, self.cx+40, self.cy-15, fill=head_col, outline="#000000", width=2)
        self.head_hl = self.canvas.create_rectangle(self.cx-30, self.cy-52, self.cx+10, self.cy-20, fill=highlight, outline="")
        self.eye_left = self.canvas.create_rectangle(self.cx-27, self.cy-45, self.cx-12, self.cy-30, fill="white", outline="#000000", width=2)
        self.eye_left_pupil = self.canvas.create_oval(self.cx-24, self.cy-42, self.cx-15, self.cy-33, fill="black", outline="#000000")
        self.eye_right = self.canvas.create_rectangle(self.cx+12, self.cy-45, self.cx+27, self.cy-30, fill="white", outline="#000000", width=2)
        self.eye_right_pupil = self.canvas.create_oval(self.cx+15, self.cy-42, self.cx+24, self.cy-33, fill="black", outline="#000000")
        self.mouth = self.canvas.create_arc(self.cx-13, self.cy-22, self.cx+13, self.cy-10, start=200, extent=140, style=tk.ARC, width=2, outline="#285B15")
        self.body_shadow = self.canvas.create_rectangle(self.cx-25+3, self.cy-15+3, self.cx+25+3, self.cy+55+3, fill=body_dark, outline="")
        self.body_main = self.canvas.create_rectangle(self.cx-25, self.cy-15, self.cx+25, self.cy+55, fill=body_col, outline="#000000", width=2)
        self.body_hl = self.canvas.create_rectangle(self.cx-10, self.cy-8, self.cx+17, self.cy+7, fill=highlight, outline="")
        self.left_arm_shadow = self.canvas.create_rectangle(self.cx-55+3, self.cy-12+3, self.cx-25+3, self.cy+6+3, fill=arm_dark, outline="")
        self.left_arm = self.canvas.create_rectangle(self.cx-55, self.cy-12, self.cx-25, self.cy+6, fill=arm_col, outline="#000000", width=2)
        self.right_arm_shadow = self.canvas.create_rectangle(self.cx+25+3, self.cy-12+3, self.cx+55+3, self.cy+6+3, fill=arm_dark, outline="")
        self.right_arm = self.canvas.create_rectangle(self.cx+25, self.cy-12, self.cx+55, self.cy+6, fill=arm_col, outline="#000000", width=2)
        self.left_leg_shadow = self.canvas.create_rectangle(self.cx-18+3, self.cy+55+3, self.cx-6+3, self.cy+85+3, fill=leg_dark, outline="")
        self.left_leg = self.canvas.create_rectangle(self.cx-18, self.cy+55, self.cx-6, self.cy+85, fill=leg_col, outline="#000000", width=2)
        self.right_leg_shadow = self.canvas.create_rectangle(self.cx+6+3, self.cy+55+3, self.cx+18+3, self.cy+85+3, fill=leg_dark, outline="")
        self.right_leg = self.canvas.create_rectangle(self.cx+6, self.cy+55, self.cx+18, self.cy+85, fill=leg_col, outline="#000000", width=2)
        self.blinking = False
    def blink(self):
        if not self.blinking:
            self.blinking = True
            self.canvas.itemconfig(self.eye_left_pupil, fill="white")
            self.canvas.itemconfig(self.eye_right_pupil, fill="white")
    def open_eyes(self):
        self.blinking = False
        self.canvas.itemconfig(self.eye_left_pupil, fill="black")
        self.canvas.itemconfig(self.eye_right_pupil, fill="black")
    def set_expression(self, mood):
        self.canvas.delete(self.mouth)
        if mood == "happy":
            self.mouth = self.canvas.create_arc(self.cx-12, self.cy-25, self.cx+12, self.cy-9, start=200, extent=140, style=tk.ARC, width=3, outline="#107C10")
        elif mood == "thinking":
            self.mouth = self.canvas.create_oval(self.cx-4, self.cy-18, self.cx+4, self.cy-12, fill="#EBBD13", outline="#BFA213")
        else:
            self.mouth = self.canvas.create_arc(self.cx-13, self.cy-22, self.cx+13, self.cy-10, start=200, extent=140, style=tk.ARC, width=2, outline="#285B15")
    def wave_animation(self, finish_cb=None):
        positions = [(self.cx-60, self.cy-28, self.cx-25, self.cy-8), (self.cx-60, self.cy-12, self.cx-25, self.cy+6)]
        def animate(i=0):
            pos = positions[i % 2]
            self.canvas.coords(self.left_arm, *pos)
            self.canvas.coords(self.left_arm_shadow, pos[0]+3, pos[1]+3, pos[2]+3, pos[3]+3)
            if i < 7:
                self.canvas.after(150, lambda: animate(i+1))
            else:
                self.canvas.coords(self.left_arm, *positions[1])
                self.canvas.coords(self.left_arm_shadow, positions[1][0]+3, positions[1][1]+3, positions[1][2]+3, positions[1][3]+3)
                if finish_cb: finish_cb()
        animate()
    def start_blinking_randomly(self, root):
        def schedule(): root.after(random.randint(2100, 4400), do_blink)
        def do_blink():
            self.blink()
            self.canvas.after(120, self.open_eyes)
            schedule()
        schedule()

class MiloApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Milo - Windows 98 2.5D AI Assistant")
        if ICON: self.iconbitmap(ICON)
        self.geometry("480x520")
        self.minsize(480, 520)
        self.maxsize(480, 520)
        self.resizable(False, False)

        # Compose layout (all in one main container)
        main = tk.Frame(self, bg="#C0C0C0")
        main.pack(fill="both", expand=True, padx=10, pady=6)

        # Milo avatar
        self.robot_canvas = tk.Canvas(main, width=320, height=220, bg="#E8F1FA", bd=2, relief="sunken")
        self.robot_canvas.pack(pady=(4, 10))
        self.milo = Milo2_5DBot(self.robot_canvas)

        # Milo's response box
        resp_label = tk.Label(main, text="Milo's Response:", bg="#F7F9FC", font=retro_font(), anchor="w")
        resp_label.pack(fill="x", padx=5)
        self.response_box = tk.Text(main, height=4, state=tk.DISABLED, font=retro_font(),
                                   bg="#ffffff", fg="#102040", wrap="word")
        self.response_box.pack(fill="x", padx=8, pady=(0, 8))

        # Input box directly underneath response
        input_frame = tk.Frame(main, bg="#e8f1fa", bd=2, relief="sunken")
        input_frame.pack(fill="x", pady=(4,8), padx=8)
        self.entry = tk.Entry(input_frame, font=retro_font(), bg="#ffffff", fg="#102040", relief="sunken", bd=2)
        self.entry.pack(side="left", fill="x", expand=True, padx=(6,2), pady=8)
        self.entry.bind("<Return>", lambda e: self.send_message())
        self.send_btn = tk.Button(input_frame, text="Send", font=retro_font(), bg="#DBDFEA", fg="black",
                                  relief="raised", bd=2, command=self.send_message, padx=20, pady=6)
        self.send_btn.pack(side="right", padx=(3,10), pady=6)

        self.status = tk.Label(self, text="Ready.", font=retro_font(),
                               bg="#C0C0C0", fg="#000000", bd=2, relief="sunken", anchor="w")
        self.status.pack(fill="x", side="bottom")

        self.typing_active = False
        self.response_queue = Queue()
        self.after(240, self.milo_intro)
        self.milo.start_blinking_randomly(self)
        self.after(100, self.check_responses)

    def milo_intro(self):
        self.milo.wave_animation(finish_cb=self._milo_intro_finished)
        self.robot_canvas.after(120, self.milo.open_eyes)

    def _milo_intro_finished(self):
        self.display_response("Hello! I'm Milo, your Windows 98 style assistant.")
        self.milo.set_expression("happy")
        self.status.config(text="Ready for your input.")
        self.after(1800, lambda: self.milo.set_expression("neutral"))

    def display_response(self, message):
        self.response_box.config(state=tk.NORMAL)
        self.response_box.delete("1.0", tk.END)
        self.response_box.insert(tk.END, message)
        self.response_box.config(state=tk.DISABLED)
        self.response_box.see(tk.END)
        threading.Thread(target=speak_milo, args=(message,), daemon=True).start()

    def send_message(self):
        if self.typing_active:
            return
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.entry.delete(0, tk.END)
        self.typing_active = True
        self.status.config(text="Milo is thinking...")
        self.milo.set_expression("thinking")
        threading.Thread(target=self.query_ai, args=(user_text,), daemon=True).start()

    def query_ai(self, user_text):
        try:
            response = gemini_chat.send_message(user_text)
            reply = response.text
        except Exception:
            reply = "(Sorry, there was a problem. Please try again.)"
        self.response_queue.put(reply)

    def check_responses(self):
        try:
            while True:
                reply = self.response_queue.get_nowait()
                self.display_response(reply)
                self.milo.set_expression("happy")
                self.status.config(text="Ready.")
                self.typing_active = False
                self.after(1500, lambda: self.milo.set_expression("neutral"))
        except Empty:
            pass
        self.after(100, self.check_responses)

if __name__ == "__main__":
    app = MiloApp()
    app.mainloop()
