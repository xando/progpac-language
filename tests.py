import parser
import ast


def parse(code):
    return parser.parse(code)


def test_step():
    ast_tree = parse("""
    s
    """)

    assert ast_tree.lines[0] == ast.Line([
        ast.Step('s')
    ])

    ast_tree = parse("""
    ss
    """)

    assert ast_tree.lines[0] == ast.Line([
        ast.Step('s'),
        ast.Step('s')
    ])


def test_lines_step():

    ast_tree = parse("""
    ss
    rl
    """)

    assert ast_tree.lines[0] == ast.Line([
        ast.Step('s'),
        ast.Step('s')
    ])
    assert ast_tree.lines[1] == ast.Line([
        ast.Step('r'),
        ast.Step('l')
    ])


def test_lines_variable():

    _ast = parse("""
    A
    """)

    assert _ast.lines[0] == ast.Line([
        ast.Variable('A'),
    ])

    _ast = parse("""
    sAs
    """)

    assert _ast.lines[0] == ast.Line([
        ast.Step('s'),
        ast.Variable('A'),
        ast.Step('s')
    ])


def test_func_call():

    ast_tree = parse("""
    f
    """)

    assert ast_tree.lines[0] == ast.Line([ast.FuncCall('f')])

    ast_tree = parse("""
    sfs
    """)

    assert ast_tree.lines[0] == ast.Line([
        ast.Step('s'),
        ast.FuncCall('f'),
        ast.Step('s')
    ])


def test_func_call_args_moves():

    _ast = parse("""
    f(s)
    """)

    assert _ast.lines[0] == ast.Line([
        ast.FuncCall(
            'f',
            ast.CallArgList([
                ast.Line([ast.Step('s')])
            ])
        )
    ])


    _ast = parse("""
    f(sSs)
    """)

    assert _ast.lines[0] == ast.Line([
        ast.FuncCall(
            'f',
            ast.CallArgList([
                ast.Line([ast.Step('s'), ast.Variable('S'), ast.Step('s')])
            ])
        )
    ])


    _ast = parse("""
    f(s,F,sF)
    """)


    assert _ast.lines[0] == ast.Line([
        ast.FuncCall(
            'f',
            ast.CallArgList([
                ast.Line([ast.Step('s')]),
                ast.Line([ast.Variable('F')]),
                ast.Line([ast.Step('s'), ast.Variable('F')]),
            ])
        )
    ])



def test_func_def():

    ast_tree = parse("""
    f:ss
    """)

    assert ast_tree.lines[0] == ast.Line([
        ast.FuncDefinition('f', None, ast.Line([ast.Step('s'), ast.Step('s')]))
    ])

