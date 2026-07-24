import itertools

def word_to_number(word, mapping):
    """Convert a word to its integer value using the letter‑>digit map."""
    num = 0
    for ch in word:
        num = num * 10 + mapping[ch]
    return num

def solve_cryptarithm(addend1, addend2, result):
    """Brute‑force search for a digit assignment that makes the equation true."""
    # collect all distinct letters
    letters = set(addend1 + addend2 + result)
    if len(letters) > 10:          # more letters than digits → impossible
        print("Too many different letters.")
        return None

    # first letters cannot be zero
    first_letters = {addend1[0], addend2[0], result[0]}

    digits = range(10)             # 0‑9
    for perm in itertools.permutations(digits, len(letters)):
        # create mapping letter -> digit
        mapping = dict(zip(letters, perm))

        # skip if any leading letter maps to 0
        if any(mapping[ch] == 0 for ch in first_letters):
            continue

        a = word_to_number(addend1, mapping)
        b = word_to_number(addend2, mapping)
        r = word_to_number(result, mapping)

        if a + b == r:
            return mapping, a, b, r

    return None   # no solution found


if __name__ == "__main__":
    # Example problem: SEND + MORE = MONEY
    add1 = "SEND"
    add2 = "MORE"
    res  = "MONEY"

    print("Trying to solve:", add1, "+", add2, "=", res)
    answer = solve_cryptarithm(add1, add2, res)

    if answer is None:
        print("No solution found.")
    else:
        mapping, a, b, r = answer
        print("\nSolution found!")
        print("Letter → digit mapping:")
        for ch in sorted(mapping):
            print(f"  {ch} = {mapping[ch]}")
        print()
        print(f"{add1} = {a}")
        print(f"{add2} = {b}")
        print(f"{res}  = {r}")
        print(f"Check: {a} + {b} = {r}  ->  {a + b == r}")
