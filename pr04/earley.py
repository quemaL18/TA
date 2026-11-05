"""Алгоритм Эрли для исходной грамматики варианта 1 (без ε-правил)."""
import argparse
from grammar import SOURCE

def recognize(word):
    rules = {k: list(v) for k, v in SOURCE.items()}
    rules['@'] = ['S']
    chart = [set() for _ in range(len(word) + 1)]
    chart[0].add(('@', 'S', 0, 0))
    for i in range(len(chart)):
        agenda = list(chart[i])
        def add(state):
            if state not in chart[i]:
                chart[i].add(state)
                agenda.append(state)
        for left, rhs, dot, origin in agenda:
            if dot == len(rhs):
                for a, r, d, o in list(chart[origin]):
                    if d < len(r) and r[d] == left:
                        add((a, r, d + 1, o))
            elif rhs[dot] in rules:
                for r in rules[rhs[dot]]:
                    add((rhs[dot], r, 0, i))
            elif i < len(word) and rhs[dot] == word[i]:
                chart[i + 1].add((left, rhs, dot + 1, origin))
    return ('@', 'S', 1, 0) in chart[-1], chart

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('word')
    p.add_argument('--table', action='store_true')
    args = p.parse_args()
    accepted, chart = recognize(args.word)
    print('ACCEPT' if accepted else 'REJECT')
    if args.table:
        for i, states in enumerate(chart):
            print(f'I[{i}]')
            for a, rhs, dot, origin in sorted(states):
                print(f'  {a} -> {rhs[:dot]}•{rhs[dot:]} ({origin})')
    raise SystemExit(0 if accepted else 1)
