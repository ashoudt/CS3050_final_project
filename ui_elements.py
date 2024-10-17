import arcade
import arcade.gui

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
            "font_color": arcade.color.BLACK,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.WHITE,

            # used if button is pressed
            "bg_color_pressed": arcade.color.RASPBERRY,
            "border_color_pressed": arcade.color.RASPBERRY,  # also used when hovered
            "font_color_pressed": arcade.color.WHITE,
        }

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create buttons
        suggestion_button = arcade.gui.UIFlatButton(text="Suggestion", width=200, style=default_style)
        self.v_box.add(suggestion_button.with_space_around(bottom=20))
        accusation_button = arcade.gui.UIFlatButton(text="Accusation", width=200, style=default_style)
        self.v_box.add(accusation_button.with_space_around(bottom=20))
        #notesheet_button = arcade.gui.UIFlatButton(text="Notesheet", width=200)

        # Create an editable test area for the notesheet
        self.notesheet = arcade.gui.UIInputText(text="Input Notes:", width=400, height=600)

        # Handle click events
        suggestion_button.on_click = self.on_click_start
        accusation_button.on_click = self.on_click_start

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-475,
                anchor_y="center_y",
                align_y=-375,
                child=self.v_box)
        )

    def on_click_start(self, event):
        print("Start:", event)