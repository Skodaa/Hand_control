import tkinter as tk

_COLORS = {
    "IDLE": "gray",
    "ARMED": "orange",
    "COOLDOWN": "red",
}

_SIZE = 20
_MARGIN = 10


class StatusIndicator:
    def __init__(self):

        self.root = tk.Tk()

        self.root.overrideredirect(True)

        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85) 

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = _MARGIN
        y = screen_height - _SIZE - _MARGIN

        self.root.geometry(f"{_SIZE}x{_SIZE}+{x}+{y}")

        self.canvas = tk.Canvas(self.root, width=_SIZE, height=_SIZE, highlightthickness=0)
        self.canvas.pack()

        self._dot = self.canvas.create_oval(2, 2, _SIZE - 2, _SIZE - 2, fill="gray")

    def set_state(self, state):

        color = _COLORS.get(state, "gray")
        self.canvas.itemconfig(self._dot, fill=color)

    def refresh(self):
        self.root.attributes("-topmost", True)
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        self.root.destroy()