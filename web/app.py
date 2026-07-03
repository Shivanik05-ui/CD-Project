import os
import sys
from flask import Flask, render_template, request, jsonify
from graphviz import Digraph

# Force Graphviz path (fix for Windows)


# allow importing src modules
sys.path.append("../src")

from grammar_input import load_grammar_from_file
from first_follow import compute_first, compute_follow
from parsing_table import generate_parsing_table


app = Flask(__name__)

# load grammar
grammar = load_grammar_from_file("../grammar/sample_grammar.txt")


# ---------------- HOME PAGE ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PARSING STEPS ---------------- #

def generate_parsing_steps(expr):

    tokens = expr.split()
    tokens.append("$")

    stack = ["$", "E"]

    pointer = 0
    steps = []

    first = compute_first(grammar)
    follow = compute_follow(grammar, first, "E")
    table = generate_parsing_table(grammar, first, follow)

    while len(stack) > 0:

        stack_str = " ".join(stack)
        input_str = " ".join(tokens[pointer:])

        top = stack.pop()
        current = tokens[pointer]

        if top == current:
            steps.append({
                "stack": stack_str,
                "input": input_str,
                "action": f"Match {current}"
            })
            pointer += 1

        elif top in table and current in table[top]:

            production = table[top][current]

            steps.append({
                "stack": stack_str,
                "input": input_str,
                "action": f"{top} → {' '.join(production)}"
            })

            if production[0] != "epsilon":
                for symbol in reversed(production):
                    stack.append(symbol)

        else:
            steps.append({
                "stack": stack_str,
                "input": input_str,
                "action": "ERROR"
            })
            break

    return steps


# ---------------- PARSE TREE ---------------- #

def create_parse_tree(expr):

    tokens = expr.split()

    dot = Digraph(comment="Parse Tree")

    dot.node("E")

    parent = "E"

    for i, tok in enumerate(tokens):

        node = f"node{i}"

        dot.node(node, tok)

        dot.edge(parent, node)

    path = "static/parse_tree"

    dot.render(path, format="png", cleanup=True)

    return "/static/parse_tree.png"


# ---------------- PARSER API ---------------- #

@app.route("/parse", methods=["POST"])
def parse():

    try:

        data = request.get_json()
        expr = data["expr"]

        # compute FIRST FOLLOW
        first = compute_first(grammar)
        follow = compute_follow(grammar, first, list(grammar.keys())[0])

        # parsing table
        table = generate_parsing_table(grammar, first, follow)

        # convert sets to list for JSON
        first = {k: list(v) for k, v in first.items()}
        follow = {k: list(v) for k, v in follow.items()}

        # parsing steps
        steps = generate_parsing_steps(expr)

        # parse tree
        tree = create_parse_tree(expr)

        return jsonify({
            "grammar": grammar,
            "first": first,
            "follow": follow,
            "table": table,
            "steps": steps,
            "tree": tree
        })

    except Exception as e:

        print("SERVER ERROR:", e)

        return jsonify({
            "error": str(e)
        })


# ---------------- RUN SERVER ---------------- #

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
