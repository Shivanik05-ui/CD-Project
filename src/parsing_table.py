# parsing_table.py

def first_of_string(symbols, first, grammar):
    result = set()

    for symbol in symbols:

        if symbol not in grammar:
            result.add(symbol)
            return result

        result |= (first[symbol] - {'epsilon'})

        if 'epsilon' not in first[symbol]:
            return result

    result.add('epsilon')
    return result


def generate_parsing_table(grammar, first, follow):

    table = {}

    for nt in grammar:
        table[nt] = {}

    for A in grammar:

        for production in grammar[A]:

            # epsilon production
            if production == ['epsilon']:

                for terminal in follow[A]:
                    if terminal in table[A]:
                        print(f"WARNING: Grammar is not LL(1)! Conflict at M[{A}, {terminal}]")
                    else:
                        table[A][terminal] = production 

                continue

            # FIRST of production
            first_set = set()

            for symbol in production:

                if symbol not in grammar:
                    first_set.add(symbol)
                    break

                first_set |= (first[symbol] - {'epsilon'})

                if 'epsilon' not in first[symbol]:
                    break

            for terminal in first_set:
                table[A][terminal] = production

    return table

def display_parsing_table(table):

    print("\nLL(1) Parsing Table\n")

    terminals = set()

    for nt in table:
        terminals.update(table[nt].keys())

    terminals = sorted(terminals)

    print("NT\t", "\t".join(terminals))

    for nt in table:
        row = [nt]

        for t in terminals:
            if t in table[nt]:
                row.append(" ".join(table[nt][t]))
            else:
                row.append("-")

        print("\t".join(row))    