from automation.regexpr.reg_expr import RegExpr
from automation.automaton.automaton import Automaton

def test_validate():
    regex = RegExpr("(a+b)*aba(a+b)*")
    assert regex.validate()
    regex = RegExpr("(a++b)**")
    assert not regex.validate()
    regex = RegExpr("(a+b)**")
    assert regex.validate()
    regex = RegExpr("(a+b)()")
    assert not regex.validate()

def test_compile():
    regex = RegExpr("(a+b)*aba(a+b)*")
    a = regex.compile()
    assert len(a.states) == 4
    assert a.accepts_word("bbbababbb")
    assert a.accepts_word("aba")
    assert a.accepts_word("bbbbaba")
    assert not a.accepts_word("ab")
    assert a.get_state('0') in a.transitions[a.get_state('2')]['b']
    assert a.get_state('1') in a.transitions[a.get_state('0')]['a']
    assert a.get_state('3') in a.finals
    assert a.get_state('0') in a.starts
    assert a.is_deterministic()
    assert a.is_total()
