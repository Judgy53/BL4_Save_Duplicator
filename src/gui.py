import os
import tkinter as tk
import utils
from save import Save
from tkinter import ttk, filedialog, messagebox
from tooltip import Tooltip

DEFAULT_PATH = os.path.join(os.getenv("USERPROFILE"), "Documents", "My Games", "Borderlands 4", "Saved", "SaveGames")
INPUT_WIDTH = 50

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Borderlands 4 Save Duplicator")
        self.root.geometry("500x475")
        self.root.resizable(False, False)
        self.root.iconbitmap(default=utils.resource_path(os.path.join("assets", "icon.ico")))

        self.loaded_save: Save | None = None

        # UI Variables
        self.source_file = tk.StringVar()
        self.steam_id = tk.StringVar()
        self.char_name = tk.StringVar()
        self.randomize_guid = tk.BooleanVar(value=True)
        self.reset_playtime = tk.BooleanVar(value=False)
        self.reset_challenges = tk.BooleanVar(value=False)
        self.reset_uvh_challenges = tk.BooleanVar(value=False)

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Source file selection
        ttk.Label(main_frame, text="Source Save File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_file_entry = ttk.Entry(main_frame, textvariable=self.source_file, width=INPUT_WIDTH)
        self.source_file_entry.grid(row=0, column=1, padx=(5,5), pady=5)
        self.source_file_entry.bind('<KeyRelease>', self.on_source_file_change)
        ttk.Button(main_frame, text="Browse", command=self.browse_source).grid(row=0, column=2, pady=5)

        # Steam ID
        ttk.Label(main_frame, text="Steam ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.steam_id_entry = ttk.Entry(main_frame, textvariable=self.steam_id, width=INPUT_WIDTH)
        self.steam_id_entry.grid(row=1, column=1, padx=(5,5), pady=5)
        self.steam_id_entry.bind('<KeyRelease>', self.on_source_file_change)

        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Character name
        ttk.Label(main_frame, text="Character Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.char_name_entry = ttk.Entry(main_frame, textvariable=self.char_name, width=INPUT_WIDTH)
        self.char_name_entry.grid(row=3, column=1, padx=(5,5), pady=5)

        # Options checkboxes in their own frame
        ttk.Label(main_frame, text="Options:").grid(row=4, column=0, sticky=tk.W, pady=5)
        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W, pady=2)

        # Randomize GUID and Reset Playtime options
        self.randomize_guid_cb = ttk.Checkbutton(options_frame, text="Randomize character GUID",
                                               variable=self.randomize_guid)
        self.randomize_guid_cb.grid(row=0, column=0, sticky=tk.W, padx=(0,10))
        Tooltip(self.randomize_guid_cb, "Necessary to avoid save conflict")

        self.reset_playtime_cb = ttk.Checkbutton(options_frame, text="Reset playtime",
                                               variable=self.reset_playtime)
        self.reset_playtime_cb.grid(row=0, column=1, sticky=tk.W)
        Tooltip(self.reset_playtime_cb, "Set total playtime to 0")

        # Challenge reset options
        self.reset_challenges_cb = ttk.Checkbutton(options_frame, text="Reset challenges",
                                               variable=self.reset_challenges)
        self.reset_challenges_cb.grid(row=1, column=0, sticky=tk.W)
        Tooltip(self.reset_challenges_cb, "/!\\ EXPERIMENTAL /!\\\nReset all non-UVH challenge progress")

        self.reset_uvh_cb = ttk.Checkbutton(options_frame, text="Reset UVH challenges",
                                               variable=self.reset_uvh_challenges)
        self.reset_uvh_cb.grid(row=1, column=1, sticky=tk.W)
        Tooltip(self.reset_uvh_cb, "/!\\ EXPERIMENTAL /!\\\nReset all UVH challenge progress")

        # Duplicate button
        self.duplicate_button = ttk.Button(main_frame, text="Duplicate Save File",
                                         command=self.duplicate_save, style="Accent.TButton")
        self.duplicate_button.grid(row=5, column=0, columnspan=3, sticky=(tk.E, tk.W), pady=20)

        # Status/log area
        ttk.Label(main_frame, text="Status:").grid(row=6, column=0, sticky=(tk.W, tk.N), pady=5)
        self.status_text = tk.Text(main_frame, width=100, height=13, wrap=tk.WORD)
        self.status_text.grid(row=6, column=1, columnspan=2, padx=(5,0), pady=5)

        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S), pady=5)
        self.status_text.configure(yscrollcommand=scrollbar.set)

        # Configure column weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Initially disable UI elements until source file is selected
        self.set_ui_enabled(False)

    def set_ui_enabled(self, enabled: bool):
        """Enable or disable UI elements"""
        state = "normal" if enabled else "disabled"

        self.char_name_entry.configure(state=state)
        self.randomize_guid_cb.configure(state=state)
        self.reset_playtime_cb.configure(state=state)
        self.reset_challenges_cb.configure(state=state)
        self.reset_uvh_cb.configure(state=state)
        self.duplicate_button.configure(state=state)

    def browse_source(self):
        """Open file dialog to select source save file"""
        initialdir = DEFAULT_PATH
        childs = os.listdir(initialdir) if os.path.exists(initialdir) else []
        if len(childs) == 1:
            initialdir = os.path.join(initialdir, childs[0], "Profiles", "client")

        filename = filedialog.askopenfilename(
            initialdir=initialdir,
            title="Select source save file",
            filetypes=[("Save files", "*.sav"), ("All files", "*.*")]
        )
        if filename:
            if os.path.basename(filename).lower() == "profile.sav":
                messagebox.showerror("Error", "Please select a valid save file, not 'profile.sav'.")
                return
            self.source_file.set(filename)
            self.source_file_entry.icursor(tk.END)
            self.source_file_entry.xview_moveto(1.0)

            self.on_source_file_change()

    def on_source_file_change(self, event=None):
        """Handle changes to the source file field"""
        source_path = self.source_file.get().strip()
        steam_id = self.steam_id.get().strip()
        try:
            self.loaded_save = Save.try_load_from_file(source_path, steam_id)
            if self.loaded_save:
                self.steam_id.set(self.loaded_save.steam_id)
                self.char_name.set(self.loaded_save.get_char_name())
                self.set_ui_enabled(True)
            else:
                self.set_ui_enabled(False)
                self.char_name.set("")
        except Exception as e:
            self.set_ui_enabled(False)
            self.char_name.set("")

    def log_message(self, message: str):
        """Log a message to the status text area"""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

    def duplicate_save(self):
        """Perform the save file duplication with modifications"""
        # Validate inputs
        if not self.char_name.get().strip():
            messagebox.showerror("Error", "Please provide a character name.")
            return

        if not self.loaded_save:
            messagebox.showerror("Error", "No valid source save file loaded.")
            return

        self.status_text.delete(1.0, tk.END)

        dest_filename = filedialog.asksaveasfilename(
            title="Select destination save file",
            defaultextension=".sav",
            initialfile=os.path.basename(self.source_file.get()),
            filetypes=[("Save files", "*.sav"), ("All files", "*.*")]
        )

        if not dest_filename:
            self.status_text.insert(tk.END, "Operation cancelled by user.\n")
            return

        try:
            new_save = self.loaded_save.clone()

            self.log_message(f"Updated character:")

            # Handle GUID randomization
            if self.randomize_guid.get():
                new_save.randomize_char_guid()
                self.log_message(f"  GUID: {self.loaded_save.get_char_guid()} → {new_save.get_char_guid()}")
            else:
                self.log_message(f"  GUID: Unchanged ({self.loaded_save.get_char_guid()})")

            # Handle character name
            if self.char_name.get().strip() != self.loaded_save.get_char_name():
                new_save.set_char_name(self.char_name.get().strip())
                self.log_message(f"  Name: {self.loaded_save.get_char_name()} → {new_save.get_char_name()}")
            else:
                self.log_message(f"  Name: Unchanged ({self.loaded_save.get_char_name()})")

            # Handle playtime reset
            if self.reset_playtime.get():
                new_save.reset_playtime()
                self.log_message(f"  Playtime: {self.loaded_save.get_playtime()} → 0")
            else:
                self.log_message(f"  Playtime: Unchanged ({self.loaded_save.get_playtime()})")

            # Handle challenges reset options
            if self.reset_challenges.get():
                new_save.reset_challenges()
                self.log_message("  Challenges: Reset")
            else:
                self.log_message("  Challenges: Unchanged")

            if self.reset_uvh_challenges.get():
                new_save.reset_uvh_challenges()
                self.log_message("  UVH Challenges: Reset")
            else:
                self.log_message("  UVH Challenges: Unchanged")

            new_save.save_to_file(dest_filename)

            self.log_message(f"Successfully wrote {os.path.basename(dest_filename)}")
            self.log_message("Don't forget to return to title screen, new saves don't load otherwise.")

        except Exception as e:
            error_msg = f"Error during duplication: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)

    def run(self):
        self.root.mainloop()
