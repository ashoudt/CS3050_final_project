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

        # Create a vertical BoxGroup to align buttons
        self.h_box = arcade.gui.UIBoxLayout(vertical=False)

        # Create buttons
        #suggestion_button = arcade.gui.UIFlatButton(text="Suggestion", width=200, style=default_style)
        #self.v_box.add(suggestion_button.with_space_around(bottom=20))
        #accusation_button = arcade.gui.UIFlatButton(text="Accusation", width=200, style=default_style)
        #self.v_box.add(accusation_button.with_space_around(bottom=100))
        notesheet_button = arcade.gui.UIFlatButton(text="Notesheet", width=200, style=self.default_style)
        self.h_box.add(notesheet_button.with_space_around(right=50))


        # Create an editable test area for the notesheet
        self.notesheet = arcade.gui.UIInputText(text="Input Notes:", width=400, height=600)

        # Handle click events
        notesheet_button.on_click = self.on_click_start

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                align_x=-100,
                anchor_y="center_y",
                align_y=-335,
                child=self.h_box)
        )

    def on_click_start(self, event):
        print("Start:", event)