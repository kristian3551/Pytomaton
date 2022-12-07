"""Module for working with regular expressions."""
from typing import List

from automaton.automaton import Automaton

def is_letter(symbol: str) -> bool:
    """Checks if symbol is from alphabet."""
    return symbol.isalpha() or symbol.isdigit()

class RegExpr:
    """Class for working with regular expressions."""

    def __init__(self, regex: str):
        self.regex = regex

    def validate(self) -> bool:
        """Function for checking if regex is valid."""
        return self.__validate(self.regex)

    def convert_in_rpn(self) -> str:
        """Converts regex into reverse polish notation."""
        output: List[str] = []
        stack: List[str] = []
        for i, value in enumerate(self.regex):
            symbol: str = value
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
                cond_1: bool = is_letter(left) and (right == '(' or is_letter(right))
                cond_2: bool = left == ')' and (is_letter(right) or right == ')')
                cond_3: bool = left == '*' and (right == '(' or is_letter(right))
                if cond_1 or cond_2 or cond_3:
                    while stack and (stack[-1] == '.' or stack[-1] == '*'):
                        output.append(stack.pop())
                    stack.append('.')
        while stack:
            output.append(stack.pop())
        return "".join(output)

    def __validate(self, current: str) -> bool:
        """Helper for validating regex. It follows the inductive definition of building regexes."""
        # r -> r* | (r)
        # r1, r2 -> r1.r2 | r1 + r2
        if not current:
            return False
        if current == '$' or is_letter(current) or\
            current[0] == '(' and current[-1] == ')' and self.__validate(current[1:-1]):
            return True
        if current[-1] == '*' and self.__validate(current[0:-1]):
            return True
        for i, value in enumerate(current):
            symbol: str = value
            if symbol == '+' and self.__validate(current[0:i]) and self.__validate(current[i+1:]):
                return True
        for i in range(len(current)):
            if self.__validate(current[0:i]) and self.__validate(current[i:]):
                return True
        return False

    def compile(self) -> Automaton:
        """Reads valid regular expression and returns an automaton with same language."""
        # if not self.validate():
        #     print("Regular expression is NOT valid!")
        #     return Automaton()
        regex_rpn: str = self.convert_in_rpn()
        stack: List[Automaton] = []
        for symbol in regex_rpn:
            if symbol == '+':
                first: Automaton = stack.pop()
                second: Automaton = stack.pop()
                stack.append(first.union(second))
            elif symbol == '*':
                starred: Automaton = stack.pop()
                stack.append(starred.star())
            elif symbol == '.':
                concat_1: Automaton = stack.pop()
                concat_2: Automaton = stack.pop()
                stack.append(concat_2.concat(concat_1))
            elif symbol == '$':
                stack.append(Automaton.singleton_epsilon())
            else:
                stack.append(Automaton.by_letter(symbol))
        return stack[-1].minimize()
