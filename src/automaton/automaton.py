"""Module providing the crusial functionality for the project."""

from __future__ import annotations
from typing import Set, Dict, List
import copy
import os

class State:
    """State in a nutshell"""
    def __init__(self, label: str = "") -> None:
        self.label = label
    def change_label(self, label: str):
        """Function that changes labels"""
        self.label = label
    def __repr__(self) -> str:
        return self.label

class Automaton:
    """The main class in the project. It holds the functionality an automaton should have:
        1. Managing internal properties: removing/adding/changing states.
        2. Saving automaton in file.
        3. Basic operations: concatenation, union, Kleene star, complement
        4. Making automaton deterministic
        5. Minifying automaton
        6. etc"""
    def __init__(self) -> None:
        self.alphabet: Set[str] = set()
        self.starts: Set[State] = set()
        self.states: List[State] = []
        self.states_dict: Dict[str, int] = {}
        self.transitions: Dict[State, Dict[str, Set[State]]] = {}
        self.finals: Set[State] = set()

    def add_state(self, label: str = "") -> None:
        """Function for adding state"""
        label = str(len(self.states)) if not label or label in self.states_dict else label
        self.states.append(State(label))
        self.states_dict[label] = len(self.states) - 1

    def remove_state(self, label: str) -> bool:
        """Removes state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index >= len(self.states) or index < 0:
            return False

        # If finals or starts include the state, remove it from there.
        self.finals = {state for state in self.finals if state is not self.states[index]}
        self.starts = {state for state in self.starts if state is not self.states[index]}

        # Remove the state transitions.
        if self.states[index] in self.transitions:
            del self.transitions[self.states[index]]
        for state, transitions in self.transitions.items():
            for letter in transitions:
                if self.states[index] in transitions[letter]:
                    transitions[letter].remove(self.states[index])

        # Delete state from states.
        self.states.pop(index)
        del self.states_dict[label]
        return True

    def make_state_final(self, label: str) -> bool:
        """State becomes final"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or index >= len(self.states) or self.states[index] in self.finals:
            return False
        self.finals.add(self.states[index])
        return True

    def make_state_unfinal(self, label: str) -> bool:
        """State becomes final"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or index >= len(self.states) or not self.states[index] in self.finals:
            return False
        self.finals.remove(self.states[index])
        return True

    def set_start(self, label: str) -> bool:
        """Setting start state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or self.states[index] in self.starts:
            return False
        self.starts.add(self.states[index])
        return True

    def remove_start(self, label: str) -> bool:
        """Removing start state"""
        index: int = self.states_dict[label] if label in self.states_dict else -1
        if index < 0 or self.states[index] not in self.starts:
            return False
        self.starts.remove(self.states[index])
        return True

    def __add_transition_by_index(self, idx1: int, letter: str, idx2: int) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        # If indexes are not valid, return.
        if idx1 < 0 or idx1 >= len(self.states):
            return False
        if idx2 < 0 or idx2 >= len(self.states):
            return False

        # If letter is not in alphabet, add it.
        if letter not in self.alphabet:
            self.alphabet.add(letter)

        state_1: State = self.states[idx1]
        state_2: State = self.states[idx2]

        # Add the transition
        if state_1 not in self.transitions:
            self.transitions[state_1] = {letter: set([state_2])}
        elif letter not in self.transitions[state_1]:
            self.transitions[state_1][letter] = set([state_2])
        # It is not allowed to have two same transitions in automaton.
        elif state_2 in self.transitions[state_1][letter]:
            return False
        else:
            self.transitions[state_1][letter].add(state_2)
        return True

    def add_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Adding new transition from state with index idx1 to state
        with index idx2 with letter 'letter'"""
        idx1: int = self.states_dict[label1] if label1 in self.states_dict else -1
        idx2: int = self.states_dict[label2] if label2 in self.states_dict else -1
        return self.__add_transition_by_index(idx1, letter, idx2)

    def add_transitions(self, label1: str, letter, states: Set[State]) -> bool:
        """Adds many transitions at a time."""
        states_labels: List[str] = [state.label for state in states]
        for state_label in states_labels:
            if not self.add_transition(label1, letter, state_label):
                return False
        return True

    def remove_transition(self, label1: str, letter: str, label2: str) -> bool:
        """Removes transition."""
        if self.get_state(label1) not in self.transitions\
             or letter not in self.transitions[self.get_state(label1)]\
            or label2 not in self.states_dict\
                or self.get_state(label2) not in self.transitions[self.get_state(label1)][letter]:
            return False
        self.transitions[self.get_state(label1)][letter].remove(self.get_state(label2))
        return True

    def __get_state_transitions_by_index(self, index: int) -> Dict[str, Set[State]]:
        """Get transitions of state with index 'index'. It is a helper function
        for Automaton.get_state_transitions."""
        if index < 0 or index >= len(self.states):
            return {}
        state: State = self.states[index]
        return self.transitions[state] if state in self.transitions else {}

    def get_state_transitions(self, state: State) -> Dict[str, Set[State]]:
        """Get transitions of state with index 'index'."""
        return self.__get_state_transitions_by_index(self.states_dict[state.label]\
            if state.label in self.states_dict else -1)

    def accepts_word(self, word: str) -> bool:
        """Checks if word is in the automaton language."""
        states: Set[State] = set(self.starts)
        for letter in word:
            new_states: Set[State] = set()
            for state in states:
                state_transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
                if letter in state_transitions:
                    new_states = new_states | set(state_transitions[letter])
            states = new_states
        for state in states:
            if state in self.finals:
                return True
        return False

    def copy(self) -> Automaton:
        """Returns a deep copy of the automation"""
        return copy.deepcopy(self)

    def is_deterministic(self) -> bool:
        """Checks if automaton is deterministic."""
        for state in self.states:
            state_transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if letter in state_transitions and len(state_transitions[letter]) > 1:
                    return False
        return True

    def is_total(self) -> bool:
        """Checks if automaton is total (for each state for each
         letter exists transition from state with letter)"""
        for state in self.states:
            state_transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in state_transitions or not state_transitions[letter]:
                    return False
        return True

    def make_total(self) -> None:
        """Makes automaton total."""
        if self.is_total():
            return
        trash_label = "t" if "t" not in self.states_dict else str(len(self.states))
        self.add_state(trash_label)
        trash_state_idx = len(self.states) - 1
        for letter in self.alphabet:
            self.__add_transition_by_index(trash_state_idx, letter, trash_state_idx)
        for state in self.states:
            state_transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
            for letter in self.alphabet:
                if not letter in state_transitions:
                    self.add_transition(state.label, letter, trash_label)

    def total(self) -> Automaton:
        """Returns a totalized copy of the automaton."""
        result: Automaton = self.copy()
        result.make_total()
        return result

    def get_state(self, label: str) -> State:
        """Returns state by label."""
        return self.states[self.states_dict[label]] if label in self.states_dict else State()

    def union(self, auto: Automaton) -> Automaton:
        """Unites automatons following the Kleene's theorem algorithm."""
        if self is auto:
            return self
        result: Automaton = self.copy()
        other_auto: Automaton = auto.copy()
        for state in other_auto.states:
            if state.label in result.states_dict:
                del other_auto.states_dict[state.label]
                state.label = str(len(result.states))
                other_auto.states_dict[state.label] = len(result.states)
            result.add_state(state.label)
        for state in other_auto.transitions:
            for letter in other_auto.transitions[state]:
                result.add_transitions(state.label, letter, other_auto.transitions[state][letter])
        for final in other_auto.finals:
            result.make_state_final(final.label)
        for start in other_auto.starts:
            result.set_start(start.label)
        return result

    def concat(self, auto) -> Automaton:
        """Returns an automaton with language L(self) . L(auto)."""
        result: Automaton = self.copy()
        other_auto: Automaton = auto.copy()

        # The algorithm follows the Kleene construction literally.
        # Renames all states in other_auto which have duplicate labels
        # with labels in result and adds them in result.
        for value in other_auto.states:
            state: State = value
            if state.label in result.states_dict:
                del other_auto.states_dict[state.label]
                state.label = str(len(result.states))
                other_auto.states_dict[state.label] = len(result.states)
            result.add_state(state.label)

        for final in result.finals:
            for start in other_auto.starts:
                start_transitions: Dict[str, Set[State]] = other_auto.transitions[start]\
                     if start in other_auto.transitions else {}
                for letter in start_transitions:
                    result.add_transitions(final.label, letter, start_transitions[letter])

        for state in other_auto.transitions:
            for letter in other_auto.transitions[state]:
                result.add_transitions(state.label, letter, other_auto.transitions[state][letter])


        # If there is a starting state amongst finals, the result finals are
        # self.finals U other.finals. Else result finals are other.finals.
        if not set(other_auto.starts).intersection(set(other_auto.finals)):
            result.finals = set()
        for final in other_auto.finals:
            result.make_state_final(final.label)
        return result

    def complement(self) -> Automaton:
        """Returns automaton with complement language."""
        # Automaton must be deterministic (or total).
        if not self.is_total():
            raise ValueError("Automaton is not deterministic.")

        result: Automaton = self.copy()
        if not result.is_total():
            result.make_total()
        old_finals: Set[State] = set(result.finals)
        result.finals = {state for state in result.states if state not in old_finals}
        return result

    def star(self) -> Automaton:
        """Returns automaton with language L(self)*.
        The algorithm derives directly from Kleene's theorem."""
        result: Automaton = self.copy()

        # For every final f add transitions
        # of all starting states (for every start
        # and every letter: add transitions from start
        # with the letter).
        for final in result.finals:
            for start in result.starts:
                transitions: Dict[str, Set[State]] = self.get_state_transitions(start)
                for letter in transitions:
                    result.add_transitions(final.label, letter, transitions[letter])

        # Add a new state to add epsilon to L(result).
        start_label = str(len(result.states))
        result.add_state(start_label)
        result.starts.add(result.get_state(start_label))
        result.make_state_final(start_label)
        return result

    def intersection(self, other_auto: Automaton) -> Automaton:
        """Returns an automaton with language L(self) ^ L(other_auto).
        The algorithm uses the technique of parallel automatons processing
        (the states are ordered pairs)."""

        # The automatons must have same alphabet.
        if len(set(self.alphabet).intersection(set(other_auto.alphabet))) != len(self.alphabet):
            raise ValueError("Automations don't have same alphabet.")

        # Both have to be deterministic.
        if not self.is_deterministic() or not other_auto.is_deterministic():
            raise ValueError("Automaton is not deterministic.")
        result: Automaton = Automaton()
        result.alphabet = set(self.alphabet)

        # Adds result states as ordered pairs: states labels are
        # {label_from_self}x{label_from_other} for all states
        # from self and other_auto.
        for state_1 in self.states:
            for state_2 in other_auto.states:
                result.add_state(f"{state_1.label}x{state_2.label}")
        for state_1 in self.starts:
            for state_2 in other_auto.starts:
                result.set_start(f"{state_1.label}x{state_2.label}")

        for state in result.states:
            tokens: List[str] = state.label.split("x")
            transitions_1: Dict[str, Set[State]] =\
                 self.get_state_transitions(self.get_state(tokens[0]))
            transitions_2: Dict[str, Set[State]] =\
                 other_auto.get_state_transitions(other_auto.get_state(tokens[1]))

            # forall q in self.states forall p in other.states
            #   forall l in self.alphabet forall transitions t1 of q with
            #       letter l forall transitions t2 of p with letter l:
            #           t1, t2 are in delta("qxp", l)
            # This the idea implemented below.
            for letter in transitions_1:
                if letter in transitions_2:
                    for s_1 in transitions_1[letter]:
                        for s_2 in transitions_2[letter]:
                            result.add_transition(state.label, letter, f"{s_1.label}x{s_2.label}")

        # Both components have to be starting states in order to make the pair starting.
        result.starts = {state for state in result.states
            if self.states[self.states_dict[state.label.split("x")[0]]] in self.starts
                and other_auto.states[self.states_dict[state.label.split("x")[1]]]\
                    in other_auto.starts}

        # Analogically for the final states.
        result.finals = {state for state in result.states
            if self.states[self.states_dict[state.label.split("x")[0]]] in self.finals
                and other_auto.states[self.states_dict[state.label.split("x")[1]]]\
                    in other_auto.finals}
        return result

    def rename(self) -> None:
        """Renames states."""
        count: int = 0
        self.states_dict = {}
        for state in self.states:
            state.label = str(count)
            self.states_dict[state.label] = count
            count += 1

    def determinize(self) -> Automaton:
        """Returns a determinized version of self. The algorithm is
        derived from the Rabin-Scott theorem."""
        result: Automaton = Automaton()
        result.alphabet = set(self.alphabet)

        queue: List[Set[State]] = []
        queue.append(self.starts)
        start_label: str = str(sorted({state.label for state in self.starts}))
        result.add_state(start_label)
        result.set_start(start_label)

        if len([state for state in self.starts if state in self.finals]) > 0:
            result.make_state_final(start_label)

        while queue:
            current: Set[State] = queue.pop(0)
            for letter in result.alphabet:
                states_set: Set[State] = set()

                for state in current:
                    transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
                    states_set = states_set.union(transitions[letter] if letter in transitions\
                         else set())

                set_label: str = str(sorted({state.label for state in states_set}))

                if not result.get_state(set_label).label:
                    queue.append(states_set)
                    result.add_state(set_label)
                    if [state for state in states_set if state in self.finals]:
                        result.make_state_final(set_label)

                result.add_transition(str(sorted(\
                    {state.label for state in current})), letter, set_label)

        result.rename()

        return result

    def minimize(self) -> Automaton:
        """Return a minimized automaton with same language.
        The algorithm follows the Bzozowski theorem: The determinized version
        of the automaton created with the construction for L(auto)^rev is
         the minimal automaton for L^rev."""
        return self.copy().determinize().reverse().determinize().reverse().determinize()

    def reverse(self) -> Automaton:
        """Returns an automaton with language L(self)^rev.
        The algorithm is as it follows:
        1. All finals become starts.
        2. All starts become finals.
        3. Change the direction of transitions."""
        result: Automaton = Automaton()
        for state in self.states:
            result.add_state(state.label)
        for start in self.starts:
            result.make_state_final(start.label)
        for final in self.finals:
            result.set_start(final.label)
        for state in result.states:
            transitions: Dict[str, Set[State]] = self.get_state_transitions(state)
            for letter in transitions:
                for res in transitions[letter]:
                    result.add_transition(res.label, letter, state.label)
        return result

    def left_arrow(self, label: str) -> Automaton:
        """Returns an automaton with language all the words that start from state {label}
        and when read in {self} automaton finish at final state."""
        result: Automaton = self.copy()
        result.finals = {result.get_state(label)}
        return result

    def right_arrow(self, label: str) -> Automaton:
        """Returns an automaton with language all the words that when
        read in the automaton would finish at state {label}."""
        result: Automaton = self.copy()
        result.starts = {result.get_state(label)}
        return result

    @staticmethod
    def by_letter(letter: str) -> Automaton:
        """Creates an automaton with language L = {letter}."""
        auto: Automaton = Automaton()
        auto.add_state()
        auto.add_state()
        auto.set_start("0")
        auto.make_state_final("1")
        auto.add_transition("0", letter, "1")
        return auto

    @staticmethod
    def singleton_epsilon() -> Automaton:
        """Creates an automaton with language L = {}."""
        auto: Automaton = Automaton()
        auto.add_state()
        auto.set_start("0")
        auto.make_state_final("0")
        return auto

    def __repr__(self) -> str:
        return "--- Automaton:\n" + "States = " + str(self.states) + \
        "\nStarting states: " + str(self.starts) \
            + "\nTransition function:\n" + "\n".join([f"--- {el} -> {el_dict}"\
                 for el, el_dict in self.transitions.items()]) + \
                "\nFinal states: " + str(self.finals)

    def save_in_file(self, path: List[str]) -> None:
        """Function for saving in file."""
        with open(os.path.join(*path), "w", encoding="UTF-8") as file:
            file.writelines(self.stream_format())
            file.close()

    def load_from_file(self, path: List[str]) -> None:
        """Loads automaton from file in the format of Automaton.stream_format function."""
        with open(os.path.join(*path), encoding="UTF-8") as file:
            states_labels: List[str] = file.readline().split(" ")
            for label in states_labels:
                self.add_state(label.replace("\n", ""))
            starts_labels: List[str] = file.readline().split(" ")
            for label in starts_labels:
                self.set_start(label.replace("\n", ""))
            rest: List[str] = file.read().split("\n")
            for i in range(len(rest) - 2):
                transitions_raw = rest[i].split(" ")
                start, letter, *targets = transitions_raw
                for target in targets:
                    self.add_transition(start, letter, target)
            final_labels: List[str] = rest[-2].split(" ")
            for label in final_labels:
                self.make_state_final(label)
            file.close()

    def stream_format(self) -> str:
        """Returns a string to save in file."""
        dict_to_list: List[str] = []
        for state, state_dict in self.transitions.items():
            for letter in state_dict:
                dict_to_list.append(f"{state.label} {letter} " + " ".join(\
                    [st.label for st in state_dict[letter]]))
        return "".join([" ".join(self.states_dict.keys()) + "\n",
                " ".join([start.label for start in self.starts]) + "\n",
                "\n".join(dict_to_list) + "\n",
                "f " + " ".join([final.label for final in self.finals]) + "\n"])
