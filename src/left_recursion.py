def remove_immediate_left_recursion(grammar):
    """
    Removes immediate left recursion from the grammar.
    Example:
        E -> E + T | T
    becomes:
        E -> T E'
        E' -> + T E' | epsilon
    """

    new_grammar = {}

    for non_terminal, productions in grammar.items():

        alpha = []   # Left-recursive productions
        beta = []    # Non-left-recursive productions

        for production in productions:

            if len(production) > 0 and production[0] == non_terminal:
                alpha.append(production[1:])
            else:
                beta.append(production)

        if alpha:

            new_nt = non_terminal + "'"

            new_grammar[non_terminal] = []

            for b in beta:
                new_grammar[non_terminal].append(b + [new_nt])

            new_grammar[new_nt] = []

            for a in alpha:
                new_grammar[new_nt].append(a + [new_nt])

            new_grammar[new_nt].append(["epsilon"])

        else:

            new_grammar[non_terminal] = productions

    return new_grammar