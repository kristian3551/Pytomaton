"""Module holding the logic behind inputs for managing automatons via GUI."""
from tkinter import ttk

class InputSection:
    """Class that handles state and transition input."""
    def __init__(self, frame: ttk.Frame, outer_section) -> None:
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
