from grammar_input import get_grammar,load_grammar_from_file
from first_follow import compute_first, compute_follow
from parsing_table import generate_parsing_table,display_parsing_table
from parser_engine import parse_input_string

def main():

    choice = input("Load grammar from file? (y/n): ")

    if choice.lower() == "y":
        grammar = load_grammar_from_file("../grammar/sample_grammar.txt")
    else:
        grammar = get_grammar()
    print("\nGrammar:")
    for k,v in grammar.items():
        print(k,"->",v)

    first = compute_first(grammar)

    print("\nFIRST Sets:")
    for nt in first:
        print(f"FIRST({nt}) =", sorted(first[nt]))

    start_symbol = list(grammar.keys())[0]

    follow = compute_follow(grammar, first, start_symbol)

    print("\nFOLLOW Sets:")
    for nt in follow:
        print(f"FOLLOW({nt}) =", sorted(follow[nt]))

    table = generate_parsing_table(grammar, first, follow)
    display_parsing_table(table)

    print("\nParsing Table:\n")

    for nt in table:
        for terminal in table[nt]:
            print(f"M[{nt}, {terminal}] -> {nt} -> {' '.join(table[nt][terminal])}")

    # Input string parsing
    user_input = input("\nEnter input string (tokens separated by space): ")

    tokens = user_input.split()

    result = parse_input_string(grammar, table, start_symbol, tokens)

    if result:
        print("\nString Accepted")
    else:
        print("\nSyntax Error")
if __name__ == "__main__":
    main()