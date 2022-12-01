from tkinter import *
from PIL import ImageTk
from PIL import Image as Img
from controller.controller import Controller

root = Tk()
root.geometry(newGeometry="700x700")
global c
c = Controller()
c.load_from_file()

current_auto_name = ""

message_label = Label(root)
message_label.grid(row=0)

# Control section

class ControlSection:
    def __init__(self, frame) -> None:
        self.control_section = Frame(frame)
        self.name_entry = Entry(self.control_section, width=50)
        self.name_entry.insert(0, "Name ")
        self.name_entry.grid(row=1)
        self.regex_entry = Entry(self.control_section, width=50)
        self.regex_entry.insert(0, "Regex/name of automaton")
        self.regex_entry.grid(row=2)
        self.load_button = Button(self.control_section, text="Load!",
         command=lambda: self.load_auto(self.name_entry.get()))
        self.save_button = Button(self.control_section, text="Save!", 
        command=lambda: self.saveAuto(self.name_entry.get()))
        self.save_button.grid(row=1, column=3)
        self.remove_button = Button(self.control_section, text="Remove!", 
        command=lambda: self.removeAuto(self.name_entry.get()))
        self.remove_button.grid(row=2, column=3)
        self.load_button.grid(row=1, column=2)
        self.create_button = Button(self.control_section, text="Create!", 
        command=lambda: self.createAuto(self.name_entry.get(),
             self.regex_entry.get()))
        self.create_button.grid(row=2, column=2)
        self.control_section.grid(row=1)
    def load_auto(self, name):
        try:
            c.show_automaton(name)
            change_name(name)
            if operations_section:
                operations_section.grid_forget()
            load_image()
            operations_section.grid(row=6)
        except KeyError as error:
            set_message(error.args[0])

    def createAuto(self, name: str, operation: str) -> None:
        try:
            c.replace_or_add_automaton(name, c.from_regex(operation))
            self.load_auto(name)
            print("Done!")
            set_message("Automation created successfully.")
        except KeyError as error:
            set_message(error.args[0])

    def removeAuto(self, name):
        global current_auto_name

        try:
            c.remove_automaton(name)
            if current_auto_name == name:
                hideImage()
                current_auto_name = ""
            set_message("Automation removed successfully.")
        except KeyError as error:
            set_message(error.args[0])

    def saveAuto(self, name):
        try:
            c.save_in_file()
            set_message("Automatons saved successfully.")
        except KeyError as error:
            set_message(error.args[0])

controlSection = ControlSection(root)

# Construction section

class ConstructionSection:
    def __init__(self) -> None:
        self.construction_section = Frame(root)
        self.determinize_button = Button(self.construction_section, text="Determinize",
        command=lambda: self.determinize(controlSection.name_entry.get()))
        self.minimize_button = Button(self.construction_section, text="Minimize",
        command=lambda: self.minimize(controlSection.name_entry.get()))
        self.concat_button = Button(self.construction_section, text="Concat",
        command=lambda: self.concat(controlSection.name_entry.get(), controlSection.regex_entry.get()))
        self.union_button = Button(self.construction_section, text="Union",
        command=lambda: self.union(controlSection.name_entry.get(), controlSection.regex_entry.get()))
        self.star_button = Button(self.construction_section, text="Kleene star",
        command=lambda: self.star(controlSection.name_entry.get()))
        self.total_button = Button(self.construction_section, text="Make total",
        command=lambda: self.total(controlSection.name_entry.get()))
        self.intersection_button = Button(self.construction_section, text="Intersection",
        command=lambda: self.intersect(controlSection.name_entry.get(), controlSection.regex_entry.get()))
        self.complement_button = Button(self.construction_section, text="Complement", 
        command=lambda: self.complement(controlSection.name_entry.get()))
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

    def complement(self, name):
        try:
            c.replace_or_add_automaton(name, c.complement(name))
            controlSection.load_auto(name)
            set_message("Successfully made automaton complement")
        except KeyError as error:
            set_message(error.args[0])

    def determinize(self, name):
        try:
            c.replace_or_add_automaton(name, c.determinize(name))
            controlSection.load_auto(name)
            set_message("Successfully determinized automaton")
        except KeyError as error:
            set_message(error.args[0])

    def total(self, name):
        try:
            c.replace_or_add_automaton(name, c.determinize(name))
            controlSection.load_auto(name)
            set_message("Successfully made automaton total")
        except KeyError as error:
            set_message(error.args[0])

    def concat(self, name1, name2):
        try:
            c.replace_or_add_automaton(name1, c.intersection(name1, name2))
            controlSection.load_auto(name1)
            set_message("Successfully intersected automaton")
        except KeyError as error:
            set_message(error.args[0])

    def minimize(self, name):
        try:
            c.replace_or_add_automaton(name, c.minimize(name))
            controlSection.load_auto(name)
            set_message("Successfully minimized automaton")
        except KeyError as error:
            set_message(error.args[0])

    def intersect(self, name1, name2):
        try:
            c.replace_or_add_automaton(name1, c.concat(name1, name2))
            controlSection.load_auto(name1)
            set_message("Successfully concatenated automaton")
        except KeyError as error:
            set_message(error.args[0])

    def union(self, name1, name2):
        try:
            c.replace_or_add_automaton(name1, c.union(name1, name2))
            controlSection.load_auto(name1)
            set_message("Successfully united automaton")
        except KeyError as error:
            set_message(error.args[0])

    def star(self, name):
        try:
            c.replace_or_add_automaton(name, c.star(name))
            controlSection.load_auto(name)
            set_message("Successfully applied Kleene star constr to automaton")
        except KeyError as error:
            set_message(error.args[0])

construction_section = ConstructionSection()

    # Operation section

operations_section = Frame(root)
auto_image_label = Label(operations_section)
auto_image_label.grid(column=1, row=2)

    # Input section

input_section = Frame(operations_section)

accepts_word_entry = Entry(input_section, width=30)
accepts_word_entry.insert(0, "Type word")
accepts_word_entry.grid()
accepts_button = Button(input_section, text="Accepts word",
command=lambda: accepts_word(accepts_word_entry.get()))
accepts_button.grid()

state_entry = Entry(input_section, width=30)
state_entry.grid(pady=5, padx=10)
state_entry.insert(0, 'State: name')
transition_entry = Entry(input_section, width=30)
transition_entry.insert(0, "Transitions: name letter name")
transition_entry.grid()
state_entry.grid()
input_section.grid(column=2)

# Button section

buttons_section = Frame(operations_section)
remove_state_button = Button(buttons_section, text="Remove state",
 command=lambda: remove_state(state_entry.get()))
add_state_button = Button(buttons_section, text="Add state",
 command=lambda: add_state(state_entry.get()))
remove_final_button = Button(buttons_section, text="Make unfinal",
command=lambda: remove_final(state_entry.get()))
add_final_button = Button(buttons_section, text="Make final",
command=lambda: add_final(state_entry.get()))
add_start_button = Button(buttons_section, text="Make start",
command=lambda: add_start(state_entry.get()))
remove_start_button = Button(buttons_section, text="Remove start",
command=lambda: removeStart(state_entry.get()))
add_transition_button = Button(buttons_section, text="Add transition",
command=lambda: add_transition(transition_entry.get()))
remove_transition_button = Button(buttons_section, text="Remove transition",
command=lambda: remove_transition(transition_entry.get()))

add_state_button.grid(row=2, column=1, padx=5)
remove_state_button.grid(row=2, column=2, padx=5)
add_start_button.grid(row=3, column=1, padx=5)
remove_start_button.grid(row=3, column=2, padx=5)
add_final_button.grid(row=4, column=1, padx=5)
remove_final_button.grid(row=4, column=2, padx=5)
add_transition_button.grid(row=5, column=1, padx=5)
remove_transition_button.grid(row=5, column=2)
buttons_section.grid(row=4, column=2, padx=5)

# Functions

def accepts_word(word):
    global current_auto_name

    try:
        set_message("Word is ACCEPTED" if c.accepts_word(current_auto_name, word)
             else "Word is REJECTED")
    except KeyError as error:
        set_message(error.args[0])

def add_transition(raw):
    global current_auto_name

    try:
        tokens = raw.split(' ')
        c.add_transition(current_auto_name, tokens[0], tokens[1], tokens[2])
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])
    except IndexError as error:
        set_message("Invalid input!")

def remove_transition(raw):
    global current_auto_name

    try:
        tokens = raw.split(' ')
        c.remove_transition(current_auto_name, tokens[0], tokens[1], tokens[2])
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])
    except IndexError as error:
        set_message("Invalid input!")

def remove_final(label):
    global current_auto_name

    try:
        c.make_state_unfinal(current_auto_name, label)
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])

def add_final(label):
    global current_auto_name

    try:
        c.make_state_final(current_auto_name, label)
        c.show_automaton(current_auto_name)
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])

def add_start(label):
    global current_auto_name

    try:
        c.set_start(current_auto_name, label)
        c.show_automaton(current_auto_name)
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])

def removeStart(label):
    global current_auto_name

    try:
        c.remove_start(current_auto_name, label)
        c.show_automaton(current_auto_name)
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])

def remove_state(label):
    global current_auto_name

    try:
        c.remove_state(current_auto_name, label)
        c.show_automaton(current_auto_name)
        controlSection.load_auto(current_auto_name)
        set_message("Successfully removed state!")
    except KeyError as error:
        set_message(error.args[0])

def add_state(label):
    global current_auto_name

    try:
        c.add_state(current_auto_name, label)
        c.show_automaton(current_auto_name)
        controlSection.load_auto(current_auto_name)
    except KeyError as error:
        set_message(error.args[0])

def set_message(message):
    global message_label

    if message_label:
        message_label.grid_forget()
    message_label = Label(root, text=message)
    message_label.grid()
    message_label.grid(row=0)

def load_image():
    global operations_section
    global auto_image_label

    if auto_image_label:
        auto_image_label.grid_forget()
    stgImg = PhotoImage(file="automaton.gv.png")
    auto_image_label = Label(operations_section, image=stgImg)
    auto_image_label.image = stgImg
    auto_image_label.grid(row=1, column=1, rowspan=10)
    root.update_idletasks()

def change_name(name):
    global current_auto_name
    current_auto_name = name

def hideImage():
    global auto_image_label

    if auto_image_label:
        auto_image_label.grid_forget()



root.mainloop()