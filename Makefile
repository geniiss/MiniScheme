name = scheme

all:
	@if java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -no-listener -visitor $(name).g4; then \
		echo "ANTLR compilation succeeded"; \
	elif antlr4 -Dlanguage=Python3 -no-listener -visitor $(name).g4; then \
		echo "ANTLR compilation succeeded"; \
	else \
		echo "ANTLR compilation failed"; \
		exit 1; \
	fi

clean:
	rm -f -r $(name).interp $(name).tokens $(name)Lexer.interp $(name)Lexer.py $(name)Lexer.tokens $(name)Parser.py $(name)Visitor.py .antlr ./__pycache__