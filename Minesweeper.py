import winsound
import random
import time

def chooseDifficulty(): # Allow user to choose the default difficulty or the custom difficulty with customizable mines and gameboard
    try:
        difficulty = input("Difficulty: ( D - Default | E - Easy | N - Normal | H - Hard | C - Custom )? ").upper()
        print()

        if (difficulty == "D"): # 10 mines and 9 * 9 matrix for the default setting
            req_mine = 10
            req_row = 9
            req_col = 9
        elif (difficulty == "E"): # Easy preset
            req_mine = 3
            req_row = 5
            req_col = 5
        elif (difficulty == "N"): # Normal preset
            req_mine = 13
            req_row = 9
            req_col = 9
        elif (difficulty == "H"): # Hard preset
            req_mine = 20
            req_row = 9
            req_col = 9
        elif (difficulty == "C"): # Customizable
            req_mine = int(input("Number of mines? "))
            req_row = int(input("Number of rows? "))
            req_col = int(input("Number of columns? "))
            if (req_row * req_col <= req_mine): # Avoid mines >= available cells
                print("\n[ERROR] Mines are more than or equal to cells available in the gameboard. Please make sure mines are less than cells available.\n")
                return chooseDifficulty()
        else: # Incorrect input will ask user to choose again
            print("\n[ERROR] Invalid input. Please try again\n")
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return chooseDifficulty()
        return req_mine, req_row, req_col
    except:
        print("\n[ERROR] Invalid input. Please try again\n")
        winsound.PlaySound("*", winsound.SND_ALIAS)
        return chooseDifficulty()



def mine_sweeper_ans(bombs): # Used to generate the answer layout of the game
    ans_board = [[0 for i in range(total_cols)] for j in range(total_rows)] # create the answer gameboard

    for bomb_location in bombs:
        (bomb_row, bomb_col) = bomb_location
        ans_board[bomb_row][bomb_col] = "M" # "M" represent bomb
        check_row = range(bomb_row - 1, bomb_row + 2) #the row range of the imaginary martrix of 3 x 3 around the bomb
        check_col = range(bomb_col - 1, bomb_col + 2) #the col range of the imaginary martrix of 3 x 3 around the bomb

        for i in check_row:
            for j in check_col: # for each mines, check columns first => then return to rows
                if (0 <= i < total_rows and 0 <= j < total_cols and ans_board[i][j] != "M"):
                    ans_board[i][j] += 1
    return ans_board


def mine_randomizer(): # Generate a seed for mine
    num_mine = 0
    lst_tempBomb = []
    while num_mine < total_mines: #Keep looping until number of valid mines is enough
        bomb_row = random.randint(0, total_rows - 1)
        bomb_col = random.randint(0, total_cols - 1)
        temp_bomb = [bomb_row, bomb_col]

        lst_tempBomb.append(temp_bomb)
        set_bomb = set(tuple(x) for x in lst_tempBomb) # Avoid duplicated mines
        bomb_cord = [list(x) for x in set_bomb]
        num_mine = len(bomb_cord)
    return bomb_cord


def create_board(): # Used to create the board that user can interact with
    unk_board = [["□" for i in range(total_cols)] for j in range(total_rows)]
    return unk_board


def display_board(board): # For displaying the gameboard interface
    print("\nMines in the game: " + str(total_mines)) # Mines counter
    print("\nCurrent board:\n")
    if (total_cols <= 9 and total_rows <= 9):
        row_ref = iter(range(1, total_rows + 1))
        col_ref = list(map(str,range(1, total_cols + 1)))
        print("   " + " ".join(col_ref))
        for i in board:
            print(next(row_ref), end = "  ")
            print(" ".join(map(str, i)))
    else:
        for i in board:
            print(" ".join(map(str, i)))


def display_ans(): # For displaying the answer
    print("Layout:")
    if (total_rows <= 9 and total_cols <= 9):
        row_ref = iter(range(1, total_rows + 1))
        col_ref = list(map(str,range(1, total_cols + 1)))
        print("   " + " ".join(col_ref))
        for i in ans:
            print(next(row_ref), end = "  ")
            print(" ".join(map(str, i)))
    else:
        for i in ans:
            print(" ".join(map(str, i)))


def retry(): # For retry
    print()
    try:
        input_retry = input("Retry? [Y / N]").upper()
        if (input_retry == "Y"):
            main()
        elif (input_retry == "N"):
            print("OK")
            return
        else:
            print("Please enter Y or N to indicate if you would like to play again.")
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return retry()
    except:
        print("Invalid Input. Try again")
        retry()



def checkNeighbor(board, input_row, input_col): # Check neighbor new zeros
    lst_check_later = [] # For checking new zeros
    neighbor_s = 0
    
    original_zero = (input_row, input_col)
    lst_check_later.append(original_zero)

    for newZero_location in lst_check_later:
        (input_row, input_col) = newZero_location
        check_row = range(input_row - 1, input_row + 2) #the row range of the imaginary martrix of 3 x 3 around the empty uncovered cell
        check_col = range(input_col - 1, input_col + 2) #the col range of the imaginary martrix of 3 x 3 around the empty uncovered cell

        for i in check_row:
            for j in check_col:
                if (0 <= i < total_rows and 0 <= j < total_cols and board[i][j] == "□"): # Check for 3 * 3 grid around the original zero and collect the covered new zero.
                    if (ans[i][j] == 0):
                        new_zero = [i, j]
                        lst_check_later.append(new_zero) # Adding the new zero checked to the list
                        board[i][j] = " "
                    else:
                        board[i][j] = ans[i][j]
                    neighbor_s += 1
    return neighbor_s


def timer(end_time): # For counting the time of the game
    hour_u = 0
    min_u = 0
    sec_u = 0
    time_used = int(round(end_time - start_time)) # In seconds

    while time_used >= 3600: # 1 hour = 60 mins = 60 * 60 = 3600 sec
        hour_u += 1
        time_used -= 3600
    else:
        while time_used >= 60: # 1 min = 60 sec
            min_u += 1
            time_used -= 60
        else:
            sec_u += time_used # remaining sec    
    return hour_u, min_u, sec_u


def uncover_mode(board, score, step, input_row, input_col): # Uncover Mode
    win_score = total_cols * total_rows - total_mines # For winning condition   

        
    if (0 <= input_row < total_rows and 0 <= input_col < total_cols): # Within the board
        if (board[input_row][input_col] == "F"): # Flagged
            print("[ERROR] Unable to uncover flagged cell.")
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return select_cell(board, score, step)
        elif (ans[input_row][input_col] == "M"): # Hit Mine
            print("BOMB. Game Over")
            print("Your score:",score)
            display_ans()
            print()
            lost()
            return retry() # Asks user to retry after lose the game
        elif (board[input_row][input_col] != "□"): # Already uncovered
            print("Try to uncover: Row: " + str(input_row+1) + ", Column: " + str(input_col+1))
            print("Cell already uncover.")
            return select_cell(board, score, step)
        else: # Uncovers a covered cell
            print("Uncovered: Row: " + str(input_row+1) + ", Column: " + str(input_col+1))
            score += 1
            step += 1
            if (ans[input_row][input_col] == 0):
                board[input_row][input_col] = " "
                neighbor_s = checkNeighbor(board, input_row, input_col)
                score += neighbor_s # Add back the neighbor score
            else:
                board[input_row][input_col] = ans[input_row][input_col] # Reveal cell number

            if (score == win_score):
                print("\nYou won!\nScore:", score)
                print("Step used:", step)
                display_ans()
                print()
                win()
                end_time = time.time()
                time_used = timer(end_time)
                hour = time_used[0]
                minute = time_used[1]
                sec = time_used[2]

                print("Time used:", hour, "hours", minute, "minutes", sec, "seconds")
                record(step, score, hour, minute, sec)
                return retry() # Ask user to retry when they finish the current game
            else:
                return select_cell(board, score, step)
    else:
        print("\n[ERROR] Input outside the range of the game board. Returning to main mode") # User enters out of range number
        winsound.PlaySound("*", winsound.SND_ALIAS)
        return select_cell(board, score, step)


def flag_mode(board, score, step): # Flag Mode
    try:
        input_row = int(input("Row? ")) - 1 # Minus 1 to look better
        input_col = int(input("Col? ")) - 1 # Minus 1 to look better

        if (0 <= input_row < total_rows and 0 <= input_col < total_cols):
            if (board[input_row][input_col] == "□"): # Flag cell from covered cell
                board[input_row][input_col] = "F"
                step += 1
                print("Flagged cord: ["+str(input_row)+", "+str(input_col)+"]")
                return select_cell(board, score, step)
            elif (board[input_row][input_col] == "F"): # Unflag a flagged cell
                board[input_row][input_col] = "□"
                step += 1
                print("Unflagged cord: ["+str(input_row)+", "+str(input_col)+"]")
                return select_cell(board, score, step)
            else:
                print("Unable to flag an opened cell")
                winsound.PlaySound("*", winsound.SND_ALIAS)
                return select_cell(board, score, step)
        else:
            print("\n[ERROR] Input outside the range of the game board. Returning to main mode") # User enters out of range number
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return select_cell(board, score, step)
    except:
        print("\n[ERROR] Input can ONLY be integer. Returning to main mode") # User enters non integer number
        winsound.PlaySound("*", winsound.SND_ALIAS)
        return select_cell(board, score, step)


def debug_mode(): # Debug Mode
    print("[Debug Mode]: ON" + "\n")
    print("Number of mines:", total_mines)
    print("Rows:", total_rows)
    print("Columns:", total_cols)
    display_ans()
    return

def select_cell(board, score, step): # Main user actions        
    display_board(board)
    print()
    try:
        input_act = input("Action (U - Uncover | F - Flag | R - Retry | E - Exit | AI - Uncovered by AI)? ").upper()
        print("Step: ",step)
        
        if (input_act == "U"):  # Uncover cell mode
            try:
                input_row = int(input("Row? (1 - " + str(total_rows) + ") ")) - 1 # Minus 1 to look better
                input_col = int(input("Col? (1 - " + str(total_cols) + ") ")) - 1 # Minus 1 to look better
            except:
                print("\n[ERROR] Please enter integer only for the row and column number. Returning to main mode") # User enters non integer number
                winsound.PlaySound("*", winsound.SND_ALIAS)
                return select_cell(board, score, step)
            
            return uncover_mode(board, score, step, input_row, input_col)
        elif (input_act == "F"): # Flag cell mode
            return flag_mode(board, score, step)
        elif (input_act == "AI"):
            input_row = int(random.randint(0,total_rows-1))
            input_col = int(random.randint(0,total_cols-1))
            return uncover_mode(board, score, step, input_row, input_col)
        elif (input_act == "R"): # Retry during mid-game
            return retry()
        elif (input_act == "E"): # Exit the game
            return
        elif (input_act == "D"): # Debug
            debug_mode()
            return select_cell(board, score, step)

        else:
            print("[ERROR] Input outside selection range. Please try again")
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return select_cell(board, score, step)
    except:
        print("[ERROR] Invalid input. Please try again")
        return select_cell(board, score, step)
    
def record(step, score, hour, minute, sec): # User can choose to write a record if he/she wins
    try:
        will = input("\nCongrats. Do you want to record your record of the game? [Y / N]").upper()
        if (will == "Y"):
            name = input("\nName? ")
            # i.e. Name: Alex | Scores: 8 | Steps: 1 | Hours: 0 | Minutes: 0 | Seconds: 10
            new_record = str("Name: " + name + " | Scores: " + str(score) + " | Steps: " + str(step) + " | Hours: " + str(hour) + " | Minutes: " + str(minute) + " | Seconds: " + str(sec) + "\n\n")

            recordFile = open("Minesweeper_record.txt", "a")
            recordFile.write(new_record)
            recordFile.close()
            return
        elif (will == "N"):
            return
        else:
            print("Instruction unclear. Please state your will. [Y / N]")
            winsound.PlaySound("*", winsound.SND_ALIAS)
            return record(step, score, hour, minute, sec)
    except:
        print("Invalid input. Please state your will. [Y / N]")
        winsound.PlaySound("*", winsound.SND_ALIAS)
        return record(step, score, hour, minute, sec)

def win():
    print('YOU WIN\n\n\n')
    print(' 0 0 0 0 0')
    print('0 /\   /\ 0')
    print('0    .    0')
    print('0  \___/  0')
    print(' 0 0 0 0 0 ')
    winsound.Beep(400,500)
    winsound.Beep(200,500)
    winsound.Beep(500,500)
    winsound.Beep(100,500)
    winsound.Beep(300,500)
    

def lost():
    print('YOU LOSE\n\n\n')
    print(' 0 0 0 0 0')
    print('0  /   \  0')
    print('0    .    0')
    print('0  _____  0')
    print(' 0 0 0 0 0 ')
    winsound.Beep(50,500)
    winsound.Beep(70,500)
    winsound.Beep(90,500)
    winsound.Beep(110,500)
    winsound.Beep(130,500)

def main(): # Main to initiate
    # Global variables
    global total_mines
    global total_rows
    global total_cols
    global ans
    global start_time
    global score
    global step


    print("Welcome to Minesweeper!\n")
    print("Suggestion: Put on your earphone and open your volume.\n")

    start_time = time.time() # Mark the start time for later use

    score = 0 # Score system
    step = 0 # Count user steps

    difficulty = chooseDifficulty()
    total_mines = difficulty[0]
    total_rows = difficulty[1]
    total_cols = difficulty[2]

    seed = mine_randomizer() # Seed for mine
    ans = mine_sweeper_ans(seed)
    board = create_board()# Print empty board

    select_cell(board, score, step)
    
    return

main()
input("Press enter to end the program")
