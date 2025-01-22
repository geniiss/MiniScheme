// Gramàtica per expressions senzilles
grammar scheme;
root : expr+            // l'etiqueta ja és root
  ;

expr : '\'' expr                                                       # noevaluar
  | '(' expr* ')'                                                      # evaluar
  | ( '*' | '/' | '+' | '-' | '<' | '>' | '<=' | '>=' | '=' | '<>' )   # ignore
  | NUM                                                                # numero
  | VAR                                                                # variable
  | STRING                                                             # string
  | ('#t'|'#f')                                                        # boolea
  ;

STRING : '"' (~["])* '"';
VAR : [a-zA-ZàèéíòóúÀÈÉÍÒÓÚ][a-zA-Z0-9_?àèéíòóúÀÈÉÍÒÓÚ-]* ;
NUM : '-'?[0-9]+ ;
WS  : [ \t\n\r]+ -> skip ;

COMENTARIS : ';' (~[\n])* ('\n' | EOF) -> skip;
