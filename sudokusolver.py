import tkinter as tk

def create_entries():
    entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(frame, font=("Arial", 12), justify='center', width=4, bg="red")
            entry.grid(row=i, column=j, padx=5, pady=5, ipady=8)
            row_entries.append(entry)
        entries.append(row_entries)
    return entries

def get_user_input(entries):
    user_input = []
    for row_entries in entries:
        row_values = []
        for entry in row_entries:
            value = entry.get()
            row_values.append(value)
        user_input.append(row_values)
    return user_input

def is_valid(board, row, col, num):
    # Check the row and column
    for i in range(9):
        if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
            return False

    # Check the 3x3 region
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num and (i, j) != (row, col):
                return False

    return True

def find_empty_position(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == "":
                return i, j
    return None

def solve_sudoku(board):
    empty = find_empty_position(board)
    if not empty:
        return True
    row, col = empty

    for num in range(1, 10):
        num = str(num)
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = ""

    return False

def get_3x3_region(board, start_row, start_col):
    region = []
    for i in range(start_row, start_row + 3):
        row = []
        for j in range(start_col, start_col + 3):
            row.append(board[i][j])
        region.append(row)
    return region

def hint():
    user_input = get_user_input(entries)

    # Satır ve sütun kontrolü
    for i in range(9):
        for j in range(9):
            num = user_input[i][j]
            if num and not is_valid(user_input, i, j, num):
                print("Sudoku cannot be solved. Duplicate number found in the same row, column, or 3x3 region.")
                return

    # 3x3 bölge kontrolü
    for i in range(0, 9, 3):
      for j in range(0, 9, 3):
        region_values = set(user_input[i + k][j + l] for k in range(3) for l in range(3) if user_input[i + k][j + l])
        if len(region_values) != len(set(region_values)):  # Corrected condition
            print("Sudoku cannot be solved. Duplicate number found in the same row, column, or 3x3 region.")
            return

    # Kontrol etmek istediğiniz bölgeleri seçin (örneğin, bir satır, bir sütun, veya bir 3x3 alan)
    regions_to_check = [user_input, list(map(list, zip(*user_input)))]

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            region_to_check = get_3x3_region(user_input, i, j)
            regions_to_check.append(region_to_check)

    for region in regions_to_check:
        for i in range(9):
            count = sum(1 for num in map(str, range(1, 10)) if str(num) not in region[i])
            if count == 1:
                missing_number = next(num for num in map(str, range(1, 10)) if str(num) not in region[i])
                print(f"Hint: Try {missing_number} in the region.")
                return

    print("No hint available. Check your input.")

def submit():
    user_input = get_user_input(entries)
    sudoku_board = [[str(user_input[i][j]) if user_input[i][j] else "" for j in range(9)] for i in range(9)]
    if solve_sudoku(sudoku_board):
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(0, sudoku_board[i][j])

def clear():
    for row_entries in entries:
        for entry in row_entries:
            entry.delete(0, "end")

form = tk.Tk()
form.title("Sudoku Solver")
form.geometry("700x600")
form.resizable(False, False)
etiket = tk.Label(form, text="Welcome The League Of Sudoku ", bg="white", fg="#1c0f45", font="Monaco 20").place(relx=0.18, rely=0.001)
form.config(bg="white")
frame = tk.Frame(form, bg="black")
frame.pack(padx=35, pady=50)

entries = create_entries()

yatay1 = tk.Label(form, bg="yellow", fg="yellow", text="t")
yatay1.place(relx=0.18, rely=0.32, width=447, height=4)

yatay2 = tk.Label(form, bg="yellow", fg="yellow", text="t")
yatay2.place(relx=0.18, rely=0.56, width=447, height=4)

dikey1 = tk.Label(form, bg="yellow", fg="yellow", text="t")
dikey1.place(relx=0.39, rely=0.083, width=4, height=430)

dikey2 = tk.Label(form, bg="yellow", fg="yellow", text="t")
dikey2.place(relx=0.604, rely=0.083, width=4, height=430)

submit_button1 = tk.Button(form, text="Submit", command=submit, bg="gray", activebackground="blue")
submit_button1.place(height=20, width=50, x=220, y=520)

hint_button2 = tk.Button(form, text="Hint", command=hint, bg="gray", activebackground="blue")
hint_button2.place(height=20, width=50, x=320, y=520)

clear_button3 = tk.Button(form, text="Clear", command=clear, bg="gray", activebackground="blue")
clear_button3.place(height=20, width=50, x=420, y=520)

form.mainloop()