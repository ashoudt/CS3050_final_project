import arcade
import arcade.gui
import tkinter as tk
import threading
from notesheet import Notesheet as ns

class GameUI:
    """
    Manage the UI elements in the program.
    """
    def __init__(self, manager):
        self.manager = manager
        self.notesheet_visible = False # Track if notesheet is visible
        self.notesheet_window = None
        self.notesheet_instance = None  # Hold the Notesheet instance

        # Render button
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.RASPBERRY,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RASPBERRY,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

        # Create a horizontal BoxGroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create buttons
        notesheet_button = arcade.gui.UIFlatButton(text="Notesheet", width=200, style=default_style)
        self.h_box.add(notesheet_button.with_space_around(right=60))
        roll_button = arcade.gui.UIFlatButton(text="Roll", width=200, style=default_style)
        self.h_box.add(roll_button.with_space_around(left=60))

        # Handle click events
        notesheet_button.on_click = self.on_click_notesheet
        roll_button.on_click = self.on_click_roll

        # Position the buttons 
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    def on_click_roll(self, event):
        """
        Place holder for roll actions
        """
        print("Roll action started")

    def on_click_notesheet(self, event):
        """
        Initiate the tkinter window for the Notesheet in a new thread
        """
        if not self.notesheet_visible:
            self.notesheet_visible = True
            print("Opening Notesheet...")
            self.open_notesheet()

    def open_notesheet(self):
        """
        Create and show the Notesheet window
        """  
        # Initialize the Tk window
        self.notesheet_window = tk.Tk()
        
        # Create an instance of Notesheet within the Tk root
        self.notesheet_instance = ns(self.notesheet_window)
        print("Initializing Notesheet...")

        # Handle the closing of the Notesheet
        self.notesheet_window.protocol("WM_DELETE_WINDOW", self.close_notesheet)

    def close_notesheet(self):
        """
        Close the Notesheet window, save data, and reset visibility
        """
        if self.notesheet_window:
            # Call Notesheet's on_close to ensure data is saved
            if self.notesheet_instance:
                self.notesheet_instance.on_close()
                print("Notesheet closed.")

    def update_notesheet(self):
        """
        Update the tkinter window periodically if open
        """
        if self.notesheet_window:
            try:
                self.notesheet_window.update()
            except tk.TclError:
                # If window is already destroyed, set the reference to None
                self.notesheet_window = None
                self.notesheet_visible = False
