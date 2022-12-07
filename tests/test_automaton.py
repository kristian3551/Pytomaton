import pytest
from automation.automaton.automaton import Automaton

def test_add_state():
    a: Automaton = Automaton()
    a.add_state('0')
    assert len(a.states) == 1
    assert a.states[0].label == '0'
    a.add_state('1')
    assert len(a.states) == 2
    assert a.states[1].label == '1'

def test_remove_state():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.remove_state('1')
    assert len(a.states) == 1
    assert a.states[0].label == '0'
    assert not a.remove_state('invalid')

def test_make_final():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.make_state_final('1')
    assert len(a.finals) == 1
    assert '1' in {state.label for state in a.finals}

    assert not a.make_state_final('1')

def test_make_unfinal():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.make_state_final('1')
    assert not a.make_state_unfinal('invalid')
    a.make_state_unfinal('1')
    assert '1' not in {state.label for state in a.finals}

def test_set_start():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    assert not a.set_start('invalid')
    assert '0' in {state.label for state in a.starts}

def test_remove_start():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.set_start('1')
    a.remove_start('1')
    assert '1' not in {state.label for state in a.starts}
    assert not a.remove_start('invalid')

def test_add_transition():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    assert not a.add_transition('0', 'a', 'invalid')
    assert not a.add_transition('invalid', 'a', '1')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'b', '1')
    assert a.get_state('0') in a.transitions
    assert 'a' in a.transitions[a.get_state('0')]
    assert a.get_state('1') in a.transitions[a.get_state('0')]['a']
    assert a.get_state('1') in a.transitions
    assert 'b' in a.transitions[a.get_state('1')]
    assert a.get_state('1') in a.transitions[a.get_state('1')]['b']

def test_remove_transition():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('0', 'b', '1')
    a.remove_transition('0', 'a', '1')
    assert a.get_state('0') in a.transitions
    assert 'a' in a.transitions[a.get_state('0')]
    assert not a.transitions[a.get_state('0')]['a']

def test_get_transitions():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('0', 'b', '1')
    assert a.get_state('0') in a.transitions
    assert 'a' in a.get_state_transitions(a.get_state('0'))
    assert a.get_state('1') in a.get_state_transitions(a.get_state('0'))['a']

def test_accepts_word():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_state('2')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('0', 'b', '2')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    a.add_transition('2', 'a', '2')
    a.add_transition('2', 'b', '2')
    assert a.accepts_word('aabbbbbb')
    assert a.accepts_word('aaaaabbbbbb')
    assert a.accepts_word('a')
    assert not a.accepts_word('bbbabab')

def test_is_deterministic():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_state('2')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('0', 'b', '2')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    a.add_transition('2', 'a', '2')
    a.add_transition('2', 'b', '2')
    assert a.is_deterministic()
    a.add_transition('1', 'a', '2')
    assert not a.is_deterministic()

def test_is_total():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_state('2')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('0', 'b', '2')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    a.add_transition('2', 'a', '2')
    a.add_transition('2', 'b', '2')
    assert a.is_total()
    a.remove_transition('1', 'b', '1')
    assert not a.is_total()

def test_make_total():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_state('2')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    assert not a.is_total()
    a.make_total()
    assert a.is_total()
    assert a.get_state('t') in a.states
    assert a.get_state('t') in a.transitions[a.get_state('0')]['b']

def test_total():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.add_state('2')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    total_a = a.total()
    assert total_a.is_total()
    assert total_a.get_state('t') in total_a.states
    assert total_a.get_state('t') in total_a.transitions[total_a.get_state('0')]['b']

def test_union():
    a1: Automaton = Automaton()
    a1.add_state('0')
    a1.add_state('1')
    a1.add_transition('0', 'a', '1')
    a2: Automaton = Automaton()
    a2.add_state('0')
    a2.add_state('1')
    a2.make_state_final('1')
    a2.add_transition('0', 'b', '1')
    union: Automaton = a1.union(a2)
    assert len(union.states) == 4
    assert union.get_state('1') in union.transitions[union.get_state('0')]['a']
    assert union.get_state('3') in union.transitions[union.get_state('2')]['b']
    assert union.get_state('3') in union.finals

def test_concat():
    a1: Automaton = Automaton()
    a1.add_state('0')
    a1.add_state('1')
    a1.set_start('0')
    a1.add_transition('0', 'a', '1')
    a1.make_state_final('1')
    a2: Automaton = Automaton()
    a2.add_state('0')
    a2.add_state('1')
    a2.set_start('0')
    a2.make_state_final('1')
    a2.add_transition('0', 'b', '1')
    concat: Automaton = a1.concat(a2)
    assert len(concat.states) == 4
    assert concat.get_state('1') in concat.transitions[concat.get_state('0')]['a']
    assert concat.get_state('3') in concat.transitions[concat.get_state('1')]['b']
    assert concat.get_state('3') in concat.transitions[concat.get_state('2')]['b']
    assert concat.get_state('3') in concat.finals
    assert concat.get_state('0') in concat.starts

def test_star():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.add_transition('0', 'a', '1')
    a.make_state_final('1')
    star: Automaton = a.star()
    assert len(star.states) == 3
    assert star.get_state('1') in star.transitions[star.get_state('0')]['a']
    assert star.get_state('1') in star.transitions[star.get_state('1')]['a']
    assert star.get_state('1') in star.finals
    assert star.get_state('0') in star.starts
    assert star.get_state('2') in star.starts

def test_complement():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'a', '1')
    a.make_state_final('1')
    compl = a.complement()
    assert not compl.get_state('1') in compl.finals
    assert compl.get_state('0') in compl.finals
    a.add_transition('0', 'a', '0')

def test_complement_throws():
    with pytest.raises(ValueError):
        a: Automaton = Automaton()
        a.add_state('0')
        a.add_state('1')
        a.set_start('0')
        a.add_transition('0', 'a', '1')
        a.add_transition('0', 'a', '0')
        a.add_transition('1', 'a', '1')
        a.make_state_final('1')
        a.complement()

def test_determinize():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.make_state_final('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '0')
    a.add_transition('0', 'b', '0')
    a.add_transition('1', 'a', '1')
    a.add_transition('1', 'b', '1')
    determinize = a.determinize()
    assert len(determinize.states) == 1
    assert determinize.get_state('0') in determinize.starts
    assert determinize.get_state('0') in determinize.finals
    assert determinize.get_state('0') in determinize.transitions[\
        determinize.get_state('0')]['a']
    assert determinize.get_state('0') in determinize.transitions[\
        determinize.get_state('0')]['b']

def test_minimize():
    a: Automaton = Automaton.by_letter('a')
    b: Automaton = Automaton.by_letter('b')
    a_union_b = a.union(b)
    sigma_star = a_union_b.star()
    sigma_star = sigma_star.minimize()
    assert len(sigma_star.states) == 1
    assert sigma_star.get_state('0') in sigma_star.starts
    assert sigma_star.get_state('0') in sigma_star.finals
    assert sigma_star.get_state('0') in sigma_star.transitions[\
        sigma_star.get_state('0')]['a']
    assert sigma_star.get_state('0') in sigma_star.transitions[\
        sigma_star.get_state('0')]['b']

def test_reverse():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'b', '1')
    a.add_transition('1', 'a', '1')
    reverse = a.reverse()
    assert reverse.get_state('1') in reverse.starts
    assert reverse.get_state('0') in reverse.finals
    assert reverse.get_state('0') in reverse.transitions[reverse.get_state('1')]['a']
    assert reverse.get_state('1') in reverse.transitions[reverse.get_state('1')]['a']
    assert reverse.get_state('1') in reverse.transitions[reverse.get_state('1')]['b']

def test_stream_format():
    a: Automaton = Automaton()
    a.add_state('0')
    a.add_state('1')
    a.set_start('0')
    a.make_state_final('1')
    a.add_transition('0', 'a', '1')
    a.add_transition('1', 'b', '1')
    assert a.stream_format() == '0 1\n0\n0 a 1\n1 b 1\nf 1\n'


