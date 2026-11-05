"""Посимвольный CYK для НФХ из JFLAP; Python 3.10+, без зависимостей."""
import argparse
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

DEFAULT = Path(__file__).with_name('L01_CYK.jff')

def load_grammar(path=DEFAULT):
    root = ET.parse(path).getroot()
    if root.findtext('type') != 'grammar':
        raise ValueError('Ожидается грамматика JFLAP')
    rules = [(p.findtext('left', ''), p.findtext('right', '')) for p in root.findall('production')]
    if not rules:
        raise ValueError('Пустая грамматика')
    variables = {a for a, _ in rules}
    if any(len(a) != 1 or not a.isupper() for a in variables):
        raise ValueError('Нетерминалы должны быть одиночными заглавными буквами')
    start = rules[0][0]
    for a, rhs in rules:
        if not ((len(rhs) == 1 and rhs not in variables and not rhs.isupper()) or
                (len(rhs) == 2 and all(b in variables for b in rhs))):
            raise ValueError(f'Правило вне НФХ: {a} -> {rhs}')
        if start in rhs:
            raise ValueError('Стартовый символ встречается справа')
    return start, rules

def recognize(word, grammar=None):
    start, rules = grammar if grammar is not None else load_grammar()
    terminals, pairs = defaultdict(set), defaultdict(set)
    for a, rhs in rules:
        (terminals if len(rhs) == 1 else pairs)[rhs].add(a)
    n = len(word)
    table = [[set() for _ in range(n + 1)] for _ in range(n)]
    for i, c in enumerate(word):
        table[i][1] = set(terminals[c])
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            for split in range(1, length):
                for b in table[i][split]:
                    for c in table[i + split][length - split]:
                        table[i][length].update(pairs[b + c])
    return bool(n and start in table[0][n]), table

def format_table(word, table):
    lines = ['Длина | Начало (с 1) | Подстрока | Нетерминалы']
    for length in range(1, len(word) + 1):
        for i in range(len(word) - length + 1):
            lines.append(f'{length} | {i+1} | {word[i:i+length]} | ' + (','.join(sorted(table[i][length])) or '∅'))
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('word', help='Точная строка, включая пробелы, если они есть')
    parser.add_argument('--table', action='store_true')
    parser.add_argument('--grammar', type=Path, default=DEFAULT)
    args = parser.parse_args()
    try:
        accepted, table = recognize(args.word, load_grammar(args.grammar))
    except (ValueError, OSError, ET.ParseError) as error:
        parser.error(str(error))
    print('ACCEPT' if accepted else 'REJECT')
    if args.table:
        print(format_table(args.word, table))
    return 0 if accepted else 1

if __name__ == '__main__':
    raise SystemExit(main())
