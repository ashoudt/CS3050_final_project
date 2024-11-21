import arcade
from driver import GameView

class PlayerSelectionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # List of character cards with images
        self.characters = [
            ("Miss Scarlet", "assets/clue cards/missscarlet.png"),
            ("Colonel Mustard", "assets/clue cards/colonelmustard.png"),
            ("Mrs. White", "assets/clue cards/mrswhite.png"),
            ("Mr. Green", "assets/clue cards/mrgreen.png"),
            ("Mrs. Peacock", "assets/clue cards/mrspeacock.png"),
            ("Professor Plum", "assets/clue cards/professorplum.png")
        ]

        # Track selected character button
        self.selected_button = None

        # Main vertical box for grid and Next button
        main_v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        # Create two horizontal boxes for each row of buttons
        row1 = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        row2 = arcade.gui.UIBoxLayout(vertical=False, space_between=10)

        # Loop through characters and create buttons, then add them to rows
        for i, (character_name, character_image) in enumerate(self.characters):
            button = arcade.gui.UITextureButton(
                texture=arcade.load_texture(character_image),
                width=200,
                height=300,
            )
            # Attach an event handler with the button and character name
            button.on_click = lambda event, button=button, name=character_name: self.on_character_select(button, name)

            # Add button to the appropriate row
            if i < 3:
                row1.add(button)
            else:
                row2.add(button)

        # Add both rows to the main vertical layout
        main_v_box.add(row1)
        main_v_box.add(row2)

        # Render buttons
        self.default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.RASPBERRY,
        }

        # Create the Next button
        next_button = arcade.gui.UIFlatButton(text="Next", width=100, style = self.default_style)
        next_button.on_click = self.on_next_button_click
        main_v_box.add(next_button)

        # Anchor the main layout to the center of the screen
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=main_v_box
            )
        )

    def on_character_select(self, button, character_name):
        # Store the selected button for the outline
        self.selected_button = button
        self.window.character_name = character_name
        print(f"Character selected: {character_name}")

    def on_next_button_click(self, event):
        # Move to game if player selected
        if self.selected_button != None:
            game_view = GameView()
            self.window.show_view(game_view)


    def on_draw(self):
        self.clear()
        self.manager.draw()

        # Draw a ring around the selected character if any
        if self.selected_button:
            x, y = self.selected_button.center_x, self.selected_button.center_y
            arcade.draw_rectangle_outline(x, y, self.selected_button.width + 10, self.selected_button.height + 10,
                                          color=arcade.color.YELLOW, border_width=5)

    def on_hide_view(self):
        self.manager.disable()