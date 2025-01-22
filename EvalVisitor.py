from schemeVisitor import schemeVisitor
import sys
from nothing import Nothing


class EvalVisitor(schemeVisitor):
    d = {
        # operacions aritmètiques
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '/': lambda x, y: x / y,
        '*': lambda x, y: x * y,
        '^': lambda x, y: x ** y,
        'mod': lambda x, y: x % y,
        # operacions booleanes
        '=': lambda x, y: x == y,
        '<>': lambda x, y: x != y,
        '>=': lambda x, y: x >= y,
        '<=': lambda x, y: x <= y,
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
    }

    @staticmethod
    def isBasicType(var):
        return any([
            isinstance(var, int),
            isinstance(var, str),
            isinstance(var, bool)])

    def __init__(self):
        self.ts = [{}]
        # {id: value} si son constants
        # {id: ([paràmetres(string)], expr)]} si son funcs

    def visitRoot(self, ctx):
        stats = list(ctx.getChildren())
        for stat in stats:
            self.visit(stat)
        if 'main' in self.ts[-1] and len(self.ts[-1]["main"]) == 2:
            for expr in self.ts[-1]["main"][1]:
                self.visit(expr)

    def printValue(self, a):
        if a is not None:
            if isinstance(a, str):
                sys.stdout.write(a)
            elif isinstance(a, bool):
                if a:
                    sys.stdout.write('#t')
                else:
                    sys.stdout.write('#f')
            elif isinstance(a, (int, float)):
                sys.stdout.write(f'{int(a)}')
            elif isinstance(a, list):
                if not a:
                    sys.stdout.write("()")
                else:
                    sys.stdout.write('(')
                    self.printValue(a[0])
                    for el in a[1:]:
                        sys.stdout.write(' ')
                        self.printValue(el)
                    sys.stdout.write(')')
            else:
                self.printValue(self.visit(a))

    def visitNoevaluar(self, ctx):
        # ["'", expr]
        expr = list(ctx.getChildren())[1]
        value = list(expr.getChildren())
        if len(value) > 1:
            return value[1:-1]
        return value[0].getText()

    def visitEvaluar(self, ctx):
        # ['(', expr*, ')']
        llista = list(ctx.getChildren())
        funcName = llista[1].getText()
        if funcName in self.d:
            if len(llista) != 5:
                raise Nothing("Error d'aritat")
            func = self.d[funcName]
            return func(self.visit(llista[2]), self.visit(llista[3]))
        if funcName == 'display':
            self.printValue(self.visit(llista[2]))
            return
        if funcName == 'cond':
            return self.explorarCond(llista)
        if funcName == 'if':
            if len(llista) != 6:
                raise Nothing("Error d'aritat")
            return self.explorarIf(llista)
        if funcName == 'define':
            if ctx.depth() != 2:
                raise Nothing("El define només pot ser usat al primer nivell")
            return self.explorarDefine(llista)
        if funcName == "car":
            if len(llista) != 4:
                raise Nothing("Error d'aritat")
            return self.explorarCar(llista)
        if funcName == 'cdr':
            if len(llista) != 4:
                raise Nothing("Error d'aritat")
            return self.explorarCdr(llista)
        if funcName == 'cons':
            if len(llista) != 5:
                raise Nothing("Error d'aritat")
            return self.explorarCons(llista)
        if funcName == 'null?':
            if len(llista) != 4:
                raise Nothing("Error d'aritat")
            return self.explorarNull(llista)
        if funcName == 'let':
            return self.explorarLet(llista)
        if funcName == 'read':
            if len(llista) != 3:
                raise Nothing("Error d'aritat")
            return self.explorarRead()
        if funcName == 'newline':
            if len(llista) != 3:
                raise Nothing("Error d'aritat")
            print()
            return
        if funcName == 'and' or funcName == 'or':
            if len(llista) != 5:
                raise Nothing("Error d'aritat")
            return self.explorarAndOr(llista, funcName)
        if funcName == 'not':
            if len(llista) != 4:
                raise Nothing("Error d'aritat")
            return self.explorarNot(llista)
        for taula_simbols in list(reversed(self.ts)):
            if funcName in taula_simbols and len(taula_simbols[funcName]) == 2:
                return self.explorarCrida(llista)
        raise Nothing("Funció no definida")

    def explorarAndOr(self, elements, OP):
        [_, _, expr1, expr2, _] = elements
        if OP != 'and' and OP != 'or':
            raise ValueError("Argument no vàlid")
        if OP == 'and':
            return self.visit(expr1) and self.visit(expr2)
        return self.visit(expr1) or self.visit(expr2)

    def explorarNot(self, elementsNot):
        [_, _, expr1, _] = elementsNot
        return not self.visit(expr1)

    def explorarDefine(self, elementsDefine):
        # ['(', 'define', expr*, ')']
        if len(elementsDefine) < 4:
            raise Nothing("Insuficients expressions en Define")
        if len(list(elementsDefine[2].getChildren())) == 1:
            return self.explorarConstant(elementsDefine)
        return self.explorarFuncio(elementsDefine)

    def explorarConstant(self, elementsConst):
        # ['(', 'define', WORD, expr, ')']
        if len(elementsConst) != 5:
            raise Nothing(
                "Els elements quan definexies constants" +
                " haurien de ser: Nom i expressió")
        [_, _, word, expr, _] = elementsConst
        self.ts[0][word.getText()] = self.visit(expr)

    def visitVariable(self, ctx):
        [word] = list(ctx.getChildren())
        word = word.getText()
        for taula_simbols in list(reversed(self.ts)):
            if word in taula_simbols:
                return taula_simbols[word]
        raise Nothing("Variable no definida")

    def visitString(self, ctx):
        [string] = list(ctx.getChildren())
        string = string.getText()
        return string[1:-1]

    def visitBoolea(self, ctx):
        [char] = list(ctx.getChildren())
        char = char.getText()
        if (char == '#t'):
            return True
        return False

    def explorarRead(self):
        a = input()
        if a == '#t':
            return True
        if a == '#f':
            return False
        try:
            a = int(a)
        except ValueError:
            pass
        return a

    def explorarIf(self, elementsIf):
        # ['(', 'if', expr, expr, expr, ')']
        [_, _, cond, expr1, expr2, _] = elementsIf
        if self.visit(cond):
            return self.visit(expr1)
        return self.visit(expr2)

    def explorarCar(self, elementsCar):
        # ['(', 'car', llista, ')']
        [_, _, llista, _] = elementsCar
        var = self.visit(llista)
        if var is None:
            return
        if not isinstance(var, list):
            raise Nothing("No és una llista")
        if not var:
            raise Nothing("Violació de contracte")
        if self.isBasicType(var[0]):
            return var[0]
        if len(list(var[0].getChildren())) == 1:
            return self.visit(var[0])
        return list(var[0].getChildren())[1:-1]

    def explorarCdr(self, elementsCar):
        # ['(', 'car', llista, ')']
        [_, _, llista, _] = elementsCar
        var = self.visit(llista)
        if not isinstance(var, list):
            raise Nothing("No és una llista")
        if not var:
            raise Nothing("Violació de contracte")
        return var[1:]

    def explorarCons(self, elementsCons):
        # ['(', 'cons', expr, llista, ')']
        [_, _, expr, llista, _] = elementsCons
        var = self.visit(llista)
        if not isinstance(var, list):
            raise Nothing("Llista no definida")
        a = self.visit(expr)
        return [a]+var

    def explorarNull(self, elementsCar):
        # ['(', 'car', llista, ')']
        [_, _, llista, _] = elementsCar
        var = self.visit(llista)
        if not isinstance(var, list):
            raise Nothing("Llista no definida")
        return not var

    def explorarLet(self, elementsLet):
        # ['(', 'let', expr+, ')']
        declaracions = list(elementsLet[2].getChildren())
        self.ts.append({})
        for declaracio in declaracions[1:-1]:
            elementsDeclaracio = list(declaracio.getChildren())
            if len(elementsDeclaracio) != 4:
                raise Nothing(
                    "Declaracions de variables" +
                    " al let haurien de tenir: nom valor")
            [_, nom, expr, _] = elementsDeclaracio
            self.ts[-1][nom.getText()] = self.visit(expr)
        for el in elementsLet[3:-2]:
            self.visit(el)
        retValue = self.visit(elementsLet[-2])
        self.ts.pop(-1)
        if retValue:
            return retValue

    def explorarCond(self, condElements):
        # ['(', 'cond', expr, ..., expr, ')']
        condExprs = condElements[2:-1]
        if len(condExprs) == 0:
            raise Nothing("El cond no té expressions")
        for el in condExprs:
            expressio = list(el.getChildren())
            if len(expressio) != 4:
                raise Nothing("Expressió no vàlida al cond")
            [_, expr1, expr2, _] = expressio
            if expr1.getText() == 'else' or self.visit(expr1):
                return self.visit(expr2)
        raise Nothing("Com a mínim una condició del const ha de ser true")

    def explorarCrida(self, elementsCrida):
        # ['(', expr*, ')']
        id = elementsCrida[1].getText()
        values = []
        for expr in elementsCrida[2:-1]:
            try:
                el = self.visit(expr)
                values.append(el)
            except Nothing:
                if len(list(expr.getChildren())) != 1:
                    raise Nothing("Variable no definida")
                word = list(expr.getChildren())[0].getText()
                if word not in self.ts[0]:
                    raise Nothing("Variable no definida")
                values.append(self.ts[0][word])
        func = self.ts[-1][id] if id in self.ts[-1] else self.ts[0][id]
        if len(func[0]) != len(values):
            raise Nothing("Error d'aritat")
        self.ts.append({key: value for (key, value) in zip(func[0], values)})
        for el in func[1][:-1]:
            self.visit(el)
        retValue = self.visit(func[1][-1])
        self.ts.pop(-1)
        if retValue is None:
            return
        return retValue

    def explorarFuncio(self, elementsFuncio):
        # ['(', 'define', expr+, ')']
        if len(elementsFuncio) < 5:
            raise Nothing(
                "Elements quan defineixes funció haurien" +
                " de ser: (funcname vars+) expressió+")
        definition = list(elementsFuncio[2].getChildren())  # ['(', WORD+, ')']
        id = definition[1].getText()
        vars = [el.getText() for el in definition[2:-1]]
        exprs = elementsFuncio[3:-1]
        self.ts[0][id] = (vars, exprs)

    def visitNumero(self, ctx):
        [numero] = list(ctx.getChildren())
        return int(numero.getText())
