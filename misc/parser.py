"""A small library for parsing and evaluating standard arithmetic expressions.
This is strictly for fun.
"""

# Threshold for comparisons with numeric zero.
EPSILON = 1e-8


# Illegal expression object.
ILLEGAL_EXPR = {
    "op": "illegal",
    "left": 0,
    "right": 0,
}


# Functions associated with the above operators.
operator_funcs = {
    "plus": (lambda x, y: x + y),
    "minus": (lambda x, y: x - y),
    "multiply": (lambda x, y: x * y),
    "divide": (lambda x, y: x / y),
}


# Compute the expression value.
def value(expr):
    # expr is either a simple number, or a map of three elements.
    if type(expr) is dict:
        op = expr.get("op", "illegal")
        if op == "illegal":
            # this is an illegal expression.
            return ILLEGAL_EXPR

        else:
            lft, rgt = expr.get("left", 0), expr.get("right", 0)
            lft, rgt = value(lft), value(rgt)
            if op == "divide" and abs(rgt) <= EPSILON:
                return ILLEGAL_EXPR

            return operator_funcs[op](lft, rgt)
    else:
        return expr


# Tokenize the expression string. Valid tokens are
# numbers, operators, brackets.
def tokenize(expr_s):
    tokens, i = [], 0

    # Skip the whitespace from i.
    def skip_whitespace(i):
        ii = i
        while ii < len(expr_s) and expr_s[ii] in " \r\n\t":
            ii = ii + 1
        return ii

    # Read a number from the current position.
    def read_number():
        # number :- [0-9]+(.[0-9]*)?
        si, ii = i, i
        while ii < len(expr_s) and expr_s[ii] in "0123456789":
            ii = ii + 1

        if ii < len(expr_s) and expr_s[ii] == '.':
            ii = ii + 1

            while ii < len(expr_s) and expr_s[ii] in "0123456789":
                ii = ii + 1

        return (ii, float(expr_s[si:ii]))

    while i < len(expr_s):
        # Skip the whitespace.
        i = skip_whitespace(i)

        if expr_s[i] in "+-/*":
            tokens.append(expr_s[i])
            i = i + 1
            continue
        elif expr_s[i] in "()":
            tokens.append(expr_s[i])
            i = i + 1
            continue
        elif expr_s[i] in "0123456789":
            i, v = read_number()
            tokens.append(v)
            continue
        else:
            return ILLEGAL_EXPR

    return tokens


# Parse the list of tokens.
def parse_tokens(tokens):

    def is_number(token):
        return token[0] in "0123456789"

    # Returns the index of next matching closing bracket,
    # or -1, if it doesn't exist.
    def matching_bracket(tokens, i):

        depth = 1
        for j in xrange(i + 1, len(tokens)):
            if tokens[j] == "(":
                depth += 1
            elif tokens[j] == ")":
                depth -= 1
                if not depth:
                    return j

        return -1

    expr_stack, i = [[]], 0
    last_operator = "plus"

    while i < len(tokens):
        if tokens[i] == "(":
            if not last_operator:
                return ILLEGAL_EXPR

            j = matching_bracket(tokens, i)
            if j < 0:
                # No matching closing bracket, hence an illegally formed
                # expression.
                return ILLEGAL_EXPR

            sub_expr = parse_tokens(tokens[i + 1:j])
            i = j + 1

            if sub_expr == ILLEGAL_EXPR:
                # Illegal sub-expr, return ILLEGAL
                return ILLEGAL_EXPR

            if last_operator in ["plus", "minus", "divide", "multiply"]:
                expr_stack[-1].append(sub_expr)
            else:
                return ILLEGAL_EXPR
            last_operator = None

        elif tokens[i] == "+":
            if last_operator:
                return ILLEGAL_EXPR

            expr_stack.append("plus")
            expr_stack.append([])
            last_operator = "plus"
            i = i + 1
        elif tokens[i] == "-":
            if last_operator:
                return ILLEGAL_EXPR
            expr_stack.append("minus")
            expr_stack.append([])
            last_operator = "minus"
            i = i + 1
        elif tokens[i] == "/":
            if last_operator:
                return ILLEGAL_EXPR
            last_operator = "divide"
            expr_stack[-1].append("divide")
            i = i + 1
        elif tokens[i] == "*":
            if last_operator:
                return ILLEGAL_EXPR
            last_operator = "multiply"
            expr_stack[-1].append("multiply")
            i = i + 1
        else:
            # it's a number.
            print "token is", tokens[i]
            if not last_operator:
                return ILLEGAL_EXPR
            expr_stack[-1].append(tokens[i])
            i = i + 1
            last_operator = None

    return expr_stack


# Parse the expression.
def parse_expression(expr_s):
    tokens = tokenize(expr_s)
    return parse_tokens(tokens)


# Read a few expressions from stdin and compute their values.
def main():
    num_cases = int(raw_input().strip())
    for cas in xrange(num_cases):
        expr_s = raw_input()
        print value(parse_expression(expr_s))


if __name__ == '__main__':
    main()
