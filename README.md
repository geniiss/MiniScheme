# Pràctica de Compiladors

Aquest directori conté els fitxers necessaris per a la pràctica de LP, a més de l'executable antlr-4.13.2-complete.jar,
el qual es pot usar per compilar la grmàtica del projecte.

## Autor

Genís Carretero Ferrete

## Instruccions

1. Preparar programa fent "make"
2. Executar interpret fent "python3 scheme.py", si es vol provar l'interpret agafant el codi per la consola.
3. Executar interpret fent "python3 scheme.py prova.scm", si es vol agafar el codi del fitxer prova.scm

## Jocs de prova

Si es vol comprovar el correcte funcionament de l'interpret, cal executar el programa de testeig "python3 test.py".
L'script test.py té el següent funcionament:
  - Executa els jocs de prova situats a ./jocs_de_prova usant "python3 scheme.py ./jocs_de_prova/nom_fitxer.scm"
  - Comprova els resultats amb els fitxers situats a ./outputs_esperats

Hi ha bastants jocs de proves, i això és perque he volgut comprovar que tots els errors salten correctament,
però només puc fer que salti un error per cada fitxer.
Petita explicació del joc de proves, obviant els errors:
  # haskell.scm
    En aquest fitxer, he implementat les funcions més bàsiques de haskell, i he fet diferentes crides per provar.
    He provat casos més extrems i més usuals.

  Amb només aquest joc de prova, es testegen totes les funcionalitats implenatades:       
    - Funcions d'ordre superior
    - Recursivitat
    - Definició de funcions
    - Operacions aritmètiques
    - Operacions booleanes
    - Funcions per defecte de llistes
    - Condicionals
    - Variables locals amb let
    - Sortida

## Decisions de disseny

S'han segut les directrius de disseny del repositori de la pràctica però s'han decidit els següents aspectes:
  1. La funció (read) sempre llegeix tota una línea de l'input
  2. Només s'executen les funcions cridades, a excepció de la funció que es digui main, que s'executarà encara que no sigui cridada.

## Ampliabilitat

Aquest projecte és fàcilment ampliable ja que la gramàtica és simple, només s'haurien d'afegir les funcionalitats noves
al fitxer EvalVisitor.py, jo continuaria implementant les funcions lambda, ja que em semblen bastant importants, i també
afegint la possibilitat de passar funcions com a paràmetre només escrivint l'operador +, *, and, or, etc. Que és una cosa 
que no he implementat i ho podria haver fet.
