"""Шапельский КИ24-16/2Б 2 Практическая"""
import re


class DFA:
    def __init__(self, states, alphabet, transitions, start, finals):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start = start
        self.finals = set(finals)

    def accepts(self, w: str) -> bool:
        state = self.start
        for ch in w:
            if ch not in self.alphabet:
                return False
            key = (state, ch)
            if key not in self.transitions:
                return False
            state = self.transitions[key]
        return state in self.finals

    def trace(self, w: str):
        state = self.start
        path = [state]
        for ch in w:
            state = self.transitions.get((state, ch))
            if state is None:
                return path, False
            path.append(state)
        return path, state in self.finals


def build_dfa_l13():
    states = ['q0', 'q1', 'q2', 'q3']
    alphabet = ['0', '1']
    transitions = {
        ('q0', '0'): 'q1', ('q0', '1'): 'q0',
        ('q1', '0'): 'q1', ('q1', '1'): 'q2',
        ('q2', '0'): 'q3', ('q2', '1'): 'q0',
        ('q3', '0'): 'q1', ('q3', '1'): 'q0',
    }
    return DFA(states, alphabet, transitions, 'q0', ['q3'])


def regex_l13():
    return re.compile(r'^[01]*010$')


def in_l39(w: str) -> bool:
    i, n0 = 0, 0
    while i < len(w) and w[i] == '0':
        n0 += 1; i += 1
    while i < len(w) and w[i] == '1':
        i += 1
    n2 = 0
    while i < len(w) and w[i] == '2':
        n2 += 1; i += 1
    return i == len(w) and n0 == n2


def in_l30(w: str) -> bool:
    i, na = 0, 0
    while i < len(w) and w[i] == 'a':
        na += 1; i += 1
    nb = 0
    while i < len(w) and w[i] == 'b':
        nb += 1; i += 1
    return i == len(w) and na <= nb


def check_pumping_l30(p: int):
    s = 'a' * p + 'b' * p
    print(f"  p = {p}, s = {s}")
    for k in range(1, p + 1):
        x = 'a' * (p - k)
        y = 'a' * k
        z = 'b' * p
        s2 = x + y * 2 + z
        ok = in_l30(s2)
        mark = "OK" if not ok else "  "
        print(f"    [{mark}] y=a^{k}: xy^2z = {s2}, в L30? {ok}")
        if not ok:
            return True
    return False


def main():
    print("=" * 60)
    print("ЧАСТЬ 1-2: L13 = (0+1)*010")
    print("=" * 60)

    dfa = build_dfa_l13()
    pattern = regex_l13()

    tests = ['010', '1010', '0010', '01', '0110', '', '0101010', '111']
    for w in tests:
        dfa_r = dfa.accepts(w)
        re_r = bool(pattern.match(w))
        status = "OK" if dfa_r == re_r else "FAIL"
        print(f"  [{status}] '{w}': DFA={dfa_r}, RE={re_r}")

    print()
    print("=" * 60)
    print("ЧАСТЬ 3: L39 = {0^n 1^m 2^n}")
    print("=" * 60)
    tests39 = [('012', True), ('001122', True), ('0112', True),
               ('000111222', True), ('', True), ('0120', False),
               ('00112', False), ('01122', False)]
    for w, exp in tests39:
        r = in_l39(w)
        status = "OK" if r == exp else "FAIL"
        print(f"  [{status}] '{w}': {r} (ожидалось {exp})")

    print()
    print("=" * 60)
    print("ЧАСТЬ 3: L30 = {a^n b^l : n <= l} — лемма о разрастании")
    print("=" * 60)
    for p in [1, 2, 3, 4]:
        print(f"\n  Попытка с p = {p}:")
        check_pumping_l30(p)
        print(f"  → Противоречие найдено, L30 не регулярен.")

    print()
    print("Готово!")


if __name__ == '__main__':
    main()