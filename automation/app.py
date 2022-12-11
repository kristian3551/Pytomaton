"""The actual GUI app."""

from tkinter import ttk, PhotoImage, Tk
from automation.controller.controller import Controller

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

class ControlSection:
    """Class that handles all widgets and logic for saving, loading
    or creating automatons."""
    def __init__(self, frame, outer_section: App) -> None:
        self.outer_section = outer_section
        self.control_section = ttk.Frame(frame)
        self.name_entry = ttk.Entry(self.control_section, width=50)
        self.name_entry.insert(0, "Name ")
        self.name_entry.grid(row=1)
        self.regex_entry = ttk.Entry(self.control_section, width=50)
        self.regex_entry.insert(0, "Regex/name of automaton")
        self.regex_entry.grid(row=2)
        self.load_button = ttk.Button(self.control_section, text="Load!",
         command=lambda: self.load_auto(self.name_entry.get()))
        self.save_button = ttk.Button(self.control_section, text="Save!",
        command=self.save_auto)
        self.save_button.grid(row=1, column=3)
        self.remove_button = ttk.Button(self.control_section, text="Remove!",
        command=lambda: self.remove_auto(self.name_entry.get()))
        self.remove_button.grid(row=2, column=3)
        self.load_button.grid(row=1, column=2)
        self.create_button = ttk.Button(self.control_section, text="Create!",
        command=lambda: self.create_auto(self.name_entry.get(),
             self.regex_entry.get()))
        self.create_button.grid(row=2, column=2)
        self.control_section.grid(row=1)

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
            text=f"Name: {self.name_entry.get()}")
        self.outer_section.operation_section.name_label.grid(row=0, column=2)
        self.outer_section.root.update_idletasks()

    def load_auto(self, name: str) -> None:
        """Function that opens the operation section."""
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
                self.outer_section.controller.from_regex(operation))
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

class ConstructionSection:
    """Class that handles all the logic behind
    performing basic automatons constructions."""
    def __init__(self, frame, outer_section: App) -> None:
        self.construction_section = ttk.Frame(frame)

        self.outer_section = outer_section

        self.determinize_button = ttk.Button(self.construction_section, text="Determinize",
        command=lambda: self.determinize(self.outer_section.control_section.name_entry.get()))

        self.minimize_button = ttk.Button(self.construction_section, text="Minimize",
        command=lambda: self.minimize(self.outer_section.control_section.name_entry.get()))

        self.concat_button = ttk.Button(self.construction_section, text="Concat",
        command=lambda: self.concat(self.outer_section.control_section.name_entry.get(),
         self.outer_section.control_section.regex_entry.get()))

        self.union_button = ttk.Button(self.construction_section, text="Union",
        command=lambda: self.union(self.outer_section.control_section.name_entry.get(),
         self.outer_section.control_section.regex_entry.get()))

        self.star_button = ttk.Button(self.construction_section, text="Kleene star",
        command=lambda: self.star(self.outer_section.control_section.name_entry.get()))

        self.total_button = ttk.Button(self.construction_section, text="Make total",
        command=lambda: self.total(self.outer_section.control_section.name_entry.get()))

        self.intersection_button = ttk.Button(self.construction_section, text="Intersection",
        command=lambda: self.intersect(self.outer_section.control_section.name_entry.get(),
         self.outer_section.control_section.regex_entry.get()))

        self.complement_button = ttk.Button(self.construction_section, text="Complement",
        command=lambda: self.complement(self.outer_section.control_section.name_entry.get()))
        self.render_elements()

    def render_elements(self):
        self.determinize_button.grid(row=1, column=1, padx=5)
        self.minimize_button.grid(row=1, column=2, padx=5)
        self.concat_button.grid(row=1, column=3, padx=5)
        self.union_button.grid(row=1, column=4, padx=5)
        self.star_button.grid(row=2, column=1, padx=5)
        self.intersection_button.grid(row=2, column=2)
        self.total_button.grid(row=2, column=3)
        self.complement_button.grid(row=2, column=4)
        self.construction_section.grid(row=2)

    def complement(self, name: str) -> None:
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
                self.outer_section.controller.complement(name))
            self.outer_section.control_section.load_auto(name)
            self.outer_section.set_message("Successfully made automaton complement")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def determinize(self, name: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
                self.outer_section.controller.determinize(name))
            self.outer_section.control_section.load_auto(name)
            self.outer_section.set_message("Successfully determinized automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def total(self, name: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
                self.outer_section.controller.determinize(name))
            self.outer_section.control_section.load_auto(name)
            self.outer_section.set_message("Successfully made automaton total")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def concat(self, name1: str, name2: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name1,
                self.outer_section.controller.intersection(name1, name2))
            self.outer_section.control_section.load_auto(name1)
            self.outer_section.set_message("Successfully intersected automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def minimize(self, name: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
            self.outer_section.controller.minimize(name))
            self.outer_section.control_section.load_auto(name)
            self.outer_section.set_message("Successfully minimized automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def intersect(self, name1: str, name2: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name1,
            self.outer_section.controller.intersection(name1, name2))
            self.outer_section.control_section.load_auto(name1)
            self.outer_section.set_message("Successfully concatenated automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])
        except ValueError as error:
            self.outer_section.set_message(error.args[0])

    def union(self, name1: str, name2: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name1,
            self.outer_section.controller.union(name1, name2))
            self.outer_section.control_section.load_auto(name1)
            self.outer_section.set_message("Successfully united automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    def star(self, name: str):
        try:
            self.outer_section.controller.replace_or_add_automaton(name,
             self.outer_section.controller.star(name))
            self.outer_section.control_section.load_auto(name)
            self.outer_section.set_message("Successfully applied Kleene star constr to automaton")
        except KeyError as error:
            self.outer_section.set_message(error.args[0])

    # Operation section

class OperationSection:
    """Class that handles"""
    def __init__(self, frame, outer_section: App) -> None:
        self.section = ttk.Frame(frame)
        self.outer_section = outer_section
        self.auto_image_label = ttk.Label(self.section)
        self.auto_image_label.grid(column=1, row=2)
        self.name_label = ttk.Label(self.section,
         text="Name: ")
        self.name_label.grid(column=2)
        self.input_section = InputSection(self.section, self)
        self.buttons_section = ButtonSection(self.section, self)

class InputSection:
    """Class that handles state and transition input."""
    def __init__(self, frame: ttk.Frame, outer_section: OperationSection) -> None:
        self.outer_section = outer_section
        self.input_section = ttk.Frame(frame)
        self.accepts_word_entry = ttk.Entry(self.input_section, width=30)
        self.accepts_word_entry.insert(0, "Type word")
        self.accepts_word_entry.grid()
        self.accepts_button = ttk.Button(self.input_section, text="Accepts word",
        command=lambda: self.accepts_word(self.accepts_word_entry.get()))
        self.accepts_button.grid()
        self.state_entry = ttk.Entry(self.input_section, width=30)
        self.state_entry.grid(pady=5, padx=10)
        self.state_entry.insert(0, 'State: name')
        self.transition_entry = ttk.Entry(self.input_section, width=30)
        self.transition_entry.insert(0, "Transitions: name letter name")
        self.transition_entry.grid()
        self.state_entry.grid()
        self.input_section.grid(column=2, row=2)

    def accepts_word(self, word):
        try:
            current_auto_name = self.outer_section.outer_section.current_auto_name
            self.outer_section.outer_section.set_message("Word is ACCEPTED"
                if self.outer_section.outer_section.controller.accepts_word(current_auto_name, word)
                 else "Word is REJECTED")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

class ButtonSection:
    """Class that handles basic automatons operations (managing state, transitions, etc.)."""
    def __init__(self, frame: ttk.Frame, outer_section: OperationSection) -> None:
        self.buttons_section = ttk.Frame(frame)
        self.outer_section = outer_section
        self.remove_state_button = ttk.Button(self.buttons_section, text="Remove state",
        command=lambda: self.remove_state(self.outer_section.input_section.state_entry.get()))
        self.add_state_button = ttk.Button(self.buttons_section, text="Add state",
        command=lambda: self.add_state(self.outer_section.input_section.state_entry.get()))
        self.remove_final_button = ttk.Button(self.buttons_section, text="Make unfinal",
        command=lambda: self.remove_final(self.outer_section.input_section.state_entry.get()))
        self.add_final_button = ttk.Button(self.buttons_section, text="Make final",
        command=lambda: self.add_final(self.outer_section.input_section.state_entry.get()))
        self.add_start_button = ttk.Button(self.buttons_section, text="Make start",
        command=lambda: self.add_start(self.outer_section.input_section.state_entry.get()))
        self.remove_start_button = ttk.Button(self.buttons_section, text="Remove start",
        command=lambda: self.remove_start(self.outer_section.input_section.state_entry.get()))
        self.add_transition_button = ttk.Button(self.buttons_section, text="Add transition",
        command=lambda: self.add_transition(\
            self.outer_section.input_section.transition_entry.get()))
        self.remove_transition_button = ttk.Button(self.buttons_section, text="Remove transition",
        command=lambda: self.remove_transition(\
            self.outer_section.input_section.transition_entry.get()))
        self.render()

    def render(self):
        self.add_state_button.grid(row=3, column=1, padx=5)
        self.remove_state_button.grid(row=3, column=2, padx=5)
        self.add_start_button.grid(row=4, column=1, padx=5)
        self.remove_start_button.grid(row=4, column=2, padx=5)
        self.add_final_button.grid(row=5, column=1, padx=5)
        self.remove_final_button.grid(row=5, column=2, padx=5)
        self.add_transition_button.grid(row=6, column=1, padx=5)
        self.remove_transition_button.grid(row=6, column=2)
        self.buttons_section.grid(row=4, column=2, padx=5)

    def add_transition(self, raw: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            tokens = raw.split(' ')
            controller.add_transition(current_auto_name, tokens[0], tokens[1], tokens[2])
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed state!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
        except IndexError:
            self.outer_section.outer_section.set_message("Invalid input!")

    def remove_transition(self, raw: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            tokens = raw.split(' ')
            controller.remove_transition(current_auto_name, tokens[0], tokens[1], tokens[2])
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed state!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
        except IndexError:
            self.outer_section.outer_section.set_message("Invalid input!")

    def remove_final(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.make_state_unfinal(current_auto_name, label)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed from finals!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_final(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.make_state_final(current_auto_name, label)
            controller.show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully added to finals!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_start(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.set_start(current_auto_name, label)
            controller.show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully added to starts!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def remove_start(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.remove_start(current_auto_name, label)
            controller.show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed from start!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def remove_state(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.remove_state(current_auto_name, label)
            controller.show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
            self.outer_section.outer_section.set_message("Successfully removed state!")
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])

    def add_state(self, label: str):
        try:
            control_section = self.outer_section.outer_section.control_section
            controller = self.outer_section.outer_section.controller
            current_auto_name = self.outer_section.outer_section.current_auto_name
            controller.add_state(current_auto_name, label)
            controller.show_automaton(current_auto_name)
            control_section.load_auto(current_auto_name)
        except KeyError as error:
            self.outer_section.outer_section.set_message(error.args[0])
