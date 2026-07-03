# parser_engine.py

from parse_tree import ParseTree

def parse_input_string(grammar, table, start_symbol, input_string):

    stack = []
    stack.append('$')
    stack.append(start_symbol)

    input_string.append('$')

    pointer = 0
    step = 1

    # Create parse tree
    tree = ParseTree()
    root = tree.add_node(start_symbol)

    node_stack = [root]

    print("\nStep-by-Step Parsing\n")
    print("STEP\tSTACK\t\tINPUT\t\tACTION")

    while stack:

        stack_top = stack[-1]
        current_input = input_string[pointer]

        print(f"{step}\t{stack}\t{input_string[pointer:]}\t", end="")
        step += 1

        # ACCEPT condition
        if stack_top == current_input == '$':
            print("ACCEPT")
            tree.render()
            return True

        # Match terminal
        elif stack_top == current_input:
            stack.pop()
            pointer += 1

            if node_stack:
                node_stack.pop()

            print("Match", current_input)

        # If non-terminal
        elif stack_top in grammar:

            if current_input in table[stack_top]:

                production = table[stack_top][current_input]

                stack.pop()

                parent_node = node_stack.pop()

                if production != ['epsilon']:

                    new_nodes = []

                    for symbol in production:
                        child = tree.add_node(symbol)
                        tree.add_edge(parent_node, child)
                        new_nodes.append(child)

                    # push to stack in reverse
                    for symbol in reversed(production):
                        stack.append(symbol)

                    node_stack.extend(reversed(new_nodes))

                print(f"{stack_top} -> {' '.join(production)}")

            else:
                print(f"Syntax Error: unexpected token '{current_input}'")
                return False

        else:
            print(f"Syntax Error: expected '{stack_top}', found '{current_input}'")
            return False

    return False