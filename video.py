from manim import *

import minesweeper
from minesweeper import *


class CreateMinefieldFilm3(Scene):
    def create_game(self):
        self.minesweeper = Minesweeper(height=4, width=4, minesLis=[])
        self.solver = MinesweeperAI()
        self.revealed = set()
        self.revealed.add((0,0))
        self.revealed.add((1,0))
        self.revealed.add((0,1))
        self.revealed.add((1,1))


    def construct(self):
        self.create_game()
        square = Square(side_length=.75)  # create a circle
        square.to_corner(UL)
        square.shift(DOWN)
        square.shift(RIGHT)
        # square.set_fill(PINK, opacity=0.5)# set the color and transparency
        squares, textEle, coords = self.place_row(3, square)
        self.clear()
        text = Text("Inferred Sentences")
        self.play(AddTextLetterByLetter(text))
        self.wait(5)
        text.shift(UP*2)
        square = Square(side_length=.75)
        square.shift(LEFT*3)
        self.minesweeper = Minesweeper(height=4, width=4, minesLis=[[1,1],[0,2]])
        self.revealed = set()
        self.revealed.add((0,0))
        self.revealed.add((1,0))
        self.revealed.add((2,0))
        self.revealed.add((1,2))
        newDict = {(0,1):"A",(1,1):"B",(2,1):"C",(0,2):"D",(2,2):"E"}
        self.place_row2(3,square,newDict)


    def place_row(self, length, head):
        squares = []  # List to store all squares
        texts = []
        textEle = []
        fadeOut = []
        coords = []
        head.set_fill(GREEN, opacity=1)
        for i in range(length):
            square = Square(side_length=.75)
            square.shift(head.get_center() + i * RIGHT)
            lis = ()
            lis += (FadeIn(square),)
            squares.append([])  # Append to squares list
            textEle.append([])
            coords.append([])
            for j in range(length):
                square1 = Square(side_length=.75)
                square1.shift(square.get_center() + j * DOWN)

                if i == 0:
                    text1 = Text(f"{j}")
                    text1.next_to(square1, LEFT)
                    lis += (FadeIn(text1),)
                    coords[i].append(text1)
                if j == 0:
                    coords.append([])
                    text1 = Text(f"{i}")
                    text1.next_to(square1, UP)
                    lis += (FadeIn(text1),)

                    coords[1].append(text1)

                lis += (FadeIn(square1),)
                squares[i].append(square1)
                if i == 0 and j == 0:
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))

                # text = Text(str(self.minesweeper.nearby_mines((i, j))))
                text = None
                if j == 0 and i == 1:
                    text = Text("A")
                elif j == 1 and i == 1:
                    text = Text("B")
                elif j == 1 and i == 0:
                    text = Text("C")
                else:
                    text = Text(str(self.minesweeper.nearby_mines((i, j))))

                if self.minesweeper.board[i][j]:
                    text = Text("M", color=BLUE)
                    square1_scaled = square1.animate.scale(1.5).set_fill(LIGHT_BROWN, opacity=1)
                    texts.append(square1_scaled)
                    # square1_scaled_scaled_down = square1.scale(1 / 1.5)

                    # fadeOut2.append(square1.animate.scale(1/1.5))
                    fadeOut.append(FadeOut(text))
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))


                elif (i,j) in self.revealed:
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))

                # Append to squares list
            self.play(FadeIn(square), lis,run_time=.5)
        # Fill all squares with green

        # Group all squares together
        vgroup = VGroup(*[sq for sublist in squares for sq in sublist])

        self.play(
            AnimationGroup(
                vgroup.animate.set_fill(GREEN, opacity=1).scale(1.2),  # Fill and scale up
                lag_ratio=0
            ),
            run_time=1
        )
        self.play(vgroup.animate.scale(1 / 1.2), run_time=1)  # Scale down

        # self.wait(2)
        # self.play(AnimationGroup(*shrink_animations, lag_ratio=0.1))

        # Wait for a moment to show the final grid

        tt1 = Text("{A, B, C} = 0")
        tt1.next_to(head, RIGHT * 10)
        self.play(AddTextLetterByLetter(tt1),*texts)
        self.wait(4)

        for i in range(len(self.minesweeper.board)):
            for j in range(len(self.minesweeper.board[i])):
                if self.minesweeper.board[i][j]:
                    fadeOut.append(squares[i][j].animate.scale(1/1.5))
        self.play(*fadeOut)
        self.wait(9)



        return squares, textEle, coords

    def place_row2(self, length, head,my_dict):
        squares = []  # List to store all squares
        texts = []
        textEle = []
        fadeOut = []
        coords = []
        head.set_fill(GREEN, opacity=1)
        for i in range(length):
            square = Square(side_length=.75)
            square.shift(head.get_center() + i * RIGHT)
            lis = ()
            lis += (FadeIn(square),)
            squares.append([])  # Append to squares list
            textEle.append([])
            for j in range(length):
                square1 = Square(side_length=.75)
                square1.shift(square.get_center() + j * DOWN)

                if i == 0:
                    coords.append([])
                    text1 = Text(f"{j}")
                    text1.next_to(square1, LEFT)
                    lis += (FadeIn(text1),)
                    coords[i].append(text1)
                if j == 0:
                    coords.append([])
                    text1 = Text(f"{i}")
                    text1.next_to(square1, UP)
                    lis += (FadeIn(text1),)

                    coords[1].append(text1)

                lis += (FadeIn(square1),)
                squares[i].append(square1)
                if i == 1 and j == 0:
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))
                if i == 1 and j == 2:
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))

                # text = Text(str(self.minesweeper.nearby_mines((i, j))))

                text = Text(str(self.minesweeper.nearby_mines((i, j))))
                if (i, j) in my_dict:
                    text = Text(my_dict[(i, j)])

                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))
                    textEle[i].append(text)

                elif self.minesweeper.board[i][j]:
                    text = Text("M", color=BLUE)
                    square1_scaled = square1.animate.scale(1.5).set_fill(LIGHT_BROWN, opacity=1)
                    texts.append(square1_scaled)
                    # square1_scaled_scaled_down = square1.scale(1 / 1.5)

                    # fadeOut2.append(square1.animate.scale(1/1.5))
                    fadeOut.append(FadeOut(text))
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))

                    textEle[i].append(text)


                elif (i,j) in self.revealed:
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))
                    textEle[i].append(text)



                # Append to squares list
            self.play(FadeIn(square), lis,run_time=.5)
        # Fill all squares with green

        # Group all squares together
        vgroup = VGroup(*[sq for sublist in squares for sq in sublist])

        self.play(
            AnimationGroup(
                vgroup.animate.set_fill(GREEN, opacity=1).scale(1.2),  # Fill and scale up
                lag_ratio=0
            ),
            run_time=1
        )
        self.play(vgroup.animate.scale(1 / 1.2), run_time=1)  # Scale down

        # self.wait(2)
        # self.play(AnimationGroup(*shrink_animations, lag_ratio=0.1))

        # Wait for a moment to show the final grid


        self.play(*texts)
        self.wait(3)
        # for i in range(len(self.minesweeper.board)):
        #     for j in range(len(self.minesweeper.board[i])):
        #         if self.minesweeper.board[i][j]:
        #             fadeOut.append(squares[i][j].animate.scale(1/1.5))
        self.play(*fadeOut)
        text1 = Text("(1,0) -> {A, B, C} = 1",font_size=30)
        text2 = Text("(1,2) -> {A, B, C, D, E} = 2",font_size=30)
        text1.shift(RIGHT*2)
        text2.shift(RIGHT*2+DOWN*2)
        self.play(ReplacementTransform(squares[1][0].copy(),text1),ReplacementTransform(squares[1][2].copy(),text2))
        self.wait(2)
        text3 = Text("{A, B, C, D, E} - {A, B, C} = {D, E}\n\n2 - 1 = 1\n\nNew Sentence -> {D, E} = 1",font_size=30)
        text4 = Text("New Sentence -> Set2 - Set1 = Count2 - Count1",font_size=30)
        text3.move_to(text1.get_center())
        text3.shift(RIGHT)
        text4.move_to(text2.get_center())
        lis2 = []
        for i in range(len(squares)):
            for j in range(len(squares[i])):
                lis2.append(squares[i][j].animate.shift(LEFT*2))
                lis2.append(textEle[i][j].animate.shift(LEFT*2))
        for i in coords:
            for j in i:
                lis2.append(j.animate.shift(LEFT*2))
        self.play(Transform(text1,text3), Transform(text2,text4),*lis2)
        self.wait(15)



        return squares, textEle, coords

class CreateMinefieldFilm2(Scene):
    def create_game(self):
        self.minesweeper = Minesweeper(height=4, width=4, minesLis=[[2, 1],[0,2],[2,2]])
        self.solver = MinesweeperAI()
        self.revealed = set()
        self.revealed.add((0,0))
        self.revealed.add((1,0))
        self.revealed.add((0,1))
        self.revealed.add((1,1))


    def construct(self):
        self.create_game()
        square = Square(side_length=.75)  # create a circle
        square.to_corner(UL)
        square.shift(DOWN)
        square.shift(RIGHT)
        # square.set_fill(PINK, opacity=0.5)# set the color and transparency
        squares, textEle, coords = self.place_row(3, square)
        self.scence2(squares, textEle, coords)

    def place_row(self, length, head):
        squares = []  # List to store all squares
        texts = []
        textEle = []
        fadeOut = []
        coords = []
        head.set_fill(GREEN, opacity=1)
        for i in range(length):
            square = Square(side_length=.75)
            square.shift(head.get_center() + i * RIGHT)
            lis = ()
            lis += (FadeIn(square),)
            squares.append([])  # Append to squares list
            textEle.append([])
            coords.append([])
            for j in range(length):
                square1 = Square(side_length=.75)
                square1.shift(square.get_center() + j * DOWN)

                if i == 0:
                    text1 = Text(f"{j}")
                    text1.next_to(square1, LEFT)
                    lis += (FadeIn(text1),)
                    coords[i].append(text1)
                if j == 0:
                    coords.append([])
                    text1 = Text(f"{i}")
                    text1.next_to(square1, UP)
                    lis += (FadeIn(text1),)

                    coords[1].append(text1)

                lis += (FadeIn(square1),)
                squares[i].append(square1)
                if i == 1 and j == 1:
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))
                text = Text(str(self.minesweeper.nearby_mines((i, j))))
                textEle[i].append(text)
                if self.minesweeper.board[i][j]:
                    text = Text("M", color=BLUE)
                    square1_scaled = square1.animate.scale(1.5).set_fill(LIGHT_BROWN, opacity=1)
                    texts.append(square1_scaled)
                    # square1_scaled_scaled_down = square1.scale(1 / 1.5)

                    # fadeOut2.append(square1.animate.scale(1/1.5))
                    fadeOut.append(FadeOut(text))
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))


                elif (i,j) in self.revealed:
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))

                # Append to squares list
            self.play(FadeIn(square), lis,run_time=.5)
        # Fill all squares with green

        # Group all squares together
        vgroup = VGroup(*[sq for sublist in squares for sq in sublist])

        self.play(
            AnimationGroup(
                vgroup.animate.set_fill(GREEN, opacity=1).scale(1.2),  # Fill and scale up
                lag_ratio=0
            ),
            run_time=1
        )
        self.play(vgroup.animate.scale(1 / 1.2), run_time=1)  # Scale down

        # self.wait(2)
        # self.play(AnimationGroup(*shrink_animations, lag_ratio=0.1))

        # Wait for a moment to show the final grid

        self.play(*texts)
        self.wait(4)

        for i in range(len(self.minesweeper.board)):
            for j in range(len(self.minesweeper.board[i])):
                if self.minesweeper.board[i][j]:
                    fadeOut.append(squares[i][j].animate.scale(1/1.5))
        self.play(*fadeOut)
        self.wait(6)
        self.play(squares[1][1].animate.scale(1/1.5))
        self.play(squares[2][2].animate.scale(1.5))


        return squares, textEle, coords
    def place_row2(self, length, head,heading):
        squares = []  # List to store all squares
        texts = []
        textEle = []
        fadeOut = []
        coords = []
        head.set_fill(GREEN, opacity=1)
        for i in range(length):
            square = Square(side_length=.75)
            square.shift(head.get_center() + i * RIGHT)
            lis = ()
            lis += (FadeIn(square),)
            squares.append([])  # Append to squares list
            textEle.append([])
            coords.append([])
            ctr=0
            for j in range(length):
                square1 = Square(side_length=.75)
                square1.shift(square.get_center() + j * DOWN)

                if i == 0:
                    text1 = Text(f"{j}")
                    text1.next_to(square1, LEFT)
                    lis += (FadeIn(text1),)
                    coords[i].append(text1)
                if j == 0:
                    coords.append([])
                    text1 = Text(f"{i}")
                    text1.next_to(square1, UP)
                    lis += (FadeIn(text1),)

                    coords[1].append(text1)

                lis += (FadeIn(square1),)
                squares[i].append(square1)
                c = self.minesweeper.width-1
                text = Text(chr(j*c+i+65-ctr*i))
                if i == 1 and j == 1:
                    text = Text("1")
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))
                    ctr=1
                if i == 0 and j == 2:
                    text = Text("F")
                if i == 2 and j == 1:
                    text = Text("E")
                if i == 2 and j == 2:
                    text = Text("H")
                text.move_to(square1.get_center())
                textEle[i].append(text)
                texts.append(FadeIn(text))




                # Append to squares list
            self.play(FadeIn(square), lis,run_time=.5)
        # Fill all squares with green

        # Group all squares together
        vgroup = VGroup(*[sq for sublist in squares for sq in sublist])

        self.play(
            AnimationGroup(
                vgroup.animate.set_fill(GREEN, opacity=1).scale(1.2),  # Fill and scale up
                lag_ratio=0
            ),
            run_time=1
        )
        self.play(vgroup.animate.scale(1 / 1.2), run_time=1)  # Scale down
        squares[1][1].set_fill(BLUE, opacity=1)

        # self.wait(2)
        # self.play(AnimationGroup(*shrink_animations, lag_ratio=0.1))

        # Wait for a moment to show the final grid

        self.play(*texts)
        self.wait(4)
        lis2=[]
        for i in range(len(squares)):
            for j in range(len(squares[i])):
                lis2.append(squares[i][j].animate.shift(LEFT*2))
                lis2.append(textEle[i][j].animate.shift(LEFT*2))
        for i in coords:
            for j in i:
                lis2.append(j.animate.shift(LEFT*2))
        lis2.append(heading.animate.shift(LEFT*2))
        prepLogic = Text("Or(A, B, C, D, E, F, G, H)",font_size=30)
        prepLogic.next_to(heading,RIGHT)
        prepLogic.shift(LEFT)
        self.play(lis2,AddTextLetterByLetter(prepLogic))
        self.wait(10)
        prepLogic2 = Text("""Or(
    And(A, Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), B, Not(C), Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), C, Not(D), Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), D, Not(E), Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), E, Not(F), Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), F, Not(G), Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), G, Not(H)),
    And(Not(A), Not(B), Not(C), Not(D), Not(E), Not(F), Not(G), H)
)""",font_size=20)
        prepLogic2.move_to(prepLogic.get_center())
        heading.shift(LEFT+UP)
        prepLogic2.shift(LEFT+DOWN)
        self.play(Transform(prepLogic, prepLogic2))
        self.wait(26)
        sentence = Text("{A, B, C, D, E, F, G, H} = 1")
        sentence.move_to(prepLogic2.get_center())
        self.play(Transform(prepLogic,sentence))
        self.wait(21)


        return squares, textEle, coords
    def scence2(self, squares, texts, coords):
        moveDown = []
        for i in range(len(squares)):
            for j in range(len(squares[i])):
                moveDown.append(squares[i][j].animate.shift(DOWN * 2))
                if i != 2 or j != 2:
                        if (i,j) in self.revealed:
                            moveDown.append(texts[i][j].animate.shift(DOWN * 2))
                else:
                    mine_copy = squares[i][j].copy()
                    text = Text("Mines = {{2,2}}")
                    text.move_to(squares[i][j].get_center() + UP * 2 + LEFT)

                    # moveDown.append(mine_copy.animate.shift(UP*4))
                    moveDown.append(Transform(mine_copy, text))
                    self.remove(mine_copy)
        for i in range(len(coords[0])):
            moveDown.append(coords[0][i].animate.shift(DOWN * 2))
            moveDown.append(coords[1][i].animate.shift(DOWN * 2))
        self.play(*moveDown, run_time=2)
        scene2 = []
        scene2.append(squares[2][2].animate.scale(1/1.5))
        scene2.append(squares[0][1].animate.set_fill(RED, opacity=1))
        scene2.append(squares[1][0].animate.set_fill(RED, opacity=1))
        scene2.append(squares[2][0].animate.scale(1.5).set_fill(BLUE, opacity=1))
        scene2.append(squares[2][1].animate.scale(1.5).set_fill(BLUE, opacity=1))
        scene2.append(squares[0][2].animate.scale(1.5).set_fill(BLUE, opacity=1))
        scene2.append(squares[1][2].animate.scale(1.5).set_fill(BLUE, opacity=1))
        self.play(*scene2)
        self.wait(8)
        scene3 = []
        scene3.append(squares[2][0].animate.scale(1/1.5))
        scene3.append(squares[2][1].animate.scale(1/1.5))
        scene3.append(squares[0][2].animate.scale(1/1.5))
        scene3.append(squares[1][2].animate.scale(1/1.5))
        scene3.append(squares[2][2].animate.scale(1.5))
        self.play(*scene3)
        self.wait(33)
        self.clear()
        prepLogicText = Text("Prepositional Logic")
        self.play(AddTextLetterByLetter(prepLogicText))
        self.wait(12)
        square = Square(side_length=.75)

        square.next_to(prepLogicText, DOWN*2)
        square.shift(LEFT*2)
        self.play(prepLogicText.animate.shift(UP))# create a circle
        # square.set_fill(PINK, opacity=0.5)# set the color and transparency
        squares, textEle, coords = self.place_row2(3, square,prepLogicText)


class CreateMinefieldFilm1(Scene):
    def create_game(self):
        self.minesweeper = Minesweeper(height=3, width=3, minesLis=[[2, 2]])
        self.solver = MinesweeperAI()
        self.revealed = set()
        for i in range(self.minesweeper.height):
            for j in range(self.minesweeper.width):
                self.revealed.add((i, j))
        self.revealed.discard((2, 2))

    def construct(self):
        self.create_game()
        square = Square(side_length=.75)  # create a circle
        square.to_corner(UL)
        square.shift(DOWN)
        square.shift(RIGHT)
        # square.set_fill(PINK, opacity=0.5)# set the color and transparency
        squares, textEle, coords = self.place_row(3, square)
        self.scence2(squares, textEle, coords)
        # self.setupMinesweeper(squares)

    #     # self.play(Create(square))
    # def setupMinesweeper(self, squares):
    #     obj = []
    #     for i in range(self.minesweeper.height):  # loop through height first
    #         for j in range(self.minesweeper.width):  # then width
    #             if (i, j) in self.revealed:
    #                 text = Text(str(self.minesweeper.nearby_mines((i, j))))
    #                 square = squares[i][j]
    #                 text.move_to(squares[i][j].get_center())
    #                 obj.append(FadeIn(text))
    #     self.play(*obj)

    def scence2(self, squares, texts, coords):
        moveDown = []
        for i in range(len(squares)):
            for j in range(len(squares[i])):
                moveDown.append(squares[i][j].animate.shift(DOWN * 2))
                if i != 2 or j != 2:
                    moveDown.append(texts[i][j].animate.shift(DOWN * 2))
                else:
                    mine_copy = squares[i][j].copy()
                    text = Text("Mines = {{2,2}}")
                    text.move_to(squares[i][j].get_center() + UP * 2 + LEFT)

                    # moveDown.append(mine_copy.animate.shift(UP*4))
                    moveDown.append(ReplacementTransform(mine_copy, text))
                    self.remove(mine_copy)
        for i in range(len(coords[0])):
            moveDown.append(coords[0][i].animate.shift(DOWN * 2))
            moveDown.append(coords[1][i].animate.shift(DOWN * 2))
        self.play(*moveDown, run_time=2)
        self.wait(3)
        scene3 = []
        leftSqr = Text("0")
        leftSqr.move_to(squares[1][2])
        rightSqr = Text("0")
        rightSqr.move_to(squares[2][1])
        scene3.append(Transform(texts[1][2], leftSqr))
        scene3.append(Transform(texts[2][1], rightSqr))
        scene3.append(squares[1][1].animate.scale(1 / 1.5))
        scene3.append(squares[1][2].animate.scale(1.5).set_fill(BLUE))
        scene3.append(squares[2][1].animate.scale(1.5).set_fill(BLUE))
        for i in range(len(squares)):
            square = Square(side_length=.75)
            text = Text("0")

            square = square.next_to(squares[i][-1], DOWN)

            square.set_fill(BLUE, opacity=1)
            text.move_to(square.get_center())
            squares[i].append(square)
            texts[i].append(text)
            scene3.append(Create(square))

        row = []
        rowText = []
        for i in range(len(squares[-1])):

            square = Square(side_length=.75)
            text = Text("0")
            row.append(square)
            rowText.append(text)
            square.next_to(squares[-1][i], RIGHT)

            if i != len(squares):
                square.set_fill(BLUE, opacity=1)
            else:
                square.set_fill(RED, opacity=1)
            text.move_to(square.get_center())
            scene3.append(Create(square))

        text1 = Text("3")
        text1.next_to(coords[1][-1], RIGHT * 2.5)
        text2 = text1.copy()
        text2.next_to(coords[0][-1], DOWN * 2.5)
        scene3.append(Write(text1))
        scene3.append(Write(text2))

        squares.append(row)
        texts.append(rowText)

        self.play(*scene3)
        scene4 = []
        scene4.append(squares[1][2].animate.scale(1 / 1.5))
        scene4.append(squares[2][1].animate.scale(1 / 1.5))
        self.play(*scene4)

        self.wait(5)

    def place_row(self, length, head):
        squares = []  # List to store all squares
        texts = []
        textEle = []
        fadeOut = []
        coords = []
        head.set_fill(GREEN, opacity=1)
        for i in range(length):
            square = Square(side_length=.75)
            square.shift(head.get_center() + i * RIGHT)
            lis = ()
            lis += (FadeIn(square),)
            squares.append([])  # Append to squares list
            textEle.append([])
            coords.append([])
            for j in range(length):
                square1 = Square(side_length=.75)
                square1.shift(square.get_center() + j * DOWN)

                if i == 0:
                    text1 = Text(f"{j}")
                    text1.next_to(square1, LEFT)
                    lis += (FadeIn(text1),)
                    coords[i].append(text1)
                if j == 0:
                    coords.append([])
                    text1 = Text(f"{i}")
                    text1.next_to(square1, UP)
                    lis += (FadeIn(text1),)

                    coords[1].append(text1)

                lis += (FadeIn(square1),)
                squares[i].append(square1)
                if i == 1 and j == 1:
                    fadeOut.append(square1.animate.scale(1.5).set_fill(PINK, opacity=1))
                text = Text(str(self.minesweeper.nearby_mines((i, j))))
                textEle[i].append(text)
                if (i, j) not in self.revealed:
                    text = Text("M", color=BLUE)
                    square1_scaled = square1.animate.scale(1.5).set_fill(LIGHT_BROWN, opacity=1)
                    texts.append(square1_scaled)
                    # square1_scaled_scaled_down = square1.scale(1 / 1.5)

                    # fadeOut2.append(square1.animate.scale(1/1.5))
                    fadeOut.append(FadeOut(text))
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))

                else:
                    text.move_to(square1.get_center())
                    texts.append(FadeIn(text))

                # Append to squares list
            self.play(FadeIn(square), lis)
        # Fill all squares with green

        # Group all squares together
        vgroup = VGroup(*[sq for sublist in squares for sq in sublist])

        self.play(
            AnimationGroup(
                vgroup.animate.set_fill(GREEN, opacity=1).scale(1.2),  # Fill and scale up
                lag_ratio=0
            ),
            run_time=1
        )
        self.play(vgroup.animate.scale(1 / 1.2), run_time=0.5)  # Scale down

        # self.wait(2)
        # self.play(AnimationGroup(*shrink_animations, lag_ratio=0.1))

        # Wait for a moment to show the final grid
        self.wait(2)

        self.play(*texts)
        self.wait(4)
        self.play(*fadeOut, squares[2][2].animate.scale(1 / 1.5))
        self.wait(7)
        code = '''
import copy
import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """
    # constructor either creates mines from minesLis 
    # or if minesLis is none randomly creates mines 
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
            self.mines  = len(minesLis)
            for i in minesLis:
                self.board[i[0]][i[1]] = True



        # At first, player has found no mines
        self.mines_found = set()


'''
        rendered_code = Code(code=code, tab_width=4, background="window",
                             language="Python", font="Monospace", font_size=12, style=Code.styles_list[10])
        rendered_code.to_edge(RIGHT)
        rendered_code = Write(rendered_code)
        self.play(rendered_code)
        self.wait(11)
        return squares, textEle, coords


with tempconfig({"quality": "low_quality", "disable_caching": True}):
    # scene = CreateMinefieldFilm1()
    # scene.render()

    scene1 = CreateMinefieldFilm3()
    scene1.render()
