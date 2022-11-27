"""Module for working with regular expressions."""
from typing import List, Set

# from automation.automation import Automaton

SYMBOLS: Set[str] = {"+", "*", "(", ")"}
OPERATIONS: Set[str] = {"+", "*"}

class RegExpr:
    """Class for working with regular expressions."""

    def __init__(self, regex: str):
        self.regex = regex

    def validate(self) -> bool:
        """Function for checking if regex is valid."""
        # TODO: Ask Stoycho how to validate expressions via regular expressions.
        return self.__validate(self.regex)

    def __validate(self, current: str) -> bool:
        return False

    def compile(self) -> None: # TODO: Edit return type!!!
        """Reads regular expression and returns """

expr: RegExpr = RegExpr("a+(ab*+b)*+")
print(expr.validate())