import arcade
import arcade.gui
import tkinter as tk
from notesheet import Notesheet as ns

class GameUI:
    """
    Manage the UI elements in the program.
    """
    def __init__(self, manager):
        self.manager = manager
        self.notesheet_visible = False # Track if notesheet is visible

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


        # Create an editable test area for the notesheet
        self.notesheet = arcade.gui.UIInputText(text="Input Notes:", width=400, height=600)

        # Handle click events
        notesheet_button.on_click = self.on_click_notesheet
        roll_button.on_click = self.on_click_start

        # Create a widget to hold the h_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    def on_click_start(self, event):
        """Place holder for actions"""
        print("Start:", event)

    def on_click_notesheet(self, event):
        """ Function to open the notesheet"""
        if not self.notesheet_visible:
            self.notesheet_visible = True
            root = tk.Tk()
            app = ns(manager=root)
            root.mainloop()
