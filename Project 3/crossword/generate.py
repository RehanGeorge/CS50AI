import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """    
        for variable in self.crossword.variables:
            for word in self.crossword.words:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize revised to False
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap is not None:
            i, j = overlap
            # For each word in x's domain, check if there is a word in y's domain
            for word_x in self.domains[x].copy():
                remove = True
                # If there is a word in y's domain that has the same letter in the overlap, keep it
                for word_y in self.domains[y]:
                    if word_x[i] == word_y[j]:
                        remove = False
                # If there is no word in y's domain that has the same letter in the overlap, remove it
                if remove:
                    self.domains[x].remove(word_x)
                    revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is None, initialize it to all arcs in the problem
        if arcs is None:
            arcs = []
            for variable in self.crossword.variables:
                for neighbor in self.crossword.neighbors(variable):
                    arcs.append((variable, neighbor))
        while arcs:
            # While queue is not empty, pop an arc
            x, y = arcs.pop()
            # If Revise and length of domain is 0, return False
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                # For each Z in X's neighbors, add (Z, X) to queue
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # If assignment has the same number of variables as the crossword, it is complete
        if len(assignment) == len(self.crossword.variables):
            return True
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if all values are distinct
        if len(assignment) != len(set(assignment.values())):
            return False
        # Check if all words have the correct length
        for variable in assignment:
            if len(assignment[variable]) != variable.length:
                return False
        # Check if no conflicts between neighboring variables
        for variable in assignment:
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[variable, neighbor]
                    if assignment[variable][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain_values = []
        # Iterate through all values in var's domain
        for value in self.domains[var]:
            ruled_out = 0
            # For each value, check how many values it rules out for neighboring variables
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment and value in self.domains[neighbor]:
                    ruled_out += 1
            domain_values.append((value, ruled_out))
        # Sort values by how many values they rule out for neighboring variables
        domain_values.sort(key=lambda x: x[1])
        return [value[0] for value in domain_values]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = []
        # Iterate through all variables
        for variable in self.crossword.variables:
            # If variable is not in assignment, add it to the list of unassigned variables
            if variable not in assignment:
                unassigned_variables.append(variable)
        # Sort unassigned variables by number of remaining values in their domain
        unassigned_variables.sort(key=lambda x: len(self.domains[x]))
        # If there is a tie, sort by degree
        if len(unassigned_variables) > 1:
            unassigned_variables.sort(key=lambda x: len(self.crossword.neighbors(x)), reverse=True)
        return unassigned_variables[0]
    

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """ 
        # If assignment is complete, return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        variable = self.select_unassigned_variable(assignment)

        # Iterate through all values in the domain of the variable
        for value in self.order_domain_values(variable, assignment):
            # Add the value to the assignment
            assignment[variable] = value
            # If the assignment is consistent, continue
            if self.consistent(assignment):
                # Recursive call to backtrack
                result = self.backtrack(assignment)
                # If result is not None, return it
                if result is not None:
                    return result
            # Remove the value from the assignment
            assignment.pop(variable)

        # If no assignment is possible, return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
