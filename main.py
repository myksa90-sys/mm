import flet as ft

def main(page: ft.Page):
    """
    Main function to build the Flet calculator application.
    """
    page.title = "Responsive Calculator"
    # Align content to the start vertically and center horizontally for a modern look
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # Enable dark mode
    page.window_width = 370  # Initial window width
    page.window_height = 600  # Initial window height
    page.window_resizable = True  # Allow window resizing for responsiveness
    page.padding = 20  # Add padding around the content
    page.bgcolor = ft.colors.BLUE_GREY_900  # Set a dark background color

    # --- Calculator Logic Variables ---
    current_expression = ""  # Stores the full expression to be evaluated
    current_display = "0"    # Stores the number currently shown on the display
    clear_on_next_number = False # Flag to clear display when a number is pressed after an '=' or operator

    def update_display():
        """
        Updates the calculator's text field with the current_display value,
        handling empty states and long numbers.
        """
        nonlocal current_display
        if current_display == "":
            result_field.value = "0" # Show '0' if display is empty
        elif len(current_display) > 12: # Limit display length for readability
            # Format large numbers to scientific notation
            try:
                result_field.value = f"{float(current_display):.7g}"
            except ValueError: # In case of "Error" or invalid number
                result_field.value = current_display
        else:
            result_field.value = current_display
        page.update()

    def on_button_click(e):
        """
        Handles all button clicks and updates the calculator's state and display.
        """
        nonlocal current_expression, current_display, clear_on_next_number
        button_text = e.control.text

        if button_text == "C":  # Clear all
            current_expression = ""
            current_display = "0"
            clear_on_next_number = False
        elif button_text == "DEL":  # Delete last character
            if current_display != "Error":
                current_display = current_display[:-1]
                if not current_display or current_display == "-":
                    current_display = "0"
        elif button_text == "=":
            if current_expression and current_display and current_display != "Error":
                try:
                    # Append current display value to form the full expression
                    full_expression = current_expression + current_display
                    # Replace common double-operator mistakes for simpler eval
                    full_expression = full_expression.replace('--', '+').replace('++', '+')
                    # Use eval for calculation. Note: eval can be a security risk with untrusted input.
                    # Here, input comes only from buttons, mitigating risk.
                    result = str(eval(full_expression))
                    current_display = result
                    current_expression = result # Allow chaining operations from the result
                    clear_on_next_number = True
                except (SyntaxError, ZeroDivisionError):
                    current_display = "Error"
                    current_expression = ""
                    clear_on_next_number = False
                except Exception: # Catch any other unexpected calculation errors
                    current_display = "Error"
                    current_expression = ""
                    clear_on_next_number = False
            else:
                # If '=' pressed with only a number, just display it as the result
                current_expression = current_display
                clear_on_next_number = True
        elif button_text in ["+", "-", "*", "/"]:  # Operator buttons
            if current_display != "Error":
                # If current_expression already ends with an operator, replace it
                if current_expression and current_expression.strip() and current_expression.strip()[-1] in ["+", "-", "*", "/"]:
                    current_expression = current_expression[:-1] + button_text
                else:
                    # Only add current_display to expression if it's not the initial '0' or is part of a previous expression
                    if current_display != "0" or current_expression:
                        current_expression += current_display
                    current_expression += button_text
                current_display = "" # Clear display for the next number input
                clear_on_next_number = False
        elif button_text == ".":  # Decimal point
            if current_display != "Error":
                if clear_on_next_number or current_display == "0":
                    current_display = "0."
                    clear_on_next_number = False
                elif "." not in current_display: # Add decimal only if not already present
                    current_display += "."
        else:  # Number buttons (0-9)
            if current_display == "Error": # If previous operation resulted in error, start new
                current_display = button_text
                current_expression = ""
            elif clear_on_next_number: # Clear display if last action was '=' or operator
                current_display = button_text
                clear_on_next_number = False
            elif current_display == "0" and button_text != "0": # Replace initial '0' with new digit
                current_display = button_text
            elif current_display != "0" or button_text == "0": # Append digit to current number
                current_display += button_text
        
        update_display()

    # --- UI Elements ---

    # Calculator display field
    result_field = ft.TextField(
        value=current_display,
        text_align=ft.TextAlign.RIGHT,
        read_only=True,  # Users cannot directly type into it
        max_lines=1,
        min_lines=1,
        height=90,
        content_padding=20,
        border=ft.InputBorder.NONE,
        text_style=ft.TextStyle(size=48, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=ft.border_radius.all(15),
        expand=True, # Make it expand horizontally
    )

    def create_button(text, color_scheme, col_span):
        """
        Helper function to create a calculator button with consistent styling.
        :param text: The text displayed on the button.
        :param color_scheme: "action", "operator", "equals", or "number" to determine button color.
        :param col_span: How many Flet 'ResponsiveRow' columns this button should span (out of 12).
        """
        # Define colors based on the scheme
        if color_scheme == "action": # C, DEL buttons
            bgcolor = ft.colors.RED_600
            hover_bgcolor = ft.colors.RED_500
        elif color_scheme == "operator": # +, -, *, / buttons
            bgcolor = ft.colors.ORANGE_500
            hover_bgcolor = ft.colors.ORANGE_400
        elif color_scheme == "equals": # = button
            bgcolor = ft.colors.BLUE_600
            hover_bgcolor = ft.colors.BLUE_500
        else: # Number and decimal point buttons
            bgcolor = ft.colors.BLUE_GREY_700
            hover_bgcolor = ft.colors.BLUE_GREY_600

        return ft.Container(
            content=ft.ElevatedButton(
                text=text,
                on_click=on_button_click,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)),
                    bgcolor={
                        ft.MaterialState.DEFAULT: bgcolor,
                        ft.MaterialState.HOVERED: hover_bgcolor,
                    },
                    color=ft.colors.WHITE, # Text color
                    text_style=ft.TextStyle(size=28, weight=ft.FontWeight.BOLD)
                ),
                elevation=2, # Add a subtle shadow
                expand=True, # Make button fill its container
            ),
            col={
                "xs": col_span
            }, # Responsive column span
            height=70, # Fixed height for buttons
            padding=ft.padding.all(5) # Padding around each button
        )

    # Define the layout of calculator buttons using a list of controls
    buttons_grid_controls = [
        # Row 1
        create_button("C", "action", 3),
        create_button("DEL", "action", 3),
        create_button("/", "operator", 3),
        create_button("*", "operator", 3),

        # Row 2
        create_button("7", "number", 3),
        create_button("8", "number", 3),
        create_button("9", "number", 3),
        create_button("-", "operator", 3),

        # Row 3
        create_button("4", "number", 3),
        create_button("5", "number", 3),
        create_button("6", "number", 3),
        create_button("+", "operator", 3),

        # Row 4 (1, 2, 3, .)
        create_button("1", "number", 3),
        create_button("2", "number", 3),
        create_button("3", "number", 3),
        create_button(".", "number", 3),

        # Row 5 (0 and =) - 0 spans 2 columns, = spans 2 columns
        create_button("0", "number", 6),  # "0" button takes 6 out of 12 columns (equivalent to 2 standard columns)
        create_button("=", "equals", 6),  # "=" button takes 6 out of 12 columns (equivalent to 2 standard columns)
    ]

    # Add the result field and the button grid to the page
    page.add(
        ft.Column(
            [
                result_field,
                ft.ResponsiveRow(
                    buttons_grid_controls,
                    run_spacing={
                        "xs": 10
                    }, # Vertical spacing between rows of buttons
                    column_spacing={
                        "xs": 10
                    }, # Horizontal spacing between buttons in a row
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            expand=True, # Make the main column expand to fill available height
            spacing=10, # Space between the result field and the button grid
        )
    )
    page.update() # Update the page to display all controls

# Start the Flet application
ft.app(target=main)
