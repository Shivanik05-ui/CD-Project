# grammar_input.py

def get_grammar():
    grammar = {}

    print("Enter grammar productions (Example: E->TE')")
    print("Type 'done' when finished\n")

    while True:
        rule = input("Enter production: ")

        if rule.lower() == "done":
            break

        left, right = rule.split("->")
        productions = right.split("|")

        grammar[left.strip()] = [p.strip().split() for p in productions]

    return grammar


def load_grammar_from_file(filename):

    grammar = {}

    with open(filename, encoding="utf-8") as f:
        lines = f.readlines()

    for rule in lines:

        rule = rule.strip()

        if not rule:
            continue

        left, right = rule.split("->")

        productions = right.split("|")

        grammar[left.strip()] = []

        for p in productions:
            symbols = p.strip().split()

            # convert epsilon word
            if symbols == ["epsilon"]:
                symbols = ["epsilon"]

            grammar[left.strip()].append(symbols)

    return grammar