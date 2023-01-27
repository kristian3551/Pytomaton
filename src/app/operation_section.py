"""Module containing widgets for the section where
 automatons are managed."""
from tkinter import ttk
from src.app.input_section import InputSection
from src.app.button_section import ButtonSection

class OperationSection:
    """Class that handles"""
    def __init__(self, frame, outer_section) -> None:
        self.section = ttk.Frame(frame)
        self.outer_section = outer_section
        self.auto_image_label = ttk.Label(self.section)
        self.name_label = ttk.Label(self.section,
         text="Name: ")
        self.input_section = InputSection(self.section, self)
        self.buttons_section = ButtonSection(self.section, self)
        self.render()

    def get_controller(self):
        """Gets controller from App."""
        return self.outer_section.controller

    def render(self):
        """Renders widgets in grid."""
        self.auto_image_label.grid(column=1, row=2)
        self.name_label.grid(column=2)
