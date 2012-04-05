from lang import Boolean, Function, List, Message, Namespace, Number, Symbol, stdlib


class Interpreter(object):

    def __init__(self):
        super(Interpreter, self).__init__()
        self.namespace = dict(stdlib.items())
        self.namespace['def'] = Namespace(self.namespace)

    def _eval(self, expression):
        return nali_eval(tokenize(expression), self.namespace)


def nali_eval(tokens, namespace):
    expression = []
    
    while len(tokens) > 0:
        token = tokens.pop(0)
        if token == '(':
            expression.append(nali_eval(tokens, namespace))
        elif token == ')':
            break
        elif token[0] == "[":
            expression.append(parse_function(tokens, namespace, nali_eval))
        elif token[0] == "\"":
            expression.append(token[1:len(token) - 1])
        elif token[0] == ":":
            expression.append(Symbol(token))
        elif token[0] == ".":
            if token[1:].isdigit():
                expression.append(Number(float('.'.join([
                    str(expression.pop()),
                    token[1:]
                ]))))
            else:
                expression.append(Message(token))
        elif token.isdigit():
            expression.append(Number(int(token)))
        elif token == 'true':
            expression.append(Boolean(True))
        elif token == 'false':
            expression.append(Boolean(False))
        elif token == '{':
            expression.append(parse_list(tokens, namespace, nali_eval))
        else:
            expression.append(namespace[token])

    return nali_exec(expression)

def nali_exec(expression):

    if len(expression) == 1 and expression[0].arg_count() > 0:
        return expression[0]

    obj = expression[0]
    arg = expression[1:]

    if(len(arg) == 0):
        obj = obj.execute(None)
    
    while len(arg) > 0:
        arg_count = obj.arg_count()
        obj = obj.execute(arg[:arg_count])
        arg = arg[arg_count:]

    return obj

def tokenize(expression):
    tokens = ['(',')','[',']','|','+','-',';','{','}']
    prefixes = ['.',':']
    
    for token in tokens:
        expression = expression.replace(token, token.join([' ',' ']))

    for prefix in prefixes:
        expression = expression.replace(prefix, prefix.join([' ','']))

    return expression.split()

def parse_function(tokens, namespace, eval_func):
    prototype = []
    expressions = []
    expression = []
    expressions.append(expression)

    if(tokens[0] == '|'):
        tokens.pop(0)
        while not tokens[0] == '|':
            prototype.append(tokens.pop(0))
        tokens.pop(0)

    count = 1

    while count > 0:
        token = tokens.pop(0)
        if token == '[':
            count = count + 1
        if token == ']':
            count = count - 1
        if token == ';':
            expression = []
            expressions.append(expression)
        else:
            expression.append(token)

    expression.pop()
    
    return Function(namespace, prototype, expressions, eval_func)

def parse_string(tokens):
    pass

def parse_list(tokens, namespace, eval_func):

    l = List()
    token = tokens.pop(0)
    
    while token != '}': 
        l.append(eval_func([token], namespace))
        token = tokens.pop(0)

    return l

def repl():
    interpreter = Interpreter()

    while(True):
        try:
            print interpreter._eval(raw_input('>> '))
        except Exception, e:
            raise
            print e.__class__.__name__ +  ": " + e.message
