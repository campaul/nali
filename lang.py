import copy

class Object(object):

    def __init__(self):
        self.namespace = {}

    def execute(self, args):
        if type(args[0])  == Symbol:
            return Setter(self, str(args[0]))
        elif isinstance(self.namespace[str(args[0])], Function):
            return Caller(self, self.namespace[str(args[0])])
        else:
            return self.namespace[str(args[0])]

    def arg_count(self):
        return 1
        
    def __str__(self):
        return '[object]'

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

class Number(Object):

    def __init__(self, value):
        super(Number, self).__init__()
        self.value = value
        self.namespace["add"] = stdlib['add']
        self.namespace["sub"] = stdlib['sub']
        self.namespace["mul"] = stdlib['mul']
        self.namespace["div"] = stdlib['div']
        self.namespace["mod"] = stdlib['mod']

    def val(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
        
stdlib = {
    'object': Object(),
    'new': New(),
    'add': Add(),
    'sub': Subtract(),
    'mul': Multiply(),
    'div': Divide(),
    'mod': Mod(),
    'exit': Exit(),
    '+': Message('.add'),
    '-': Message('.sub'),
    '*': Message('.mul'),
    '/': Message('.div'),
    '%': Message('.mod')
}
