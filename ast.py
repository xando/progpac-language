from rply.token import BaseBox


class Node(BaseBox):
    def compile(self, ctx):
        pass

    def __eq__(self, other):
        # tests only
        if self.__class__ != other.__class__:
            return False

        self.__dict__.pop("pos", None)
        other.__dict__.pop("pos", None)

        return self.__dict__ == other.__dict__


class Root(Node):

    def __init__(self, lines):
        self.lines = [lines]

    def append(self, element):
        self.lines.append(element)

    def get_lines(self):
        return self.lines

    def __repr__(self):
        return "Prog(lines=%s)" % self.lines

    def compile(self, ctx):
        for line in self.lines:
            line.compile(ctx)


class Line(Node):

    def __init__(self, stmts):
        self.stmts = stmts

    def append(self, element):
        self.stmts.append(element)

    def get_stmts(self):
        return self.stmts

    def __repr__(self):
        return "Line(stmts=%s)" % self.stmts

    def compile(self, ctx):
        for stmt in self.stmts:
            stmt.compile(ctx)


class Step(Node):
    def __init__(self, value, pos=None):
        self.value = value
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "Step('%s')" % self.value

    def compile(self, ctx):
        ctx.code.append(self.value)


class FuncCall(Node):
    def __init__(self, value, args=None, pos=None):
        self.value = value
        self.args = args
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "FuncCall('%s', %s)" % (self.value, self.args)

    def compile(self, ctx):
        function_body = ctx.functions[self.value]
        ctx.stack.append(self.args)
        for step in function_body.get_stmts():
            try:
                step.compile(ctx)
            except RuntimeError:
                pass


class FuncDefinition(Node):
    def __init__(self, name, args, body, pos=None):
        self.name = name
        self.body = body
        self.args = args
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "FuncDefinition('%s', %s, %s)" % (self.name, self.args, self.body)

    def compile(self, ctx):
        ctx.functions[self.name] = self.body


class Variable(Node):
    def __init__(self, name, pos=None):
        self.name = name

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Variable('%s')" % self.name

    def compile(self, ctx):
        if not ctx.stack:
            raise Exception("Using arguments outside functions is not allowed")

        args = ctx.stack.pop()
        for step in args.stmts:
            step.compile(ctx)


class DefinitionArg(Node):
    def __init__(self, name, pos=None):
        self.name = name
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Arg(%s)" % self.name


class CallArg(Node):
    def __init__(self, value, pos=None):
        self.value = value
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "Arg(%s)" % self.value


class CallArgList(Line):

    def __repr__(self):
        return "CallArgList(stmts=%s)" % self.stmts



class Context(object):
    code = []
    functions = {}
    stack = []


def compile(ast):
    ctx = Context()
    ast.compile(ctx)
    return "".join(ctx.code)
