"""Class holding the logic behind managing automatons via GUI."""
from tkinter import ttk
from typing import Dict

class ButtonSection:
    """Class that handles basic automatons operations (managing state, transitions, etc.)."""
    def __init__(self, frame: ttk.Frame, outer_section) -> None:
        self.buttons_section = ttk.Frame(frame)
        self.outer_section = outer_section

        self.buttons: Dict[str, ttk.Button] = {}
        # Buttons widgets
        self.buttons["remove_state_button"] = ttk.Button(self.buttons_section, text="Remove state",
        command=lambda: self.remove_state(self.outer_section.input_section.state_entry.get()))

        self.buttons["add_state_button"] = ttk.Button(self.buttons_section, text="Add state",
        command=lambda: self.add_state(self.outer_section.input_section.state_entry.get()))

        self.buttons["remove_final_button"] = ttk.Button(self.buttons_section, text="Make unfinal",
        command=lambda: self.remove_final(self.outer_section.input_section.state_entry.get()))

        self.buttons["add_final_button"] = ttk.Button(self.buttons_section, text="Make final",
        command=lambda: self.add_final(self.outer_section.input_section.state_entry.get()))

        self.buttons["add_start_button"] = ttk.Button(self.buttons_section, text="Make start",
        command=lambda: self.add_start(self.outer_section.input_section.state_entry.get()))

        self.buttons["remove_start_button"] = ttk.Button(self.buttons_section, text="Remove start",
        command=lambda: self.remove_start(self.outer_section.input_section.state_entry.get()))

        self.buttons["add_transition_button"] = ttk.Button(self.buttons_section,
        text="Add transition",
        command=lambda: self.add_transition(\
            self.outer_section.input_section.transition_entry.get()))

        self.buttons["remove_transition_button"]\
            = ttk.Button(self.buttons_section, text="Remove transition",
        command=lambda: self.remove_transition(\
            self.outer_section.input_section.transition_entry.get()))

        self.render()

    def __get_controller(self):
        """Gets controller from higher sections in the tree."""
        return self.outer_section.outer_section.controller

    def render(self):
        """Displays section content."""
        self.buttons["add_state_button"].grid(row=3, column=1, padx=5)
        self.buttons["remove_state_button"].grid(row=3, column=2, padx=5)
        self.buttons["add_start_button"].grid(row=4, column=1, padx=5)
        self.buttons["remove_start_button"].grid(row=4, column=2, padx=5)
        self.buttons["add_final_button"].grid(row=5, column=1, padx=5)
        self.buttons["remove_final_button"].grid(row=5, column=2, padx=5)
        self.buttons["add_transition_button"].grid(row=6, column=1, padx=5)
        self.buttons["remove_transition_button"].grid(row=6, column=2)
        self.buttons_section.grid(row=4, column=2, padx=5)


    # Functions triggered when pressing buttons in this section.
    # All of their action is self-explanatory.

    def add_transition(self, raw: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            tokens = raw.split(" ")
            self.__get_controller().add_transition(current_auto_name,
                 tokens[0], tokens[1], tokens[2])
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully added transition!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
        except IndexError:
            self.outer_section.outer_section.set_message("Invalid input!")

    def remove_transition(self, raw: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            tokens = raw.split(" ")
            self.__get_controller().remove_transition(current_auto_name,
             tokens[0], tokens[1], tokens[2])
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed transition!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
        except IndexError:
            self.outer_section.outer_section.set_message("Invalid input!")

    def remove_final(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().make_state_unfinal(current_auto_name, label)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed from finals!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_final(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().make_state_final(current_auto_name, label)
            self.__get_controller().show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully added to finals!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_start(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().set_start(current_auto_name, label)
            self.__get_controller().show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully added to starts!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def remove_start(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().remove_start(current_auto_name, label)
            self.__get_controller().show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed from starts!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def remove_state(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().remove_state(current_auto_name, label)
            self.__get_controller().show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed state!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_state(self, label: str):
        """Function triggered when clicking on
         button from this section with the same name as the function."""
        try:
            control_section = self.outer_section.outer_section.control_section
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.__get_controller().add_state(current_auto_name, label)
            self.__get_controller().show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
