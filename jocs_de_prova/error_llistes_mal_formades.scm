; Test 4.1: Ús de `car` sobre un literal no llista
(car 42) ; Error esperat: No és una llista

; Test 4.2: Ús de `cdr` sobre un literal no llista
(cdr 'a) ; Error esperat: No és una llista

; Test 4.3: `car` sobre llista buida
(car '()) ; Error esperat: Operació no vàlida sobre llista buida

; Test 4.4: `cdr` sobre llista buida
(cdr '()) ; Error esperat: Operació no vàlida sobre llista buida
