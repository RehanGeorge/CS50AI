from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledge = And(
    # A can be a knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B can be a knight or knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # C can be a knight or knave but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledge,
    # If A is a knight, then A is both a knight and a knave
    Implication(AKnight, And(AKnight, AKnave)),
    # If A is a knave, then A is not both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledge,
    # If A is a knight, then A and B are both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, then (A and B) are not both knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledge,
    # If A is a knight, then A and B are both knights or both knaves
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # If A is a knave, then A and B are not both knights or both knaves
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a knight, then A and B are not both knights or both knaves
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # If B is a knave, then A and B are both knights or both knaves
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."


knowledge3 = And(
    knowledge,
    # B says A says "I am a knave." - If B is a knight
    Implication(BKnight, And(
        # If A is a knight, then A is a knave
        Implication(AKnight, AKnave),
        # If A is a knave, then A is not a knave
        Implication(AKnave, Not(AKnave))
    )),
    # B says "A said 'I am a knave'." - If B is a knave
    Implication(BKnave, Not(And(
        # If A is a knight, then A is a knave
        Implication(AKnight, AKnave),
        # If A is a knave, then A is not a knave
        Implication(AKnave, Not(AKnave))
    ))),
    # B says "C is a knave." - If B is a knight
    Implication(BKnight, CKnave),
    # B says "C is a knave." - If B is a knave
    Implication(BKnave, Not(CKnave)),
    # C says "A is a knight." - If C is a knight
    Implication(CKnight, AKnight),
    # C says "A is a knight." - If C is a knave
    Implication(CKnave, Not(AKnight))
)
    
### Test ###
# knowledge3 = And(
#     knowledge,
#     Or(
#         # A says "I am a knight."
#         And(
#             # If A is a knight, then A is a knight
#             Implication(AKnight, AKnight),
#             # If A is a knave, then A is not a knight
#             Implication(AKnave, Not(AKnight)),
#             # B says "A said 'I am a knave'." - this doesn't seem useful
#             # B says "C is a knave." - If B is a knight
#             Implication(BKnight, CKnave),
#             # B says "C is a knave." - If B is a knave
#             Implication(BKnave, Not(CKnave)),
#             # C says "A is a knight." - If C is a knight
#             Implication(CKnight, AKnight),
#             # C says "A is a knight." - If C is a knave
#             Implication(CKnave, Not(AKnight))
#         ),
#         # A says "I am a knave."
#         And(
#             # If A is a knight, then A is a knave
#             Implication(AKnight, AKnave),
#             # If A is a knave, then A is not a knave
#             Implication(AKnave, Not(AKnave)),
#             # B says "A said 'I am a knave'." - this doesn't seem useful
#             # B says "C is a knave." - If B is a knight
#             Implication(BKnight, CKnave),
#             # B says "C is a knave." - If B is a knave
#             Implication(BKnave, Not(CKnave)),
#             # C says "A is a knight." - If C is a knight
#             Implication(CKnight, AKnight),
#             # C says "A is a knight." - If C is a knave
#             Implication(CKnave, Not(AKnight))
#         )
#     )
# )


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
