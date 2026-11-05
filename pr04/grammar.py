"""Исходная грамматика и воспроизводимое преобразование в НФХ."""
from pathlib import Path
import xml.etree.ElementTree as ET

SOURCE = {
    'S': ['V=E'], 'E': ['E+T', 'E-T', 'T'],
    'T': ['T*U', 'T/U', 'U'], 'U': ['-U', '[E]', 'V', 'N'],
    'V': list('abcdef'), 'N': ['NK', '0', '1'], 'K': ['0', '1'],
}
# Замена терминалов в составных правых частях.
TERMINALS = {'=': 'Z', '+': 'P', '-': 'M', '*': 'R', '/': 'W', '[': 'L', ']': 'J'}
# Имена вспомогательных пар фиксированы для удобства чтения JFLAP.
PAIRS = {'ZE': 'Q', 'PT': 'A', 'MT': 'B', 'RU': 'C', 'WU': 'D', 'EJ': 'H'}

def cnf():
    """Удалить цепные правила, заменить терминалы, бинаризовать правила."""
    rules = {}
    for left in SOURCE:
        closure = {left}
        while True:
            more = {r for a in closure for r in SOURCE[a] if r in SOURCE}
            if more <= closure:
                break
            closure |= more
        rules[left] = sorted({r for a in closure for r in SOURCE[a] if r not in SOURCE})
    result = {}
    for left, rights in rules.items():
        result[left] = []
        for right in rights:
            if len(right) > 1:
                right = ''.join(TERMINALS.get(c, c) for c in right)
            if len(right) == 3:
                right = right[0] + PAIRS[right[1:]]
            result[left].append(right)
    result.update({v: [k] for k, v in TERMINALS.items()})
    result.update({v: [k] for k, v in PAIRS.items()})
    return result

def write_jff(path):
    root = ET.Element('structure')
    ET.SubElement(root, 'type').text = 'grammar'
    for left, rights in cnf().items():
        for right in rights:
            p = ET.SubElement(root, 'production')
            ET.SubElement(p, 'left').text = left
            ET.SubElement(p, 'right').text = right
    ET.indent(root)
    ET.ElementTree(root).write(path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    write_jff(Path(__file__).with_name('L01_CYK.jff'))
