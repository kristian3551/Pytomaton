"""The actual GUI app. All of the application logic is performed in
an instance of Controller class, held in class App. Everything else is just hardcoded
GUI interface made with TKinter."""

from tkinter import ttk, Tk
from src.controller.controller import Controller # pyright: ignore[reportMissingImport]
from src.app.control_section import ControlSection
from src.app.construction_section import ConstructionSection
from src.app.operation_section import OperationSection

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
