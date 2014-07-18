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
        self.lines = lines

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
        ctx.stack[-1].code.append(self)


class FuncCall(Node):
    def __init__(self, value, args=None, pos=None):
        self.value = value
        if args:
            self.args = args.stmts
        else:
            self.args = []
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "FuncCall('%s', %s)" % (self.value, self.args)

    def compile(self, ctx):
        try:
            function_body, def_args = ctx.functions[self.value]
        except KeyError:
            raise ValueError('(%s:%s) Function "%s" is undefined.' % (
                self.pos.lineno, self.pos.colno, self.value)
            )

        def_args_number = len(def_args)
        call_args_number = len(self.args)

        if def_args_number != call_args_number:
            raise ValueError('(%s:%s) Function "%s" takes %s arguments, %s given.' % (
                self.pos.lineno, self.pos.colno, self.value, def_args_number, call_args_number)
            )


        call_variables = {}

        for i, arg in enumerate(self.args):
            ctx.stack.append(Frame(ctx.stack[-1].variables))
            arg.compile(ctx)
            frame = ctx.stack.pop()
            call_variables[def_args[i].name] = Line(frame.code)

        ctx.stack.append(Frame(call_variables))

        for step in function_body.get_stmts():
            step.compile(ctx)

        frame = ctx.stack.pop()
        ctx.stack[-1].code.extend(frame.code)


class FuncDefinition(Node):
    def __init__(self, name, body, args=None, pos=None):
        self.name = name
        self.body = body
        if args:
            self.args = args.stmts
        else:
            self.args = []
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "FuncDefinition('%s', %s, %s)" % (self.name, self.args, self.body)

    def compile(self, ctx):
        ctx.functions[self.name] = self.body, self.args


class Variable(Node):
    def __init__(self, name, pos=None):
        self.name = name
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Variable('%s')" % self.name

    def compile(self, ctx):
        try:
            ctx.stack[-1].variables[self.name].compile(ctx)
        except KeyError:
            raise ValueError('(%s:%s) Variable "%s" is undefined.' % (
                self.pos.lineno, self.pos.colno, self.name)
            )


class DefArg(Node):
    def __init__(self, name, pos=None):
        self.name = name
        self.pos = pos

    def getstr(self):
        return self.name

    def __repr__(self):
        return "Arg(%s)" % self.name


class DefArgList(Line):

    def __repr__(self):
        return "DefArgList(stmts=%s)" % self.stmts


class CallArg(Line):
    def __init__(self, value, pos=None):
        self.value = value
        self.pos = pos

    def getstr(self):
        return self.value

    def __repr__(self):
        return "CallArg(%s)" % self.value


class CallArgList(Line):

    def __repr__(self):
        return "CallArgList(stmts=%s)" % self.stmts


class Frame(object):

    def __init__(self, variables=None):
        self.code = []
        self.variables = variables or {}

    def __repr__(self):
        return "<Frame %s: %s>" % (self.variables, self.code)

class Context(object):
    functions = {}
    stack = [Frame()]


def compile(ast):
    ctx = Context()
    ast.compile(ctx)
    return "".join([c.value for c in ctx.stack[-1].code])
