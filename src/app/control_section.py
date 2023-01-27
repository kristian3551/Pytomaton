"""Module containing all the widgets for saving, deleting, loading and
creating automatons."""
from tkinter import ttk, PhotoImage
from typing import Dict

class ControlSection:
    """Class that handles all widgets and logic for saving, loading
    or creating automatons."""
    def __init__(self, frame, outer_section) -> None:
        self.outer_section = outer_section
        self.control_section = ttk.Frame(frame)

        self.input_fields: Dict[str, ttk.Entry] = {}

        self.input_fields["name_entry"] = ttk.Entry(self.control_section, width=50)
        self.input_fields["name_entry"].insert(0, "Name ")

        self.input_fields["regex_entry"] = ttk.Entry(self.control_section, width=50)
        self.input_fields["regex_entry"].insert(0, "Regex/name of automaton/empty")

        self.load_button = ttk.Button(self.control_section, text="Load!",
         command=lambda: self.load_auto(self.input_fields["name_entry"].get()))

        self.save_button = ttk.Button(self.control_section, text="Save!",
        command=self.save_auto)

        self.remove_button = ttk.Button(self.control_section, text="Remove!",
        command=lambda: self.remove_auto(self.input_fields["name_entry"].get()))

        self.create_button = ttk.Button(self.control_section, text="Create!",
        command=lambda: self.create_auto(self.input_fields["name_entry"].get(),
             self.input_fields["regex_entry"].get()))

        self.render()

    def render(self):
        """Renders widgets"""
        self.input_fields["name_entry"].grid(row=1)
        self.input_fields["regex_entry"].grid(row=2)
        self.save_button.grid(row=1, column=3)
        self.remove_button.grid(row=2, column=3)
        self.load_button.grid(row=1, column=2)
        self.create_button.grid(row=2, column=2)
        self.control_section.grid(row=1)

    def get_name(self):
        """Returns the value of the entry."""
        return self.input_fields["name_entry"].get()

    def get_regex(self):
        """Returns the value of the regex entry."""
        return self.input_fields["regex_entry"].get()

    def hide_image(self):
        """Function that removes automaton picture from display."""
        if self.outer_section.operation_section.section:
            self.outer_section.operation_section.section.grid_forget()

    def load_image(self):
        """Function that triggers automaton picture creating and loads
        it in the operation section."""
        if self.outer_section.operation_section.auto_image_label:
            self.outer_section.operation_section.auto_image_label.grid_forget()
            self.outer_section.operation_section.name_label.grid_forget()
        auto_image = PhotoImage(file="database/automaton.gv.png")
        self.outer_section.operation_section.auto_image_label = ttk.Label(\
            self.outer_section.operation_section.section, image=auto_image)
        self.outer_section.operation_section.auto_image_label.image = auto_image
        self.outer_section.operation_section.auto_image_label.grid(row=1, column=1, rowspan=10)
        self.outer_section.operation_section.name_label = ttk.Label(\
            self.outer_section.operation_section.section,
            text=f"Name: {self.get_name()}")
        self.outer_section.operation_section.name_label.grid(row=0, column=2)
        self.outer_section.root.update_idletasks()

    def load_auto(self, name: str) -> None:
        """Function that opens the operation section and
        loads the automaton image."""
        try:
            self.outer_section.controller.show_automaton(name)
            self.outer_section.change_name(name)
            if self.outer_section.operation_section.section:
                self.outer_section.operation_section.section.grid_forget()
            self.load_image()
            self.outer_section.operation_section.section.grid(row=6)
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def create_auto(self, name: str, operation: str) -> None:
        """Function that creates automaton in controller and displays
        the operation section."""
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
                self.outer_section.controller.from_regex(operation)\
                    if operation != "empty"\
                         else self.outer_section.controller.empty_automaton())
            self.load_auto(name)
            self.outer_section.set_message("Automation created successfully.")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def remove_auto(self, name: str) -> None:
        """Function that removes automaton in controller and hides
        the operation section."""
        try:
            self.outer_section.controller.remove_automaton(name)
            if self.outer_section.current_auto_name == name:
                self.hide_image()
                self.outer_section.current_auto_name = ""
            self.outer_section.set_message("Automation removed successfully.")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def save_auto(self):
        """Function that saves automatons from controller to files."""
        try:
            self.outer_section.controller.save_in_file()
            self.outer_section.set_message("Automatons saved successfully.")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])
