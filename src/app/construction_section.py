"""Module containing all GUI widgets for performing constructions
on automatons."""
from tkinter import ttk
from typing import Dict

class ConstructionSection:
    """Class that handles all the logic behind
    performing basic automatons constructions."""
    def __init__(self, frame, outer_section) -> None:
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
