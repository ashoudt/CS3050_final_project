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

        self.default_style = {
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

        self.disabled_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.GRAY,
        }


        # Create a horizontal BoxGroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create buttons
        notesheet_button = arcade.gui.UIFlatButton(text="Notesheet", width=200, style=self.default_style)
        self.h_box.add(notesheet_button.with_space_around(right=60))


        # Handle click events
        notesheet_button.on_click = self.on_click_notesheet

        # Position the buttons 
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    def on_click_notesheet(self, event):
        """Initiate the tkinter window for the Notesheet in a new thread"""
        if not self.notesheet_visible:
            self.notesheet_visible = True
            threading.Thread(target=self.open_notesheet, daemon=True).start()
    def open_notesheet(self):
        """
        Create and show the Notesheet window
        """  
        root = tk.Tk()
        app = ns(manager=root)
        root.mainloop()
        self.notesheet_visible = False # Reset visability flag
