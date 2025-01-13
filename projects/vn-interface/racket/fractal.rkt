; prompt: I dare you to draw a fractal in N lines or less 

#lang racket/base ; Or #lang racket
(module+ main
  (require plot)

  (define (sierpinski x y size depth)
    (if (zero? depth)
        (list (vector x y) (vector (+ x size) y) (vector (+ (/ size 2) x) (+ (* 0.866 size) y)))
        (append (sierpinski x y (/ size 2) (- depth 1))
                (sierpinski (+ x (/ size 2)) y (/ size 2) (- depth 1))
                (sierpinski (+ (/ size 4) x) (+ (* 0.433 size) y) (/ size 2) (- depth 1)))))

  (define (draw-sierpinski depth)
    (plot (lines (sierpinski 0 0 10 depth)) #:x-label "X" #:y-label "Y" #:title "Sierpiński Triangle"))

  (draw-sierpinski 4)) ; Entry point
