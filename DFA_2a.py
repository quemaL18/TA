# DFA_2a.py
ALPHABET = ['a', 'b']

START = (0, 0)
ACCEPT = {(2, 3)}
def inc(x):
    if x < 3:
        return x + 1
    return 3

TRANS = {}
for i in range(4):
    for j in range(4):
        TRANS[(i, j)] = {}
        TRANS[(i, j)]['a'] = (inc(i), j)
        TRANS[(i, j)]['b'] = (i, inc(j))

def run_dfa(word):
    state = START
    trace = [state]
    for idx in range(len(word)):
        ch = word[idx]
        if ch not in ALPHABET:
            return False, trace, "invalid symbol"
        state = TRANS[state][ch]
        trace.append(state)
    return state in ACCEPT, trace, None

if __name__ == "__main__":
    tests = [
        ['a','a','b','b','b'],       # aabbb True
        ['a','a','b','b','b','b'],
        ['a','a','b','b'],
        ['a','a','a','b','b','b'],
        ['b','b','a','a'],
        ['a','b','a','b','a','b'],
        ['a','a','b','b','b','a'],
    ]
    for w in tests:
        ok, trace, err = run_dfa(w)
        print("Word:", ''.join(w))
        print("  Trace:", ' -> '.join(str(s) for s in trace))
        print("  Result:", "ACCEPT" if ok else "REJECT")
        print()