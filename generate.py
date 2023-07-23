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
        self.times = 0

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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        #print("In enforce_node_consistency")
        for var in self.domains:
            var_len = var.length
            for word in list(self.domains[var]):
                if len(word) == var_len:
                    continue
                else:
                    self.domains[var].remove(word)
        #print(self.domains)
        #print(self.crossword.words)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] is None:
            return False
        else:
            i = self.crossword.overlaps[x, y][0]
            j = self.crossword.overlaps[x, y][1]

            ret  = False

            for temp_x in list(self.domains[x]):
                ok = 0
                for temp_y in list(self.domains[y]):
                    if temp_x[i] == temp_y[j]:
                        ok = 1
                        break
                if not ok:
                    self.domains[x].remove(temp_x)
                    ret = True
            
            return ret


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if not arcs:
            queue = []
            for var in self.domains:
                var_neighbours = list(self.crossword.neighbors(var))
                for neighbour in var_neighbours:
                    if neighbour != var:
                        queue.append(set((var, neighbour)))
        
        else:
            for arc in arcs:
                queue.append(arc)


        while len(queue) > 0:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                x_neighbors = self.crossword.neighbors(x)

                #print(x_neighbors)
                for z in x_neighbors:
                    if z != y:
                        queue.append((z, x))

        return True


        # raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        ok = True
        for var in self.domains:
            if var not in assignment:
                return False
            
        return ok


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        ## Checking length 
        values = []
        for var in assignment:
            if len(assignment[var]) != var.length:
                print("FF")
                return False
            
            ## Checking copy of values
            value = assignment[var]
            if value in values:
                return False
            values.append(value)


            ### Checking Conflicts
            var_neighbors = self.crossword.neighbors(var)
            for neighbor in var_neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment:
                    if assignment[var][overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False
                    
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        out_list = []

        for value in self.domains[var]:
            n = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    continue

                (i, j) = self.crossword.overlaps[var, neighbor]
                for neighbor_value in self.domains[neighbor]:
                    if not(value[i] == neighbor_value[j]):
                        n += 1
            out_list.append((value, n))
        
        out_list = sorted(out_list, key=lambda weight: weight[1])

        ret_list = []
        for i in out_list:
            ret_list.append(i[0])
        
        return ret_list


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        ret_variable = None
        min_value = 10 ** 9
        for var in self.domains:
            if var in assignment:
                continue

            if len(self.domains[var]) < min_value:
                ret_variable = var
                min_value = len(self.domains[var])
            
            elif len(self.domains) == min_value:
                if self.crossword.neighbors(var): 
                    if self.crossword.neighbors(var) > self.crossword.neighbors(ret_variable):
                        ret_variable = var

        return ret_variable
    

    # def Inference(assignment):

    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        #print("var, ", var)
        for value in self.order_domain_values(var, assignment):
            #print("value,", value)
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                #self.ac3()
                result = self.backtrack(new_assignment)
                self.times += 1
                #print(result, "times = ", self.times)
                if result is not None:
                    return result

            new_assignment.pop(var)

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
