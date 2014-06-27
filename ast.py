from rply.token import BaseBox


class Node(BaseBox):
    def compile(self, ctx):
        pass


class Root(Node):

    def __init__(self, lines):
        self.lines = [lines]

    def append(self, element):
        self.lines.append(element)

    def get_lines(self):
        return self.lines

    def __repr__(self):
        return "Prog(lines=%s)" % self.lines


class Line(Node):

    def __init__(self, stmts):
        self.stmts = [stmts]

    def append(self, element):
        self.stmts.append(element)

    def get_stmts(self):
        return self.stmts

    def __repr__(self):
        return "Line(stmts=%s)" % self.stmts


class Step(Node):
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "Step(%s)" % self.value

    def compile(self, ctx):
        ctx.code.append(self.value)


class FuncCall(Node):
    def __init__(self, value, args, pos):
        self.value = value
        self.args = int(args.value)
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "FuncCall(name=%s, args=%s)" % (self.value, self.args)

    def compile(self, ctx):

        print self.args
        self.args -= 1
        function = ctx.functions[self.value]
        for step in function.get_stmts():
            try:
                step.compile(ctx)
            except RuntimeError:
                pass


class FuncDefinition(Node):
    def __init__(self, name, args, body, pos):
        self.name = name
        self.body = body
        self.args = args
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "FuncDefinition(name=%s, args=%s, %s)" % (self.name, self.args, self.body)

    def compile(self, ctx):
        ctx.functions[self.name] = self.body


class DefinitionArg(Node):
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Arg(%s)" % self.name


class CallArg(Node):
    def __init__(self, value, pos):
        self.value = value
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Arg(%s)" % self.value


class Context(object):
    code = []
    functions = {}


def compile(ast):
    ctx = Context()

    for l in ast.get_lines():
        for stmt in l.get_stmts():
            stmt.compile(ctx)

    return "".join(ctx.code)

