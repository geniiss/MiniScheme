from antlr4 import InputStream, StdinStream, CommonTokenStream
from schemeLexer import schemeLexer
from schemeParser import schemeParser
from EvalVisitor import EvalVisitor
from nothing import Nothing
import sys

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as file:
            input_stream = InputStream(file.read())
    except Exception:
        print("Es llegirà de stdin")
        input_stream = StdinStream(encoding='utf-8')  # llegir de stdin

    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    tree = parser.root()
    evaluator = EvalVisitor()
    try:
        evaluator.visit(tree)
    except Nothing as n:
        print(n)
    except Exception:
        print("Aplicació no vàlida o similar")
