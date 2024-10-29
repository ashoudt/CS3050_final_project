import tkinter as tk
from tkinter import ttk

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

        # Dictionary to hold all check box variables
        self.vars = {}

        # Create sections for each card category
        self.create_section("Suspects", ["Colonel Mustard", "Miss Scarlet", 
                            "Mr Green", "Mrs Peacock", "Mrs White", "Professor Plum"], 0)
        self.create_section("Weapons", ["Candle Stick", "Knife", "Lead Pipe", "Revolver"
                            "Rope", "Wrench"], 1)
        self.create_section("Rooms", ["Ballroom", "Billiard Room", "Conservatory",
                            "Dining Room", "Kitchen", "Library", "Lounge", "Study"], 2)
        
        # Create buttons for making suggestions and accusations
        self.create_action_buttons()

    def create_section(self, title, items, col):
        """Creates a section of the checklist with checkboxes"""
        section_frame = ttk.Labelframe(self.frame, text=title, padding="10")
        section_frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

        # Add check boxes for each item in the section
        for item in items:
            var = tk.BooleanVar()
            checkBox = ttk.Checkbutton(section_frame, text=item, variable=var)
            checkBox.pack(anchor="w")
            self.vars[item] = var

    def create_action_buttons(self):
        """Creates suggestion and accustation buttons"""
        button_frame = ttk.Frame(self.frame, padding="10")
        button_frame.grid(row=1, column=0, columnspan=3, pady=10)

        # Create buttons
        suggest_button = ttk.Button(button_frame, text="Suggestion", command=self.suggestion)
        accuse_button = ttk.Button(button_frame, text="Accusation", command=self.accusation)

        suggest_button.pack(side="left", padx=5)
        accuse_button.pack(side="left", padx=5)

    def suggestion(self):
        """Handle suggestion logic (Placeholder)"""
        print("Suggest action initiated")
    
    def accusation(self):
        """Handle accusation logic (Placeholder)"""
        print("Accuse action initiated")
