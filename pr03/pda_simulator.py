#!/usr/bin/env python3
"""Формальный недетерминированный МПА для L12; принятие по финальному состоянию."""
from collections import deque
from itertools import product
from pathlib import Path
import xml.etree.ElementTree as ET

FINAL = {"q3", "q4"}
# (откуда, символ ввода или '', вершина магазина, куда, замена вершины)
DELTA = [
    ("q0", "a", "Z", "q0", "AZ"),
    ("q0", "a", "A", "q0", "AA"),
    ("q0", "", "Z", "q1", "Z"),
    ("q0", "", "A", "q1", "A"),
    ("q1", "b", "A", "q1", ""),
    ("q1", "", "A", "q3", "A"),
    ("q1", "b", "Z", "q2", "Z"),
    ("q2", "b", "Z", "q2", "Z"),
    ("q2", "", "Z", "q4", "Z"),
]

def recognize(word):
    """Вернуть (принято, один успешный путь). Верх магазина — первый символ."""
    if any(ch not in "ab" for ch in word):
        return False, []
    start = ("q0", 0, "Z")
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        (state, pos, stack), path = queue.popleft()
        if pos == len(word) and state in FINAL:
            return True, path
        for src, char, top, dst, repl in DELTA:
            if state != src or not stack.startswith(top):
                continue
            if char and (pos == len(word) or word[pos] != char):
                continue
            nxt = (dst, pos + bool(char), repl + stack[1:])
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt]))
    return False, []

def check_jff():
    root = ET.parse(Path(__file__).with_name("L12_PDA.jff")).getroot()
    ids = {s.attrib["id"]: s.attrib["name"] for s in root.findall(".//state")}
    transitions = []
    for t in root.findall(".//transition"):
        transitions.append((ids[t.findtext("from")], t.findtext("read") or "",
                            t.findtext("pop") or "", ids[t.findtext("to")],
                            t.findtext("push") or ""))
    assert sorted(transitions) == sorted(DELTA), "Переходы Python и JFLAP различаются"

def test():
    check_jff()
    for length in range(9):
        for chars in product("ab", repeat=length):
            word = "".join(chars)
            expected = word == "a" * word.count("a") + "b" * word.count("b") and word.count("a") != word.count("b")
            got, _ = recognize(word)
            assert got == expected, f"Ошибка для {word!r}: {got} != {expected}"
    print("OK: все цепочки над {a,b} длины 0..8, 511 тестов; JFF совпадает с Python")

if __name__ == "__main__":
    test()
    for word in ("aab", "abb", "aabb"):
        accepted, path = recognize(word)
        print(word, "ACCEPT" if accepted else "REJECT")
        for state, pos, stack in path:
            print(f"  {state}, остаток={word[pos:]!r}, магазин={stack}")
