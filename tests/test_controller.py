from automation.controller.controller import Controller
import pytest

def test_add_automaton():
    c = Controller()
    c.add_automaton('A', c.from_regex("(a+b)*aba"))
    assert 'A' in c.automatons
    assert c.automatons['A'].accepts_word("abbbbbbbaba")
    assert not c.automatons['A'].accepts_word("abbbbbbbabab")

def test_add_automaton_throws():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex("(a+b)*aba"))
        c.add_automaton('A', c.empty_automaton())

def test_remove_automaton():
    c = Controller()
    c.add_automaton('A', c.from_regex("(a+b)*aba"))
    c.remove_automaton('A')
    assert 'A' not in c.automatons

def test_remove_automaton_throws():
    with pytest.raises(KeyError):
        c = Controller()
        c.remove_automaton('B')

def test_replace_automaton():
    c = Controller()
    c.add_automaton('A', c.from_regex("(a+b)*aba"))
    c.replace_or_add_automaton('A', c.from_regex("(a+b)*aba(a+b)*"))
    assert c.automatons['A'].accepts_word("abbbabababbb")

def test_get_automaton():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex("(a+b)*aba"))
        assert c.get_automaton('A') is c.get_automaton('A')
        c.get_automaton('B')

