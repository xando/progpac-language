from language import parser
from language import ast


def interpret(source):
    try:
        ast_tree = parser.parse(source)
        return ast.compile(ast_tree, source)
    except ValueError as e:
        return e.message



def test_steps():
    assert interpret("sss") == "sss"
    assert interpret("rsss") == "rsss"
    assert interpret("sssl") == "sssl"


def test_funcion():
    assert interpret("""
    f:sss
    f
    """) == "sss"

    assert interpret("""
    z:rrr
    f:sss
    fz
    """) == "sssrrr"

    assert interpret("""
    z:rrr
    f:sz
    f
    """) == "srrr"


def test_error_funcion_undefined():
    ret = interpret("z")

    assert 'Line:1, Column:1' in ret
    assert 'Function "z" is undefined.' in ret

    ret = interpret("""
    ssszf
    """)

    assert 'Line:2, Column:8' in ret
    assert 'Function "z" is undefined.' in ret


def test_error_funcion_arguments():
    ret = interpret("""
    f(A):sA
    f
    """)

    assert 'Line:3, Column:5' in ret
    assert 'Function "f" takes 1 arguments, 0 given' in ret

    ret = interpret("""
    f(A,B):sAB
    f(ss)
    """)

    assert 'Line:3, Column:5' in ret
    assert 'Function "f" takes 2 arguments, 1 given' in ret


def test_error_variable():
    ret = interpret("""
    B
    """)

    assert 'Line:2, Column:5' in ret
    assert 'Variable "B" is undefined' in ret

    ret = interpret("""
    f:B
    sssf
    """)

    assert 'Line:2, Column:7' in ret
    assert 'Variable "B" is undefined' in ret
