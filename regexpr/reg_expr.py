"""Module for working with regular expressions."""
from typing import List

from automation.automation import Automaton

def is_letter(symbol: str) -> bool:
        return symbol.isalpha() or symbol.isdigit()

class RegExpr:
    """Class for working with regular expressions."""

    def __init__(self, regex: str):
        self.regex = regex

    def validate(self) -> bool:
        """Function for checking if regex is valid."""
        # TODO: Ask Stoycho how to validate expressions via regular expressions.
        return self.__validate()

    def convert_in_RPN(self) -> str:
        """Converts regex into reverse polish notation."""
        output: List[str] = []
        stack: List[str] = []
        for i in range(len(self.regex)):
            symbol: str = self.regex[i]
            if symbol.isalpha() or symbol.isdigit() or symbol == '$':
                output.append(symbol)
            elif symbol == '(':
                stack.append(symbol)
            elif symbol == '*':
                output.append(symbol)
            elif symbol == ')':
                while stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            elif symbol == '+':
                while stack and (stack[-1] == '.' or stack[-1] == '+'):
                    output.append(stack.pop())
                stack.append(symbol)
            if i != len(self.regex) - 1:
                left: str = self.regex[i]
                right: str = self.regex[i + 1]
                if is_letter(left) and (right == '(' or is_letter(right))\
                    or left == ')' and (is_letter(right) or right == ')')\
                        or left == '*' and (right == '(' or is_letter(right)):
                        while stack and (stack[-1] == '.' or stack[-1] == '*'):
                            output.append(stack.pop())
                        stack.append('.')
        while stack:
            output.append(stack.pop())
        return "".join(output)

    def __validate(self) -> bool:
        return False

    def compile(self) -> Automaton:
        """Reads regular expression and returns """
        regex_RPN: str = self.convert_in_RPN()
        stack: List[Automaton] = []
        for symbol in regex_RPN:
            if symbol == '+':
                a: Automaton = stack.pop()
                b: Automaton = stack.pop()
                stack.append(a.union(b).determinize())
            elif symbol == '*':
                starred: Automaton = stack.pop()
                stack.append(starred.star().determinize())
            elif symbol == '.':
                concat_1: Automaton = stack.pop()
                concat_2: Automaton = stack.pop()
                stack.append(concat_2.concat(concat_1).determinize())
            elif symbol == '$':
                stack.append(Automaton.singleton_epsilon())
            else:
                stack.append(Automaton.by_letter(symbol))
        return stack[-1].minimize()

