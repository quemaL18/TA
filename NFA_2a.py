# NFA_2b.py
ALPHABET = ['1', '2', '3']

STATES = ['S', 'P1_23', 'P2_13', 'P3_12', 'F1', 'F2', 'F3']
START = 'S'
ACCEPT = {'F1', 'F2', 'F3'}

TRANS = {
    'S': {
        '1': ['F1', 'P2_13', 'P3_12'],
        '2': ['F2', 'P1_23', 'P3_12'],
        '3': ['F3', 'P1_23', 'P2_13'],
    },
    'P1_23': {
        '1': ['F1'],
        '2': ['P1_23'],
        '3': ['P1_23'],
    },
    'P2_13': {
        '1': ['P2_13'],
        '2': ['F2'],
        '3': ['P2_13'],
    },
    'P3_12': {
        '1': ['P3_12'],
        '2': ['P3_12'],
        '3': ['F3'],
    },
    'F1': {'1': [], '2': [], '3': []},
    'F2': {'1': [], '2': [], '3': []},
    'F3': {'1': [], '2': [], '3': []},
}

def run_nfa(word):
    current = {START}
    trace = [set(current)]
    for idx in range(len(word)):
        ch = word[idx]
        if ch not in ALPHABET:
            return False, trace, "invalid symbol"
        nxt = set()
        for st in current:
            for ns in TRANS[st][ch]:
                nxt.add(ns)
        current = nxt
        trace.append(set(current))
        if not current:
            break
    ok = len(current & ACCEPT) > 0
    return ok, trace, None

if __name__ == "__main__":
    tests = [
        ['2','3','2','1'],           # 2321 True
        ['1','2','3','2','1'],
        ['1'],
        ['1','1'],
        ['2','3','1'],
        ['1','2','3'],
        ['3','1','2','3'],
    ]
    for w in tests:
        ok, trace, err = run_nfa(w)
        print("Word:", ''.join(w))
        for k, s in enumerate(trace):
            print("  step", k, ":", sorted(s) if s else "{}")
        print("  Result:", "ACCEPT" if ok else "REJECT")
        print()