"""Тесты CYK и проверка рекурсивным спуском."""
import itertools
import json
from pathlib import Path
import random
import unittest
from cyk import load_grammar, recognize as cyk
from grammar import cnf

CASES = json.loads(Path(__file__).with_name('tests.json').read_text(encoding='utf-8'))

def reference(s):
    """Независимый анализатор; правила не считывает из тестируемых грамматик."""
    i = 0
    def peek():
        return s[i] if i < len(s) else '\0'
    def unary():
        nonlocal i
        if peek() == '-':
            i += 1
            unary()
        elif peek() == '[':
            i += 1
            expression()
            if peek() != ']':
                raise ValueError
            i += 1
        elif peek() in 'abcdef':
            i += 1
        elif peek() in '01':
            while peek() in '01':
                i += 1
        else:
            raise ValueError
    def term():
        nonlocal i
        unary()
        while peek() in '*/':
            i += 1
            unary()
    def expression():
        nonlocal i
        term()
        while peek() in '+-':
            i += 1
            term()
    try:
        if len(s) < 3 or s[0] not in 'abcdef' or s[1] != '=':
            return False
        i = 2
        expression()
        return i == len(s)
    except ValueError:
        return False

class ParsersTest(unittest.TestCase):
    def test_cnf_and_jff_consistency(self):
        start, rules = load_grammar()
        self.assertEqual(start, 'S')
        self.assertEqual(set(rules), {(a,r) for a,rs in cnf().items() for r in rs})
    def test_examples(self):
        for t in CASES:
            with self.subTest(word=t['input']):
                for f in (lambda s: cyk(s)[0], reference):
                    self.assertEqual(f(t['input']),t['expected'])
    def test_exhaustive_short_expressions(self):
        for n in range(5):
            for chars in itertools.product('a01+-*/[]', repeat=n):
                word = 'a=' + ''.join(chars)
                expected = reference(word)
                self.assertEqual(cyk(word)[0], expected, word)
    def test_generated_and_mutated(self):
        rng = random.Random(4101)
        def expr(depth):
            if not depth or rng.random() < .4:
                return rng.choice(['a','b','e','f','0','1','101','001'])
            kind = rng.randrange(3)
            if kind == 0:
                return '-'+expr(depth-1)
            if kind == 1:
                return '['+expr(depth-1)+']'
            return expr(depth-1)+rng.choice('+-*/')+expr(depth-1)
        for _ in range(400):
            word = rng.choice('abcdef')+'='+expr(3)
            for sample in (word, word[:rng.randrange(len(word))], word+'+', word+'2'):
                expected = reference(sample)
                self.assertEqual(cyk(sample)[0], expected, sample)

if __name__ == '__main__':
    unittest.main(verbosity=2)
