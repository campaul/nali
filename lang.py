import copy


class Object(object):

    def __init__(self):
        super(Object, self).__init__()
        self.namespace = {}

    def execute(self, args):
        if isinstance(args[0], Symbol):
            return Setter(self, str(args[0]))
        elif isinstance(self.namespace[str(args[0])], Function):
            return Caller(self, self.namespace[str(args[0])])
        else:
            return self.namespace[str(args[0])]

    def arg_count(self):
        return 1
        
    def __str__(self):
        return '[object]'

    def val(self):
        return self


class Function(Object):

    def __init__(self, namespace, prototype, expressions, eval_func):
        self.namespace = namespace
        self.prototype = prototype
        self.expressions = expressions
        self.eval_func = eval_func
    
    def execute(self, args):
        if args:
            namespace = dict(self.namespace.items() + dict(zip(self.prototype, args)).items())
        else:
            namespace = dict(self.namespace.items())

        namespace['def'] = Namespace(namespace)

        for expression in self.expressions:
            result = self.eval_func(expression[:], namespace)

        return result

    def arg_count(self):
        return len(self.prototype)

    def __str__(self):
        return "[function]"


class Namespace(Object):

    def __init__(self, namespace):
        self.namespace = namespace


class Message(Object):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value[1:]


class Symbol(Object):

    def __init__(self, value):
        super(Symbol, self).__init__()
        self.value = value

    def __str__(self):
        return self.value[1:]


class Setter(Object):
    def __init__(self, target, name):
        self.target = target
        self.name = name

    def execute(self, args):
        self.target.namespace[self.name] = args[0]
        return args[0]


class Caller(Object):

    def __init__(self, caller, function):
        self.caller = caller
        self.function = function

    def execute(self, args):
        if not args:
            args = []

        return self.function.execute([self.caller] + args)
    
    def arg_count(self):
        return self.function.arg_count() - 1


class Print(Function):

    def __init__(self):
        pass

    def execute(self, args):
        print args[0]
        return Object()

    def arg_count(self):
        return 1


class Exit(Function):

    def __init__(self):
        pass

    def execute(self, args):
        exit()

    def arg_count(self):
        return 0


class Add(Function):
    
    def __init__(self):
        pass

    def execute(self, args):
        return Number(args[0].val() + args[1].val())

    def arg_count(self):
        return 2


class Subtract(Function):
    
    def __init__(self):
        pass

    def execute(self, args):
        return Number(args[0].val() - args[1].val())

    def arg_count(self):
        return 2


class Multiply(Function):
    
    def __init__(self):
        pass

    def execute(self, args):
        return Number(args[0].val() * args[1].val())

    def arg_count(self):
        return 2
    

class Divide(Function):
    
    def __init__(self):
        pass

    def execute(self, args):
        return Number(args[0].val() / args[1].val())

    def arg_count(self):
        return 2


class Mod(Function):
    
    def __init__(self):
        pass

    def execute(self, args):
        return Number(args[0].val() % args[1].val())

    def arg_count(self):
        return 2
        

class New(Function):
    
    def __init__(self):
        pass
        
    def execute(self, args):
        return copy.deepcopy(args[0])
    
    def arg_count(self):
        return 1


class Echo(Function):
    
    def __init__(self):
        pass
        
    def execute(self, args):
        return args[0]
    
    def arg_count(self):
        return 1


class Number(Object):

    def __init__(self, value):
        super(Number, self).__init__()
        self.value = value
        self.namespace = {
            'add': stdlib['add'],
            'sub': stdlib['sub'],
            'mul': stdlib['mul'],
            'div': stdlib['div'],
            'mod': stdlib['mod'],
            'equal': stdlib['equal'],
            'gt': stdlib['gt'],
            'lt': stdlib['lt']
        }

    def val(self):
        return self.value
    
    def __str__(self):
        return str(self.value)


class Boolean(Object):

    def __init__(self, value):
        super(Boolean, self).__init__()
        self.value = value

    def val(self):
        return self.value

    def __str__(self):
        return str(self.value)


class List(Object):
    
    def __init__(self):
        super(List, self).__init__()
        self.namespace = {
            'do': stdlib['do']
        }
        self.items = []

    def append(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)


class Do(Function):

    def __init__(self):
        pass

    def execute(self, args):
        for item in args[0].items:
            args[1].execute([item])

    def arg_count(self):
        return 2


class If(Function):

    def __init__(self):
        pass

    def execute(self, args):
        if args[0].execute(None).val():
            return args[1].val()
        else:
            return args[2].val()
    
    def arg_count(self):
        return 3


class Equal(Function):

    def __init__(self):
        pass

    def execute(self, args):
        return Boolean(args[0].val() == args[1].val())

    def arg_count(self):
        return 2


class Greater(Function):

    def __init__(self):
        pass

    def execute(self, args):
        return Boolean(args[0].val() > args[1].val())

    def arg_count(self):
        return 2


class Less(Function):

    def __init__(self):
        pass

    def execute(self, args):
        return Boolean(args[0].val() < args[1].val())

    def arg_count(self):
        return 2

        
stdlib = {
    'object': Object(),
    'new': New(),
    'add': Add(),
    'sub': Subtract(),
    'mul': Multiply(),
    'div': Divide(),
    'mod': Mod(),
    'exit': Exit(),
    'if': If(),
    'gt': Greater(),
    'lt': Less(),
    'equal': Equal(),
    'echo': Echo(),
    'print': Print(),
    'do': Do(),
    '+': Message('.add'),
    '-': Message('.sub'),
    '*': Message('.mul'),
    '/': Message('.div'),
    '%': Message('.mod'),
    '=': Message('.equal'),
    '>': Message('.gt'),
    '<': Message('.lt')
}
