import tkinter as tk
from tkinter import messagebox
from lexical_analyzer import LexicalAnalyzer
from tkinter import messagebox, Canvas, Text, Button, PhotoImage, Scrollbar

def relative_to_assets(file_path):
    base_path = r"C:\Users\Josh\Documents\VSCODE python\LEXICAL\Lexical Software"
    absolute_path = base_path + "\\" + file_path
    return absolute_path

def analyze_code():
    input_program = entry_1.get("1.0", tk.END)

    if not input_program.strip():
        messagebox.showerror("Error", "Enter a Code!")
        return

    lexer = LexicalAnalyzer()
    tokens = lexer.tokenize_and_categorize(input_program)

    entry_2.delete("1.0", tk.END)

    # Add headers
    header = f"{'Lexeme':<20}{'Token':^15}\n"
    entry_2.insert(tk.END, header)

    for lexeme, token in tokens:
        formatted_lexeme = f"{lexeme:<20}"
        formatted_token = f"{token:^15}"
        entry_2.insert(tk.END, f"{formatted_lexeme}{formatted_token}\n")

def clear_text():
    entry_1.delete("1.0", tk.END)
    entry_2.delete("1.0", tk.END)

def download_output():
    output_content = entry_2.get("1.0", tk.END)

    if not output_content.strip():
        messagebox.showerror("Error", "There is no output to download!")
        return

    try:
        with open("tokens.txt", "w") as output_file:
            output_file.write(output_content)
        messagebox.showinfo("Success", "Output saved to 'tokens.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save output: {e}")
        
window = tk.Tk()

window.geometry("1280x720")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    720.0,
    fill="#534C4C",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    396.0,
    355.5,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#E6E6E6",
    fg="#000716",
    highlightthickness=0,
    font=("Consolas", 14)
)
entry_1.place(
    x=82.0,
    y=126.0,
    width=618.0,
    height=457.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    997.5,
    398.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#E6E6E6",
    fg="#000716",
    highlightthickness=0,
    font=("Consolas", 14)
)
entry_2.place(
    x=789.0,
    y=126.0,
    width=417.0,
    height=542.0
)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    388.0,
    61.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    997.0,
    65.0,
    image=image_image_2
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=3,
    highlightthickness=3,
    command=analyze_code,
    relief="raised"
)
button_1.place(
    x=66.967529296875,
    y=598.0,
    width=200.06944274902344,
    height=74.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=3,
    highlightthickness=3,
    command=clear_text,
    relief="raised"
)
button_2.place(
    x=296.0,
    y=598.0,
    width=201.0,
    height=72.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=3,
    highlightthickness=3,
    command=download_output,
    relief="raised",
   
)
button_3.place(
    x=525.0,
    y=598.0,
    width=201.0,
    height=72.0
)

# Add vertical scrollbar to entry_1
scrollbar_1 = Scrollbar(window, command=entry_1.yview)
scrollbar_1.place(x=708, y=136, height=425)
entry_1.config(yscrollcommand=scrollbar_1.set)

# Add both vertical and horizontal scrollbars to entry_2
scrollbar_2_y = Scrollbar(window, command=entry_2.yview)
scrollbar_2_x = Scrollbar(window, command=entry_2.xview, orient=tk.HORIZONTAL)
scrollbar_2_y.place(x=1205, y=146, height=500)
entry_2.config(yscrollcommand=scrollbar_2_y.set)


window.resizable(False, False)
window.title("ReCipe: Lexical Analyzer Software")
window.mainloop()
