import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """
    # constructor either creates mines from minesLis or if minesLis is none randomly creates mines
    def __init__(self, height=8, width=8, mines=8,minesLis=None):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)
        if minesLis is None:
        # Add mines randomly
            while len(self.mines) != mines:
                i = random.randrange(height)
                j = random.randrange(width)
                if not self.board[i][j]:
                    self.mines.add((i, j))
                    self.board[i][j] = True
        else:
            self.mines  = set()
            for i in minesLis:
                self.board[i[0]][i[1]] = True
                self.mines.add((i[0], i[1]))



        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0
        print(cell)
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines






class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        try:
            self.cells.remove(cell)
            self.count -= 1
        except KeyError:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        try:
            self.cells.remove(cell)
        except Exception:
            pass


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def close_cells(self, cell):
        """
        Returns a list of cells surrounding the given cell.
        """

        # Keep count of nearby mines
        count = []

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    count.append((i,j))

        return count



    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function will update the knowledge representation as so:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # initial setup adding to our safes and moves made while also initializing the cells
        # that will go in our new sentence

        self.moves_made.add(cell)
        self.mark_safe(cell)
        cells = set()
        count_cpy = count

        # look through adjacent cells
        for cell1 in self.close_cells(cell):
            # Add the cell to the cells set if it is not marked safe or as a mine
            if cell1 not in self.safes and cell1 not in self.mines:
                cells.add(cell1)
            # If the cell is a mine, decrease the count
            if cell1 in self.mines:
                count_cpy -= 1

        # check if given cell are all mines
        if len(cells) == count_cpy:
            for cell1 in cells:
                self.mark_mine(cell1)

        # checks if given cells are all safe
        if count_cpy == 0:
            for cell1 in cells:
                self.mark_safe(cell1)


        # Create a sentence with the cells set and remaining count
        cent = Sentence(cells, count_cpy)
        if len(cent.cells)>0:
            self.knowledge.append(cent)

        # used for new inference
        lis = []
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            if cells != sentence.cells:
                # If cells is a subset of sentence's cells, create a new sentence and add to list
                if cells.issubset(sentence.cells):
                    lis.append(Sentence(sentence.cells-cells,sentence.count-count_cpy))
                # If cells includes sentence's cells, create a new sentence and add it to the list
                if cells.issuperset(sentence.cells):
                    lis.append(Sentence(cells-sentence.cells,count_cpy-sentence.count))

        # Add new inferences to the AI's knowledge
        for i in lis:
            if len(i.cells)>0:
                self.knowledge.append(i)

        # use to see if new inferences or knowledge can be made from previous knowledge
        self.extra_inference()
        self.check_knowledge()



    def check_knowledge(self):
        """
        check knowledge for new safes and mines, updates knowledge if possible
        """
        # copies the knowledge to operate on copy
        # iterates through sentences

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                try:
                    self.knowledge.remove(sentence)
                except ValueError:
                    pass

            # check for possible mines and safes
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            # update knowledge if mine or safe was found
            if mines:
                for mine in list(mines):  # convert set to list for iteration
                    self.mark_mine(mine)
                    self.check_knowledge()
            if safes:
                for safe in list(safes):  # convert set to list for iteration
                    self.mark_safe(safe)
                    self.check_knowledge()


    def extra_inference(self):
        """
        update knowledge based on inference
        """
        # Iterate through every pair of sentences in the AI's knowledge base
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # Check if the cells from sentence1 are a subset of the cells from sentence2
                if sentence1.cells.issubset(sentence2.cells):
                    # Find the remaining cells and corresponding count by subtracting sentence1 from sentence2
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count

                    # Create a new sentence with the new cells and count
                    new_sentence = Sentence(new_cells, new_count)

                    # Get any known mine locations and safe cells from the new sentence and mark any known mines or safes
                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()

                    # Mark mine or safes if known
                    if mines:
                        for mine in mines:
                            self.mark_mine(mine)

                    if safes:
                        for safe in safes:
                            self.mark_safe(safe)





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """


        try:
            while True:
                val = self.safes.pop()
                if val not in self.moves_made:
                    return val
        except KeyError:
            return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # If the knowledge base is not empty we will find the cell with the
        # lowest probability of being a mine
        if len(self.knowledge)!=0:
            # Initialize the lowest probability of a cell being a mine as 1
            minProb = 1

            # bestMove will be used to store the best (i.e., lowest probability) move found
            bestMove = None
            for sentence in self.knowledge:
                # If the sentence has cells and has a lower mine probability than the current minimum
                if len(sentence.cells) != 0 and sentence.count / len(sentence.cells) < minProb:

                    # Select a random cell from this sentence
                    bestMove = random.choice(list(sentence.cells))

                    # Make sure that the selected cell has not already been chosen or marked as a mine
                    while bestMove in self.moves_made or bestMove in self.mines:
                        bestMove = random.choice(list(sentence.cells))

            # If a best move was found among the knowledge, return it
            if bestMove is not None:
                return bestMove

         # If no move can be inferred from the knowledge base, then a random cell is selected
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    return i, j
     








