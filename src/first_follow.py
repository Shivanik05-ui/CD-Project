# first_follow.py

def compute_first(grammar):
    first = {}

    for non_terminal in grammar:
        first[non_terminal] = set()

    changed = True

    while changed:
        changed = False

        for nt in grammar:
            for production in grammar[nt]:

                symbol = production[0]

                if symbol not in grammar:
                    if symbol not in first[nt]:
                        first[nt].add(symbol)
                        changed = True
                else:
                    before = len(first[nt])
                    first[nt] |= first[symbol]
                    if len(first[nt]) > before:
                        changed = True

    return first


def compute_follow(grammar, first, start_symbol):

    follow = {nt: set() for nt in grammar}
    follow[start_symbol].add('$')

    changed = True

    while changed:
        changed = False

        for A in grammar:
            for production in grammar[A]:

                for i, B in enumerate(production):

                    if B in grammar:

                        # case 1: symbol followed by another
                        if i + 1 < len(production):

                            beta = production[i+1]

                            if beta in grammar:

                                before = len(follow[B])

                                follow[B] |= (first[beta] - {'epsilon'})

                                if 'epsilon' in first[beta]:
                                    follow[B] |= follow[A]

                                if len(follow[B]) > before:
                                    changed = True

                            else:
                                before = len(follow[B])

                                follow[B].add(beta)

                                if len(follow[B]) > before:
                                    changed = True

                        # case 2: last symbol
                        else:

                            before = len(follow[B])

                            follow[B] |= follow[A]

                            if len(follow[B]) > before:
                                changed = True

    return follow