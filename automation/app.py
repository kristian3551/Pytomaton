"""The actual GUI app. All of the application logic is performed in
an instance of Controller class, held in class App. Everything else is just hardcoded
GUI interface made with TKinter."""

from tkinter import ttk, PhotoImage, Tk
from typing import Dict
from automation.controller.controller import Controller

# --------------------------------- App ---------------------------------

class App:
    """Main class for the application"""
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry(newGeometry="700x700")
        self.controller: Controller = Controller()
        self.controller.load_from_file()
        self.current_auto_name: str = ""
        self.message_label = ttk.Label(self.root)
        self.message_label.grid(row=0)

        self.control_section: ControlSection = ControlSection(self.root, self)
        self.construction_section: ConstructionSection = ConstructionSection(self.root, self)
        self.operation_section: OperationSection = OperationSection(self.root, self)

    def set_message(self, message):
        """Function that sets the top message label with text={message}."""
        if self.message_label:
            self.message_label.grid_forget()
        self.message_label = ttk.Label(self.root, text=message)
        self.message_label.grid()
        self.message_label.grid(row=0)
    def change_name(self, name):
        """Function that changes current automaton name."""
        self.current_auto_name = name
    def run(self):
        """Function that starts the application."""
        self.root.mainloop()

# --------------------------------- Control section ---------------------------------

class ControlSection:
    """Class that handles all widgets and logic for saving, loading
    or creating automatons."""
    def __init__(self, frame, outer_section: App) -> None:
        self.outer_section = outer_section
        self.control_section = ttk.Frame(frame)

        self.input_fields: Dict[str, ttk.Entry] = {}

        self.input_fields["name_entry"] = ttk.Entry(self.control_section, width=50)
        self.input_fields["name_entry"].insert(0, "Name ")
        self.input_fields["name_entry"].grid(row=1)
        self.input_fields["regex_entry"] = ttk.Entry(self.control_section, width=50)
        self.input_fields["regex_entry"].insert(0, "Regex/name of automaton/empty")
        self.input_fields["regex_entry"].grid(row=2)
        self.load_button = ttk.Button(self.control_section, text="Load!",
         command=lambda: self.load_auto(self.input_fields["name_entry"].get()))
        self.save_button = ttk.Button(self.control_section, text="Save!",
        command=self.save_auto)
        self.save_button.grid(row=1, column=3)
        self.remove_button = ttk.Button(self.control_section, text="Remove!",
        command=lambda: self.remove_auto(self.input_fields["name_entry"].get()))
        self.remove_button.grid(row=2, column=3)
        self.load_button.grid(row=1, column=2)
        self.create_button = ttk.Button(self.control_section, text="Create!",
        command=lambda: self.create_auto(self.input_fields["name_entry"].get(),
             self.input_fields["regex_entry"].get()))
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

# --------------------------------- Construction section ---------------------------------

class ConstructionSection:
    """Class that handles all the logic behind
    performing basic automatons constructions."""
    def __init__(self, frame, outer_section: App) -> None:
        self.construction_section = ttk.Frame(frame)

        self.outer_section = outer_section

        self.input_fields: Dict[str, ttk.Button] = {}

        self.input_fields["determinize_button"] = ttk.Button(self.construction_section,
         text="Determinize",
         command=lambda: self.perform_construction("det", "Successfully determinized automaton!",
             self.outer_section.control_section.get_name()))

        self.input_fields["minimize_button"]\
        = ttk.Button(self.construction_section, text="Minimize",
        command=lambda: self.perform_construction("min", "Successfully minimized automaton!",
             self.outer_section.control_section.get_name()))

        self.input_fields["concat_button"]\
            = ttk.Button(self.construction_section, text="Concat",
        command=lambda: self.perform_construction("concat", "Successfully concatenated automatons!",
             self.outer_section.control_section.get_name(),
              self.outer_section.control_section.get_regex()))

        self.input_fields["union_button"] = ttk.Button(self.construction_section, text="Union",
        command=lambda: self.perform_construction("union", "Successfully united automaton!",
             self.outer_section.control_section.get_name(),
             self.outer_section.control_section.get_regex()))

        self.input_fields["star_button"] = ttk.Button(self.construction_section, text="Kleene star",
        command=lambda: self.perform_construction("star", "Successfully starred automaton!",
             self.outer_section.control_section.get_name()))

        self.input_fields["total_button"] = ttk.Button(self.construction_section, text="Make total",
        command=lambda: self.perform_construction("tot", "Successfully made automaton total!",
             self.outer_section.control_section.get_name()))

        self.input_fields["intersection_button"]\
            = ttk.Button(self.construction_section, text="Intersection",
        command=lambda: self.perform_construction("intersect",
             "Successfully intersected automatons!",
             self.outer_section.control_section.get_name(),
             self.outer_section.control_section.get_regex()))

        self.input_fields["complement_button"]\
            = ttk.Button(self.construction_section, text="Complement",
        command=lambda: self.perform_construction("compl", "Successfully united automaton!",
             self.outer_section.control_section.get_name()))
        self.render_elements()

    def render_elements(self):
        """Function that displays widgets in grid."""
        self.input_fields["determinize_button"].grid(row=1, column=1, padx=5)
        self.input_fields["minimize_button"].grid(row=1, column=2, padx=5)
        self.input_fields["concat_button"].grid(row=1, column=3, padx=5)
        self.input_fields["union_button"].grid(row=1, column=4, padx=5)
        self.input_fields["star_button"].grid(row=2, column=1, padx=5)
        self.input_fields["intersection_button"].grid(row=2, column=2)
        self.input_fields["total_button"].grid(row=2, column=3)
        self.input_fields["complement_button"].grid(row=2, column=4)
        self.construction_section.grid(row=2)

    def perform_construction(self, cons_type: str, succ_message: str, name1: str, name2: str = ""):
        """Function triggered when clicking on
         button from this section."""
        try:
            auto_to_replace = self.outer_section.controller.empty_automaton()
            if cons_type == "compl":
                auto_to_replace = self.outer_section.controller.complement(name1)
            elif cons_type == "det":
                auto_to_replace = self.outer_section.controller.determinize(name1)
            elif cons_type == "tot":
                auto_to_replace = self.outer_section.controller.total(name1)
            elif cons_type == "concat":
                auto_to_replace = self.outer_section.controller.concat(name1, name2)
            elif cons_type == "min":
                auto_to_replace = self.outer_section.controller.minimize(name1)
            elif cons_type == "intersect":
                auto_to_replace = self.outer_section.controller.intersection(name1, name2)
            elif cons_type == "union":
                auto_to_replace = self.outer_section.controller.union(name1, name2)
            elif cons_type == "star":
                auto_to_replace = self.outer_section.controller.star(name1)
            self.outer_section.controller.replace_or_add_automaton(name1,
                auto_to_replace)
            self.outer_section.control_section.load_auto(name1)
            self.outer_section.set_message(succ_message)
        except KeyError as error:
            self.outer_section.set_message(error.args[0])
        except ValueError as error:
            self.outer_section.set_message(error.args[0])

# --------------------------------- Operation section ---------------------------------

class OperationSection:
    """Class that handles"""
    def __init__(self, frame, outer_section: App) -> None:
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

# --------------------------------- Input section ---------------------------------

class InputSection:
    """Class that handles state and transition input."""
    def __init__(self, frame: ttk.Frame, outer_section: OperationSection) -> None:
        self.outer_section = outer_section
        self.input_section = ttk.Frame(frame)
        self.accepts_word_entry = ttk.Entry(self.input_section, width=30)
        self.accepts_word_entry.insert(0, "Type word")
        self.accepts_button = ttk.Button(self.input_section, text="Accepts word",
        command=lambda: self.accepts_word(self.accepts_word_entry.get()))
        self.state_entry = ttk.Entry(self.input_section, width=30)
        self.state_entry.insert(0, 'State: name')
        self.transition_entry = ttk.Entry(self.input_section, width=30)
        self.transition_entry.insert(0, "Transitions: name letter name")

        self.render()

    def render(self):
        """Displays section widgets."""
        self.accepts_word_entry.grid()
        self.state_entry.grid(pady=5, padx=10)
        self.accepts_button.grid()
        self.transition_entry.grid()
        self.state_entry.grid()
        self.input_section.grid(column=2, row=2)

    def accepts_word(self, word):
        """Function triggered when the button with label
        "accepts word" is pressed."""
        try:
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.outer_section.outer_section.set_message("Word is ACCEPTED"
                if self.outer_section.outer_section.controller.accepts_word(current_auto_name, word)
                 else "Word is REJECTED")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

# --------------------------------- Button section ---------------------------------

class ButtonSection:
    """Class that handles basic automatons operations (managing state, transitions, etc.)."""
    def __init__(self, frame: ttk.Frame, outer_section: OperationSection) -> None:
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
            tokens = raw.split(' ')
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
            tokens = raw.split(' ')
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
