from rply import ParserGenerator

import ast
import lexer

pg = ParserGenerator(lexer.TOKENS, cache_id="language")


@pg.production("main : line")
def main_line(p):
    return ast.Root(p[0])


@pg.production("main : main line")
def main_main_line(p):
    p[0].append(p[1])
    return p[0]


@pg.production("line : line-content")
def line(p):
    return p[0]

@pg.production("line : line-content NEWLINE")
def line_content_NEWLINE(p):
    return p[0]


@pg.production("line : NEWLINE line-content NEWLINE")
def NEWLINE_line_NEWLINE(p):
    return p[1]


@pg.production("line : NEWLINE line-content")
def NEWLINE_line_content(p):
    return p[1]


@pg.production("line-content : func-definition ")
@pg.production("line-content : moves-list ")
def line_content(p):
    return p[0]


@pg.production("func-definition : FUNC COLON moves-list ")
def func_definition(p):
    return ast.Line(ast.FuncDefinition(
        p[0].getstr(),
        p[2],
        p[0].getsourcepos()
    ))


@pg.production("func-definition : FUNC ( definition-args ) COLON moves-list ")
def func_definition_args(p):
    return ast.Line(ast.FuncDefinition(
        p[0].getstr(),
        p[2],
        p[5],
        p[0].getsourcepos()
    ))


@pg.production("definition-args : ARGUMENT ")
def definition_args(p):
    return ast.DefinitionArg(p[0].getstr(), p[0].getsourcepos())


@pg.production("moves-list : moves-list move ")
@pg.production("moves-list : moves-list func-call ")
def moves_list(p):
    p[0].append(p[1])
    return p[0]


@pg.production("moves-list : move ")
def moves_list_move(p):
    return ast.Line(p[0])


@pg.production("move : STEP ")
@pg.production("move : TURN_LEFT ")
@pg.production("move : TURN_RIGHT ")
def move(p):
    return ast.Step(p[0].getstr(), p[0].getsourcepos())


@pg.production("func-call : FUNC ( call-args )")
def func_call(p):
    return ast.FuncCall(p[0].getstr(), p[2], p[0].getsourcepos())


@pg.production("call-args : DIGIT ")
def call_args(p):
    return ast.CallArg(p[0].getstr(), p[0].getsourcepos())


@pg.production("call-args : definition-args ")
def call_args_1(p):
    return p[0]



@pg.error
def error_handler(token):
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())


parser = pg.build()
