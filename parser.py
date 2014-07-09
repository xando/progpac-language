from rply import ParserGenerator

import ast
import lexer


pg = ParserGenerator(lexer.TOKENS, cache_id="language")

@pg.production("main : line")
def main(p):
    return ast.Root(p[0])


@pg.production("main : NEWLINE line")
def NEWLINE_main(p):
    return ast.Root(p[1])


@pg.production("main : main line")
def main_line(p):
    p[0].append(p[1])
    return p[0]


@pg.production("line : line-content NEWLINE ")
def line(p):
    return p[0]


@pg.production("line-content : moves-list ")
@pg.production("line-content : func-definition ")
def line_content(p):
    return p[0]


@pg.production("func-definition : FUNC COLON moves-list ")
def func_definition(p):
    return ast.Line([ast.FuncDefinition(
        p[0].getstr(),
        None,
        p[2],
        p[0].getsourcepos()
    )])


@pg.production("func-definition : FUNC ( NAME ) COLON moves-list ")
def func_definition_args(p):
    return ast.Line([ast.FuncDefinition(
        p[0].getstr(),
        None,
        p[5],
        p[0].getsourcepos()
    )])


@pg.production("moves-list : moves-list move ")
def moves_list(p):
    p[0].append(p[1])
    return p[0]


@pg.production("moves-list : move ")
def moves_list_move(p):
    return ast.Line([p[0]])


@pg.production("move : variable ")
@pg.production("move : func-call ")
@pg.production("move : step ")
def move(p):
    return p[0]


@pg.production("variable : NAME ")
def variable(p):
    return ast.Variable(p[0].getstr(), p[0].getsourcepos())


@pg.production("func-call : FUNC ")
def func_call(p):
    return ast.FuncCall(p[0].getstr(), None, p[0].getsourcepos())


@pg.production("step : STEP ")
@pg.production("step : TURN_LEFT ")
@pg.production("step : TURN_RIGHT ")
def step(p):
    return ast.Step(p[0].getstr(), p[0].getsourcepos())


@pg.production("func-call : FUNC ( args-list ) ")
def func_call_ags(p):
    return ast.FuncCall(p[0].getstr(), p[2], p[0].getsourcepos())


@pg.production("args-list : args-list , arg ")
def func_call_args_list(p):
    p[0].append(p[2])
    return p[0]


@pg.production("args-list : arg ")
def func_call_args(p):
    return ast.CallArgList([p[0]])


@pg.production("arg : DIGIT ")
def call_args_DIGIT(p):
    return ast.CallArg(p[0].getstr(), p[0].getsourcepos())


@pg.production("arg : moves-list ")
def call_args_moves_list(p):
    return p[0]


@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())


parser = pg.build()


def parse(code):
    # code = "%s" % code
    print [t for t in lexer.lexer.lex(code)]
    token_stream = lexer.lexer.lex(code)
    return parser.parse(token_stream)

