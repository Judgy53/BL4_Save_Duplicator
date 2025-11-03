import tkinter as tk
from tkinter import ttk

class Tooltip:
    """Simple tooltip for tkinter widgets."""
    def __init__(self, widget: ttk.Widget, text: str, delay: int = 250):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.id = None
        widget.bind("<Enter>", self.schedule)
        widget.bind("<Leave>", self.hide)
        widget.bind("<ButtonPress>", self.hide)

    def schedule(self, event=None):
        """Schedule the tooltip to appear after a delay."""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show)

    def unschedule(self):
        """Cancel the scheduled tooltip display."""
        id_ = self.id
        self.id = None
        if id_:
            try:
                self.widget.after_cancel(id_)
            except Exception:
                pass

    def show(self):
        """Display the tooltip."""
        if self.tipwindow or not self.text:
            return
        # Position tooltip based on current mouse pointer coordinates so it follows the cursor
        try:
            x = self.widget.winfo_pointerx() + 20
            y = self.widget.winfo_pointery() + 10
        except Exception:
            # Fallback to widget-based positioning if pointer query fails
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=(None, 8, 'normal'))
        label.pack(ipadx=4, ipady=2)

    def hide(self, event=None):
        """Hide the tooltip."""
        self.unschedule()
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except Exception:
                pass
