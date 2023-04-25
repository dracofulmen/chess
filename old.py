# ♖♘♗♕♔♙ Pieces
# ┌ ┐ └ ┘ ┼ ┬ ┴ ├ ┤ │ ─ Board
import os

for x in range(0, 1):
    turns = 1
    win = 0
    bc = 0
    wc = 0
    enby = 0
    enbx = 0
    enwy = 0
    enwx = 0
    btaken = []
    wtaken = []
    bpromotion = []
    wpromotion = []
    board = [["Rbl", "Nbl", "Bbl", "Qbl", "Kbl", "Bbl", "Nbl", "Rbl"],
             ["Pbl", "Pbl", "Pbl", "Pbl", "Pbl", "Pbl", "Pbl", "Pbl"],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             [" ", " ", " ", " ", " ", " ", " ", " "],
             ["P", "P", "P", "P", "P", "P", "P", "P"],
             ["R", "N", "B", "Q", "K", "B", "N", "R"]]
    full = [board, turns, bc, wc, enby, enbx, enwy, enwx, btaken, wtaken, bpromotion, wpromotion]


    def check_check(full, king):
        kingy = ""
        kingx = ""
        kingkind = ""
        done = ""
        for y in range(0, 8):
            for x in range(0, 8):
                if (full[0][y][x] == king):
                    kingy = y
                    kingx = x
                    if ("bl" in king):
                        kingkind = "b"
                    else:
                        kingkind = "w"
                    break
        if (kingkind == "b"):
            for x in range(0, kingx):
                if (full[0][kingy][x] == "R" or full[0][kingy][x] == "Q"):
                    done = 0
                elif (full[0][kingy][x] != " "):
                    done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for x in range(kingx + 1, 8):
                if (full[0][kingy][counter] == "R" or full[0][kingy][counter] == "Q"):
                    done = 0
                elif (full[0][kingy][counter] != " "):
                    done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for x in range(0, kingy):
                if (full[0][x][kingx] == "R" or full[0][x][kingx] == "Q"):
                    done = 0
                elif (full[0][x][kingx] != " "):
                    done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for x in range(kingy + 1, 8):
                if (full[0][counter][kingx] == "R" or full[0][counter][kingx] == "Q"):
                    done = 0
                elif (full[0][counter][kingx] != " "):
                    done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for y in range(0, kingy):
                x = (kingx - kingy) + y
                if (x < 8 and x > -1):
                    if (full[0][y][x] == "B" or full[0][y][x] == "Q"):
                        done = 0
                    elif (full[0][y][x] != " "):
                        done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for y in range(kingy + 1, 8):
                x = (kingx - kingy) + counter
                if (x < 8 and x > -1):
                    if (full[0][counter][x] == "B" or full[0][counter][x] == "Q"):
                        done = 0
                    elif (full[0][counter][x] != " "):
                        done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for y in range(0, kingy):
                x = (kingx + kingy) - y
                if (x < 8 and x > -1):
                    if (full[0][y][x] == "B" or full[0][y][x] == "Q"):
                        done = 0
                    elif (full[0][y][x] != " "):
                        done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for y in range(kingy + 1, 8):
                x = (kingx + kingy) - counter
                if (x < 8 and x > -1):
                    if (full[0][counter][x] == "B" or full[0][counter][x] == "Q"):
                        done = 0
                    elif (full[0][counter][x] != " "):
                        done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy + 1][kingx + 1] == "P"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy + 1][kingx - 1] == "P"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 2 > -1 and kingy + 2 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy + 2][kingx - 1] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 2 > -1 and kingy + 2 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy + 2][kingx + 1] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 2 > -1 and kingy - 2 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy - 2][kingx - 1] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 2 > -1 and kingy - 2 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy - 2][kingx + 1] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx + 2 > -1 and kingx + 2 < 8):
                if (full[0][kingy - 1][kingx + 2] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx + 2 > -1 and kingx + 2 < 8):
                if (full[0][kingy + 1][kingx + 2] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx - 2 > -1 and kingx - 2 < 8):
                if (full[0][kingy - 1][kingx - 2] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx - 2 > -1 and kingx - 2 < 8):
                if (full[0][kingy + 1][kingx - 2] == "N"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
        elif (kingkind == "w"):
            for x in range(0, kingx):
                if (full[0][kingy][x] == "Rbl" or full[0][kingy][x] == "Qbl"):
                    done = 0
                elif (full[0][kingy][x] != " "):
                    done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for x in range(kingx + 1, 8):
                if (full[0][kingy][counter] == "Rbl" or full[0][kingy][counter] == "Qbl"):
                    done = 0
                elif (full[0][kingy][counter] != " "):
                    done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for x in range(0, kingy):
                if (full[0][x][kingx] == "Rbl" or full[0][x][kingx] == "Qbl"):
                    done = 0
                elif (full[0][x][kingx] != " "):
                    done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for x in range(kingy + 1, 8):
                if (full[0][counter][kingx] == "Rbl" or full[0][counter][kingx] == "Qbl"):
                    done = 0
                elif (full[0][counter][kingx] != " "):
                    done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for y in range(0, kingy):
                x = (kingx - kingy) + y
                if (x < 8 and x > -1):
                    if (full[0][y][x] == "Bbl" or full[0][y][x] == "Qbl"):
                        done = 0
                    elif (full[0][y][x] != " "):
                        done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for y in range(kingy + 1, 8):
                x = (kingx - kingy) + counter
                if (x < 8 and x > -1):
                    if (full[0][counter][x] == "Bbl" or full[0][counter][x] == "Qbl"):
                        done = 0
                    elif (full[0][counter][x] != " "):
                        done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            for y in range(0, kingy):
                x = (kingx + kingy) - y
                if (x < 8 and x > -1):
                    if (full[0][y][x] == "Bbl" or full[0][y][x] == "Qbl"):
                        done = 0
                    elif (full[0][y][x] != " "):
                        done = 1
            if (done == 0):
                return "check"
            done = ""
            counter = 7
            for y in range(kingy + 1, 8):
                x = (kingx + kingy) - counter
                if (x < 8 and x > -1):
                    if (full[0][counter][x] == "Bbl" or full[0][counter][x] == "Qbl"):
                        done = 0
                    elif (full[0][counter][x] != " "):
                        done = 1
                counter = counter - 1
            if (done == 0):
                return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy - 1][kingx + 1] == "Pbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy - 1][kingx - 1] == "Pbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 2 > -1 and kingy + 2 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy + 2][kingx - 1] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 2 > -1 and kingy + 2 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy + 2][kingx + 1] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 2 > -1 and kingy - 2 < 8 and kingx - 1 > -1 and kingx - 1 < 8):
                if (full[0][kingy - 2][kingx - 1] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 2 > -1 and kingy - 2 < 8 and kingx + 1 > -1 and kingx + 1 < 8):
                if (full[0][kingy - 2][kingx + 1] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx + 2 > -1 and kingx + 2 < 8):
                if (full[0][kingy - 1][kingx + 2] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx + 2 > -1 and kingx + 2 < 8):
                if (full[0][kingy + 1][kingx + 2] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy - 1 > -1 and kingy - 1 < 8 and kingx - 2 > -1 and kingx - 2 < 8):
                if (full[0][kingy - 1][kingx - 2] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
            if (kingy + 1 > -1 and kingy + 1 < 8 and kingx - 2 > -1 and kingx - 2 < 8):
                if (full[0][kingy + 1][kingx - 2] == "Nbl"):
                    done = 0
                else:
                    done = 1
                if (done == 0):
                    return "check"
            done = ""
        return ""


    def board_print(full):
        counter = 8
        print("\033[0m     A   B   C   D   E   F   G   H  ")
        print("\033[0m   ┌───┬───┬───┬───┬───┬───┬───┬───┐")
        for y in range(0, 8):
            print(" " + str(counter) + " ", end="")
            for x in range(0, 8):
                print("\033[0m│", end="")
                piece = full[0][y][x]
                piece2 = ""
                if ("bl" not in piece):
                    if ("R" in piece):
                        piece2 = "\033[0m ♖ "
                    elif ("N" in piece):
                        piece2 = "\033[0m ♘ "
                    elif ("B" in piece):
                        piece2 = "\033[0m ♗ "
                    elif ("Q" in piece):
                        piece2 = "\033[0m ♕ "
                    elif ("K" in piece):
                        piece2 = "\033[0m ♔ "
                    elif ("P" in piece):
                        piece2 = "\033[0m ♙ "
                    else:
                        piece2 = "\033[0m   "
                else:
                    if ("R" in piece):
                        piece2 = "\033[0;34m ♖ "
                    elif ("N" in piece):
                        piece2 = "\033[0;34m ♘ "
                    elif ("B" in piece):
                        piece2 = "\033[0;34m ♗ "
                    elif ("Q" in piece):
                        piece2 = "\033[0;34m ♕ "
                    elif ("K" in piece):
                        piece2 = "\033[0;34m ♔ "
                    elif ("P" in piece):
                        piece2 = "\033[0;34m ♙ "
                    else:
                        piece2 = "\033[0m   "
                if ("bl" in full[0][y][x]):
                    print(piece2, end="")
                else:
                    print(piece2, end="")
            print("\033[0m│", end="")
            print(" " + str(counter) + " ")
            counter = counter - 1
            if (y != 7):
                print("\033[0m   ├───┼───┼───┼───┼───┼───┼───┼───┤")
            else:
                print("\033[0m   └───┴───┴───┴───┴───┴───┴───┴───┘")
                print("\033[0m     A   B   C   D   E   F   G   H  ")
        for x in range(0, len(full[10])):
            if (full[10][x] in full[8]):
                full[8].remove(full[10][x])
                full[10].remove(full[10][x])
                full[8].append("Pbl")
        for x in range(0, len(full[11])):
            if (full[11][x] in full[9]):
                full[9].remove(full[11][x])
                full[11].remove(full[11][x])
                full[9].append("P")
        counter = 0
        if (len(full[8]) > 0):
            print("\033[0mWhite: ", end="")
            for x in range(0, len(full[8])):
                piece = full[8][x]
                piece2 = ""
                if ("R" in piece):
                    piece2 = "\033[0;34m♖"
                    counter = counter + 5
                elif ("N" in piece):
                    piece2 = "\033[0;34m♘"
                    counter = counter + 3
                elif ("B" in piece):
                    piece2 = "\033[0;34m♗"
                    counter = counter + 3
                elif ("Q" in piece):
                    piece2 = "\033[0;34m♕"
                    counter = counter + 9
                elif ("K" in piece):
                    piece2 = "\033[0;34m♔"
                    counter = counter + 0
                elif ("P" in piece):
                    piece2 = "\033[0;34m♙"
                    counter = counter + 1
                else:
                    piece2 = "\033[0m"
                    counter = counter + 0
                print("\033[0;34m" + piece2, end="")
            print("\033[0;1m + " + str(counter))
        counter = 0
        if (len(full[9]) > 0):
            print("\033[0;34mBlack: ", end="")
            for x in range(0, len(full[9])):
                piece = full[9][x]
                piece2 = ""
                if ("R" in piece):
                    piece2 = "\033[0m♖"
                    counter = counter + 5
                elif ("N" in piece):
                    piece2 = "\033[0m♘"
                    counter = counter + 3
                elif ("B" in piece):
                    piece2 = "\033[0m♗"
                    counter = counter + 3
                elif ("Q" in piece):
                    piece2 = "\033[0m♕"
                    counter = counter + 9
                elif ("K" in piece):
                    piece2 = "\033[0m♔"
                    counter = counter + 0
                elif ("P" in piece):
                    piece2 = "\033[0m♙"
                    counter = counter + 1
                else:
                    piece2 = "\033[0m"
                    counter = counter + 0
                print("\033[0m" + piece2, end="")
            print("\033[0;1m + " + str(counter))


    def move(full):
        if (full[1] / 2 == int(full[1] / 2)):
            if (check_check(full, "Kbl") == "check"):
                print("\033[0;31;1mYou are in check!")
            print("\033[0;34;1mBlack's Turn:")
            full[4] = 0
            full[5] = 0
            player = 2
        else:
            if (check_check(full, "K") == "check"):
                print("\033[0;31;1mYou are in check!")
            print("\033[0;1mWhite's Turn:")
            full[6] = 0
            full[7] = 0
            player = 1
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        nums = ["8", "7", "6", "5", "4", "3", "2", "1"]
        choice = input("\033[0mWhich piece would you like to move?\n").lower()
        boardx = ""
        boardy = ""
        for x in range(0, 8):
            if (letters[x] in choice):
                boardx = x
                break
        if (boardx == ""):
            print("Invalid.")
            return full
        else:
            for x in range(0, 8):
                if (nums[x] in choice):
                    boardy = x
                    break
            if (boardy == ""):
                print("Invalid.")
                return full
        if (full[0][boardy][boardx] == " "):
            print("Invalid.")
            return full
        else:
            if ("R" in full[0][boardy][boardx]):
                piece = "R"
            elif ("N" in full[0][boardy][boardx]):
                piece = "N"
            elif ("B" in full[0][boardy][boardx]):
                piece = "B"
            elif ("Q" in full[0][boardy][boardx]):
                piece = "Q"
            elif ("K" in full[0][boardy][boardx]):
                piece = "K"
            elif ("P" in full[0][boardy][boardx]):
                piece = "P"
        if ("bl" in full[0][boardy][boardx]):
            if (player == 1):
                print("Invalid.")
                return full
        else:
            if (player == 2):
                print("Invalid.")
                return full
        choice = input("\033[0mWhere do you want to move that piece?\n").lower()
        pboardx = ""
        pboardy = ""
        for x in range(0, 8):
            if (letters[x] in choice):
                pboardx = x
                break
        if (pboardx == ""):
            print("Invalid.")
            return full
        else:
            for x in range(0, 8):
                if (nums[x] in choice):
                    pboardy = x
                    break
            if (pboardy == ""):
                print("Invalid.")
                return full
        print(str(pboardy) + " " + str(pboardx))
        if (full[0][pboardy][pboardx] == full[0][pboardy][pboardx]):
            if (piece == "P"):
                if ("bl" in full[0][boardy][boardx]):
                    if (boardy + 2 == pboardy and pboardx == boardx and boardy == 1):
                        if (" " in full[0][pboardy][pboardx]):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[4] = pboardy - 1
                            full[5] = pboardx
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy + 1 == pboardy and pboardx == boardx):
                        if (" " in full[0][pboardy][pboardx]):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy + 1 == pboardy and boardx + 1 == pboardx):
                        if (pboardy == full[6] and pboardx == full[7]):
                            full[9].append(full[0][pboardy - 1][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[0][pboardy - 1][pboardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" not in full[0][pboardy][pboardx] and " " not in full[0][pboardy][pboardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy + 1 == pboardy and boardx - 1 == pboardx):
                        if (pboardy == full[6] and pboardx == full[7]):
                            full[9].append(full[0][pboardy - 1][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[0][pboardy - 1][pboardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" not in full[0][pboardy][pboardx] and " " not in full[0][pboardy][pboardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        print("Invalid.")
                        return full
                else:
                    if (boardy - 2 == pboardy and pboardx == boardx and boardy == 6):
                        if (" " in full[0][pboardy][pboardx]):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[6] = pboardy + 1
                            full[7] = pboardx
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy - 1 == pboardy and pboardx == boardx):
                        if (" " in full[0][pboardy][pboardx]):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy - 1 == pboardy and boardx + 1 == pboardx):
                        if (pboardy == full[6] and pboardx == full[7]):
                            full[8].append(full[0][pboardy + 1][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[0][pboardy + 1][pboardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx] and " " not in full[0][pboardy][pboardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    elif (boardy - 1 == pboardy and boardx - 1 == pboardx):
                        if (pboardy == full[6] and pboardx == full[7]):
                            full[8].append(full[0][pboardy + 1][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[0][pboardy + 1][pboardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx] and " " not in full[0][pboardy][pboardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        print("Invalid.")
                        return full
            elif (piece == "R"):
                if (pboardy != boardy and pboardx != boardx):
                    print("Invalid.")
                    return full
                elif (pboardy == boardy and pboardx == boardx):
                    print("Invalid.")
                    return full
                else:
                    if (pboardx != boardx):
                        if (pboardx < boardx):
                            for x in range(pboardx + 1, boardx):
                                if (full[0][boardy][x] != " "):
                                    print("Invalid.")
                                    return full
                        else:
                            for x in range(boardx + 1, pboardx):
                                if (full[0][boardy][x] != " "):
                                    print("Invalid.")
                                    return full
                    elif (pboardy != boardy):
                        if (boardy > pboardy):
                            for x in range(pboardy + 1, boardy):
                                if (full[0][boardx][x] != " "):
                                    print("Invalid.")
                                    return full
                        else:
                            for x in range(boardy + 1, pboardy):
                                if (full[0][boardx][x] != " "):
                                    print("Invalid.")
                                    return full
                    if (full[0][pboardy][pboardx] == " "):
                        if (boardx == 0):
                            if ("bl" in full[0][boardy][boardx]):
                                if (full[2] == 0):
                                    full[2] = 1
                                elif (full[2] == 2):
                                    full[2] = 3
                            elif ("bl" not in full[0][boardy][boardx]):
                                if (full[3] == 0):
                                    full[3] = 1
                                elif (full[3] == 2):
                                    full[3] = 3
                        elif (boardx == 7):
                            if ("bl" in full[0][boardy][boardx]):
                                if (full[2] == 0):
                                    full[2] = 2
                                elif (full[2] == 1):
                                    full[2] = 3
                            elif ("bl" not in full[0][boardy][boardx]):
                                if (full[3] == 0):
                                    full[3] = 2
                                elif (full[3] == 1):
                                    full[3] = 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    elif ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            if (boardx == 0):
                                if ("bl" in full[0][boardy][boardx]):
                                    if (full[2] == 0):
                                        full[2] = 1
                                    elif (full[2] == 2):
                                        full[2] = 3
                                elif ("bl" not in full[0][boardy][boardx]):
                                    if (full[3] == 0):
                                        full[3] = 1
                                    elif (full[3] == 2):
                                        full[3] = 3
                            elif (boardx == 7):
                                if ("bl" in full[0][boardy][boardx]):
                                    if (full[2] == 0):
                                        full[2] = 2
                                    elif (full[2] == 1):
                                        full[2] = 3
                                elif ("bl" not in full[0][boardy][boardx]):
                                    if (full[3] == 0):
                                        full[3] = 2
                                    elif (full[3] == 1):
                                        full[3] = 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            if (boardx == 0):
                                if ("bl" in full[0][boardy][boardx]):
                                    if (full[2] == 0):
                                        full[2] = 1
                                    elif (full[2] == 2):
                                        full[2] = 3
                                elif ("bl" not in full[0][boardy][boardx]):
                                    if (full[3] == 0):
                                        full[3] = 1
                                    elif (full[3] == 2):
                                        full[3] = 3
                            elif (boardx == 7):
                                if ("bl" in full[0][boardy][boardx]):
                                    if (full[2] == 0):
                                        full[2] = 2
                                    elif (full[2] == 1):
                                        full[2] = 3
                                elif ("bl" not in full[0][boardy][boardx]):
                                    if (full[3] == 0):
                                        full[3] = 2
                                    elif (full[3] == 1):
                                        full[3] = 3
                            return full
                        else:
                            print("Invalid.")
                            return full
            elif (piece == "N"):
                if (boardy + 2 == pboardy):
                    if (boardx + 1 == pboardx or boardx - 1 == pboardx):
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        if ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (boardy - 2 == pboardy):
                    if (boardx + 1 == pboardx or boardx - 1 == pboardx):
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        if ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (boardx + 2 == pboardx):
                    if (boardy + 1 == pboardy or boardy - 1 == pboardy):
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        if ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (boardx - 2 == pboardx):
                    if (boardy + 1 == pboardy or boardy - 1 == pboardy):
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        if ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                else:
                    print("Invalid.")
                    return full
            elif (piece == "B"):
                if (pboardy > boardy and pboardx > boardx):
                    if (pboardy - boardy == pboardx - boardx):
                        for x in range(1, pboardy - boardy):
                            if (full[0][boardy + x][boardx + x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy < boardy and pboardx < boardx):
                    if (boardy - pboardy == boardx - pboardx):
                        for x in range(1, boardy - pboardy):
                            if (full[0][boardy - x][boardx - x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy > boardy and pboardx < boardx):
                    if (pboardy - boardy == boardx - pboardx):
                        for x in range(1, pboardy - boardy):
                            if (full[0][boardy + x][boardx - x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy < boardy and pboardx > boardx):
                    if (boardy - pboardy == pboardx - boardx):
                        for x in range(1, boardy - pboardy):
                            if (full[0][boardy - x][boardx + x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                else:
                    print("Invalid.")
                    return full
            elif (piece == "Q"):
                if (pboardy > boardy and pboardx > boardx):
                    if (pboardy - boardy == pboardx - boardx):
                        for x in range(1, pboardy - boardy):
                            if (full[0][boardy + x][boardx + x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy < boardy and pboardx < boardx):
                    if (boardy - pboardy == boardx - pboardx):
                        for x in range(1, boardy - pboardy):
                            if (full[0][boardy - x][boardx - x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy > boardy and pboardx < boardx):
                    if (pboardy - boardy == boardx - pboardx):
                        for x in range(1, pboardy - boardy):
                            if (full[0][boardy + x][boardx - x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                elif (pboardy < boardy and pboardx > boardx):
                    if (boardy - pboardy == pboardx - boardx):
                        for x in range(1, boardy - pboardy):
                            if (full[0][boardy - x][boardx + x] != " "):
                                print("Invalid.")
                                return full
                        if (full[0][pboardy][pboardx] == " "):
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        elif ("bl" in full[0][pboardy][pboardx]):
                            if ("bl" not in full[0][boardy][boardx]):
                                full[8].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                        else:
                            if ("bl" in full[0][boardy][boardx]):
                                full[9].append(full[0][pboardy][pboardx])
                                full[0][pboardy][pboardx] = full[0][boardy][boardx]
                                full[0][boardy][boardx] = " "
                                full[1] = full[1] + 1
                                return full
                            else:
                                print("Invalid.")
                                return full
                    else:
                        print("Invalid.")
                        return full
                else:
                    if (pboardx != boardx):
                        if (pboardx < boardx):
                            for x in range(pboardx + 1, boardx):
                                if (full[0][boardy][x] != " "):
                                    print("Invalid.")
                                    return full
                        else:
                            for x in range(boardx + 1, pboardx):
                                if (full[0][boardy][x] != " "):
                                    print("Invalid.")
                                    return full
                    elif (pboardy != boardy):
                        if (boardy > pboardy):
                            for x in range(pboardy + 1, boardy):
                                if (full[0][boardx][x] != " "):
                                    print("Invalid.")
                                    return full
                        else:
                            for x in range(boardy + 1, pboardy):
                                if (full[0][boardx][x] != " "):
                                    print("Invalid.")
                                    return full
                    if (full[0][pboardy][pboardx] == " "):
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    elif ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            return full
                        else:
                            print("Invalid.")
                            return full
                print("Invalid.")
                return full
            elif (piece == "K"):
                if (pboardy + 1 == boardy and pboardx == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy + 1 == boardy and pboardx + 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy + 1 == boardy and pboardx - 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy - 1 == boardy and pboardx == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy - 1 == boardy and pboardx + 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy - 1 == boardy and pboardx - 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy == boardy and pboardx + 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (pboardy == boardy and pboardx - 1 == boardx):
                    if (full[0][pboardy][pboardx] == " "):
                        if ("bl" in full[0][boardy][boardx]):
                            full[2] == 3
                        else:
                            full[3] == 3
                        full[0][pboardy][pboardx] = full[0][boardy][boardx]
                        full[0][boardy][boardx] = " "
                        full[1] = full[1] + 1
                        return full
                    if ("bl" in full[0][pboardy][pboardx]):
                        if ("bl" not in full[0][boardy][boardx]):
                            full[8].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[3] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                    else:
                        if ("bl" in full[0][boardy][boardx]):
                            full[9].append(full[0][pboardy][pboardx])
                            full[0][pboardy][pboardx] = full[0][boardy][boardx]
                            full[0][boardy][boardx] = " "
                            full[1] = full[1] + 1
                            full[2] == 3
                            return full
                        else:
                            print("Invalid.")
                            return full
                elif (boardy == 7 and boardx == 4 and full[0][boardy][boardx] == "K" and pboardy == 7 and full[
                    3] != 3 and check_check(full, "K") != "check"):
                    if (pboardx == 2 and full[3] != 1):
                        if (full[0][7][0] == "R" and full[0][7][1] == " " and full[0][7][2] == " " and full[0][7][
                            3] == " "):
                            full[0][7][0] = " "
                            full[0][7][2] = "K"
                            full[0][7][3] = "R"
                            full[0][7][4] = " "
                    elif (pboardx == 6 and full[3] != 2):
                        if (full[0][7][7] == "R" and full[0][7][6] == " " and full[0][7][5] == " "):
                            full[0][7][4] = " "
                            full[0][7][5] = "R"
                            full[0][7][6] = "K"
                            full[0][7][7] = " "
                    else:
                        print("Invalid.")
                        return full
                elif (boardy == 0 and boardx == 4 and full[0][boardy][boardx] == "Kbl" and pboardy == 0 and full[
                    2] != 3 and check_check(full, "Kbl") != "check"):
                    if (pboardx == 2 and full[2] != 1):
                        if (full[0][0][0] == "Rbl" and full[0][0][1] == " " and full[0][0][2] == " " and full[0][0][
                            3] == " "):
                            full[0][0][0] = " "
                            full[0][0][2] = "Kbl"
                            full[0][0][3] = "Rbl"
                            full[0][0][4] = " "
                    elif (pboardx == 6 and full[2] != 2):
                        if (full[0][0][7] == "Rbl" and full[0][0][6] == " " and full[0][0][5] == " "):
                            full[0][0][4] = " "
                            full[0][0][5] = "Rbl"
                            full[0][0][6] = "Kbl"
                            full[0][0][7] = " "
                    else:
                        print("Invalid.")
                        return full
                else:
                    print("Invalid.")
                    return full
        return full


    while win == 0:
        os.system('clear')
        board_print(full)
        full = move(full)
        for i in range(0, 8):
            if (full[0][0][i] == "P"):
                done = 0
                while done == 0:
                    os.system('clear')
                    board_print(full)
                    choice = input("\033[0mWhat piece would you like to promote your pawn into?\n").lower()
                    if ("rook" in choice or "r" in choice):
                        full[0][0][i] = "R"
                        done = 1
                        full[11].append("R")
                        break
                    elif ("knight" in choice or "kn" in choice):
                        full[0][0][i] = "N"
                        done = 1
                        full[11].append("N")
                        break
                    elif ("bishop" in choice or "b" in choice):
                        full[0][0][i] = "B"
                        done = 1
                        full[11].append("B")
                        break
                    elif ("queen" in choice or "q" in choice):
                        full[0][0][i] = "Q"
                        done = 1
                        full[11].append("Q")
                        break
        for i in range(0, 8):
            if (full[0][7][i] == "Pbl"):
                done = 0
                while done == 0:
                    os.system('clear')
                    board_print(full)
                    choice = input("\033[0mWhat piece would you like to promote your pawn into?\n").lower()
                    if ("rook" in choice or "r" in choice):
                        full[0][7][i] = "Rbl"
                        done = 1
                        full[10].append("Rbl")
                        break
                    elif ("knight" in choice or "kn" in choice):
                        full[0][7][i] = "Nbl"
                        done = 1
                        full[10].append("Nbl")
                        break
                    elif ("bishop" in choice or "b" in choice):
                        full[0][7][i] = "Bbl"
                        done = 1
                        full[10].append("Bbl")
                        break
                    elif ("queen" in choice or "q" in choice):
                        full[0][7][i] = "Qbl"
                        done = 1
                        full[10].append("Qbl")
                        break
        wk = 0
        bk = 0
        for y in range(0, 8):
            for x in range(0, 8):
                if ("K" in full[0][y][x]):
                    if ("bl" in full[0][y][x]):
                        bk = 1
                    else:
                        wk = 1
        if (wk == 1 and bk == 0):
            win = 1
        elif (wk == 0 and bk == 1):
            win = 1
if (wk == 1):
    os.system('clear')
    board_print(full)
    print("\033[0;1mWhite Wins!")
    print("\033[0;1mCheckmate in " + str(int((full[1] + 1) / 2)) + "\033[0;1m.")
else:
    os.system('clear')
    board_print(full)
    print("\033[0;34;1mBlack Wins!")
    print("\033[0;1mCheckmate in " + str(int((full[1]) / 2)) + "\033[0;1m.")
