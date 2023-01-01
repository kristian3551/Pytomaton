import pytest
from src.controller.controller import Controller

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

def test_add_state():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_state('A', 'q')

def test_remove_state():
    with pytest.raises(KeyError):
        c = Controller()
        c.remove_state('A', 'q')

def test_remove_start():
    with pytest.raises(KeyError):
        c = Controller()
        c.remove_start('A', 'q')

def test_make_state_final():
    with pytest.raises(KeyError):
        c = Controller()
        c.make_state_final('A', 'q')

def test_make_state_unfinal():
    with pytest.raises(KeyError):
        c = Controller()
        c.make_state_unfinal('A', 'q')

def test_set_start():
    with pytest.raises(KeyError):
        c = Controller()
        c.set_start('A', 'q')

def test_add_transition():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_transition('A', '0', 'a', '1')

def test_remove_transition():
    with pytest.raises(KeyError):
        c = Controller()
        c.remove_transition('A', '0', 'a', '1')

def test_accepts_word():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex('a*b*'))
        assert c.accepts_word('A', 'aaaabbbb')
        assert c.accepts_word('A', 'bbbb')
        assert not c.accepts_word('A', 'bbbba')
        assert c.accepts_word('A', '')
        c.accepts_word('B', 'asdasd')

def test_total():
    with pytest.raises(KeyError):
        c = Controller()
        c.total('A')

def test_make_total():
    with pytest.raises(KeyError):
        c = Controller()
        c.make_total('A')

def test_union():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex('a*'))
        c.add_automaton('B', c.from_regex('b*'))
        assert c.union('A', 'B').accepts_word('aaaaaa')
        assert c.union('A', 'B').accepts_word('bbbb')
        assert c.union('A', 'B').accepts_word('')
        assert not c.union('A', 'B').accepts_word('aaaabbbbb')
        c.union('C', 'A')

def test_concat():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex('a*'))
        c.add_automaton('B', c.from_regex('b*'))
        assert c.concat('A', 'B').accepts_word('aaaaaa')
        assert c.concat('A', 'B').accepts_word('bbbb')
        assert c.concat('A', 'B').accepts_word('')
        assert c.concat('A', 'B').accepts_word('aaaabbbbb')
        c.concat('C', 'A')

def test_star():
    with pytest.raises(KeyError):
        c = Controller()
        c.star('B')

def test_complement():
    with pytest.raises(KeyError):
        c = Controller()
        c.complement('B')

def test_intersection():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex('ab*'))
        c.add_automaton('B', c.from_regex('a*b'))
        assert c.intersection('A', 'B').accepts_word('ab')
        assert not c.intersection('A', 'B').accepts_word('')
        assert not c.intersection('A', 'B').accepts_word('aaaabbb')
        c.intersection('C', 'A')

def test_determinize():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.empty_automaton())
        c.add_state('A', '0')
        c.add_state('A', '1')
        c.add_state('A', '2')
        c.add_transition('A', '0', 'a', '1')
        c.add_transition('A', '0', 'a', '2')
        c.add_transition('A', '0', 'b', '2')
        c.set_start('A', '0')
        c.make_state_final('A', '1')
        c.make_state_final('A', '2')
        det_auto = c.determinize('A')
        assert det_auto.accepts_word('a')
        assert det_auto.accepts_word('b')
        assert not det_auto.accepts_word('ab')
        assert not det_auto.accepts_word('')
        assert det_auto.is_deterministic()
        c.determinize('B')

def test_reverse():
    with pytest.raises(KeyError):
        c = Controller()
        c.add_automaton('A', c.from_regex('a*b*'))
        rev_auto = c.reverse('A')
        assert rev_auto.accepts_word('bbbbbaaaa')
        assert rev_auto.accepts_word('aaaa')
        assert rev_auto.accepts_word('')
        assert not rev_auto.accepts_word('aaaabbb')
        c.reverse('B')

