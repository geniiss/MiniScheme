;funcions de haskell:
(define (foldl func x llista)
  (if (null? llista)
    x
    (foldl func (func x (car llista)) (cdr llista))))

(define (foldr f x llista)
  (if (null? llista)
    x
    (f (car llista) (foldr f x (cdr llista)))))

(define (until p f x)
  (if (p x)
    x
    (until p f (f x))))

(define (map f l)
  (if (null? l)
    '()
    (cons (f (car l)) (map f (cdr l)))))

(define (filter p l)
  (cond 
    ((null? l) '())
    ((p (car l)) (cons (car l) (filter p (cdr l))))
    (else (filter p (cdr l)))))

(define (all p l)
  (cond
    ((null? l) #t)
    ((p (car l)) (all p (cdr l)))
    (else #f)))

(define (any p l)
  (cond 
    ((null? l) #f)
    ((p (car l)) #t)
    (else (any p (cdr l)))))

(define (zip l1 l2)
  (cond
    ((null? l1) '())
    ((null? l2) '())
    (else (let ((llista (cons (car l2) '()))
                (llista2 (cons (car l1) llista)))
              (cons llista2 (zip (cdr l1) (cdr l2)))))))

(define (zipWith f l1 l2)
  (cond
    ((null? l1) '())
    ((null? l2) '())
    (else (cons (f (car l1) (car l2)) (zipWith f (cdr l1) (cdr l2))))))


;funcions auxiliars:
(define (suma n m) (+ n m))
(define (resta n m) (- n m))
(define (mult n m) (* n m))
(define (div n m) (/ n m))
(define (mod n m) (mod n m))
(define (mult2 n) (* 2 n))
(define (greaterThan100 n) (> n 100))
(define (inc n) (+ n 1))
(define (even n) (= (mod n 2) 0))
(define (odd n) (not (even n)))
(define (even100Odd n) (or (and (<= n 100) (even n)) (and (> n 100) (odd n))))
(define (square n) (* n n))
(define (greaterThan3 n) (> n 3))
(define (lessThan10 n) (< n 10))
(define (greaterThan5 n) (> n 5))
(define (lessThan0 n) (< n 0))
(define (classifyEvenOdd n) (if (even n) 'even 'odd))
(define (addIfEven acc x) (if (even x) (+ acc x) acc))
(define (doubleAndCons x acc) (cons (mult2 x) acc))
(define (sumList l) (foldl suma 0 l))
(define (cons el l) (cons el l))

;proves:
(display (foldl suma 1 '(1 2 3))) ;7
(newline)

(display (zipWith mult '(1 2 3 4) '(5 6 7 8))) ; (5 12 21 32)
(newline)

(display (until greaterThan100 mult2 101)); 101
(newline)

(display (until greaterThan100 mult2 2)); 128 
(newline)

(display (map inc '(123 86 53 567))); (124 87 54 568)
(newline)

(display (any even '(1 587 213 4323 9))); #f
(newline)

(display (any even '(1 587 213 43232 9))); #t
(newline)

(display (all even '(1 587 213 43232 9))); #f
(newline)

(display (all even '(12 5875 2130 43232 94))); #f
(newline)

(display (all odd '(1 3 5 7 9))); #t
(newline)

(display (any odd '(2 4 10 12))); #f
(newline)

(display (all even100Odd '(16 30 28 101 871 2))); #t
(newline)

(display (foldr mult 1 '(1 2 3 4 5))) ; 120
(newline)

(display (foldr resta 0 '(10 20 30))) ; 20 ; (10 - (20 - (30 - 0)))
(newline)

(display (foldl resta 0 '(10 20 30))) ; -60 ; (((0 - 10) - 20) - 30)
(newline)

(display (map square '(1 2 3 4 5))) ; (1 4 9 16 25)
(newline)

(display (filter greaterThan3 '(1 2 3 4 5))) ; (4 5)
(newline)

(display (all lessThan10 '(1 5 8 9))) ; #t
(newline)

(display (all greaterThan5 '(6 7 8 9))) ; #t
(newline)

(display (any lessThan0 '(1 2 3 -1 5))) ; #t
(newline)

(display (zip '(1 2 3) '(4 5 6))) ; ((1 4) (2 5) (3 6))
(newline)

(display (zipWith resta '(10 20 30) '(1 2 3))) ; (9 18 27)
(newline)

(display (map classifyEvenOdd '(1 2 3 4 5))) ; (odd even odd even odd)
(newline)

(display (until greaterThan100 mult2 5)) ; 128
(newline)

(display (foldl addIfEven 0 '(1 2 3 4 5 6))) ; 12 ; suma només els parells
(newline)

(display (foldr doubleAndCons '() '(1 2 3))) ; (2 4 6)
(newline)

(display (filter even100Odd '(50 101 102 120 7 9))) ; (50 101)
(newline)

(display (map sumList '((1 2 3) (4 5 6) (7 8 9)))) ; (6 15 24)
(newline)


(display (foldr cons '() '(1 2 3 4 5))) ; (1 2 3 4 5)
(newline)
