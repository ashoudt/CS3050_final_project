import tkinter as tk
from tkinter import ttk
import json
import os

# Initiate file to save the notesheet state
SAVE_FILE = "notesheet_state.json"

class Notesheet:
    """ 
    Create and manage the notesheet within the game.

    Provide suggestion and button capabilities.
    """

    def __init__(self, manager):
        self.manager = manager
        self.manager.title("Notesheet")

        # Create main frame for notesheet
        self.frame = ttk.Frame(self.manager, padding="10")
        self.frame.grid(row=0, column=0, sticky="nsew")
        

        # Configure grid layout
        self.manager.grid_rowconfigure(0, weight=1)
        self.manager.grid_columnconfigure(0, weight=1)

        # Create sections for each card category
        self.vars = {} # Dictionary to hold all check box variables

        self.create_section("Suspects", ["Colonel Mustard", "Miss Scarlet", 
                            "Mr Green", "Mrs Peacock", "Mrs White", "Professor Plum"], 0)
        self.create_section("Weapons", ["Candle Stick", "Knife", "Lead Pipe", "Revolver", 
                            "Rope", "Wrench"], 1)
        self.create_section("Rooms", ["Ballroom", "Billiard Room", "Conservatory",
                            "Dining Room", "Kitchen", "Library", "Lounge", "Study"], 2)
        
        # Create a section for user notes
        notes_label = ttk.Label(self.frame, text="Your Notes:")
        notes_label.grid(row=1, column=0, pady=(20,5), sticky="w")

        self.notes_text = tk.Text(self.frame, width=50, height=10)
        self.notes_text.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Create buttons for making suggestions and accusations
        self.create_action_buttons()

        # Load saved state if available
        self.load_data()

        # Bind close event to save data when window is closed
        self.manager.protocol("WM_DELETE_WINDOW", self.on_close)


    def create_section(self, title, items, col):
        """
        Creates a section of the checklist with checkboxes
        """
        section_frame = ttk.Labelframe(self.frame, text=title, padding="10")
        section_frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

        # Add check boxes for each item in the section
        for item in items:
            var = tk.BooleanVar()
            checkBox = ttk.Checkbutton(section_frame, text=item, variable=var)
            checkBox.pack(anchor="w")
            self.vars[item] = var


    def create_action_buttons(self):
        """
        Creates suggestion and accustation buttons
        """
        button_frame = ttk.Frame(self.frame, padding="10")
        button_frame.grid(row=3, column=0, pady=10)

        # Create buttons
        suggest_button = ttk.Button(button_frame, text="Suggestion", command=self.suggestion)
        accuse_button = ttk.Button(button_frame, text="Accusation", command=self.accusation)

        suggest_button.pack(side="left", padx=5)
        accuse_button.pack(side="left", padx=5)
    

    def save_data(self):
        """
        Save the state of check boxes and notes to a file
        """
        data = {
            "checkboxes": {key: var.get() for key, var in self.vars.items()},
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Data saved successfully.")


    def load_data(self):
        """
        Load the state of checkboxes and notes from a file if available
        """
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
                # Restore checkbox states
                for key, value in data.get("checkboxes", {}).items():
                    if key in self.vars:
                        self.vars[key].set(value)
                # Restore notes text
                self.notes_text.insert("1.0", data.get("notes", ""))
            print("Data loaded successfully.")

    def on_close(self):
        """
        Save data and close the window
        """
        self.save_data()
        self.manager.destroy()

    def suggestion(self):
        """
        Handle suggestion logic (Placeholder)
        """
        print("Suggest action initiated")
    
    def accusation(self):
        """
        Handle accusation logic (Placeholder)
        """
        print("Accuse action initiated")
