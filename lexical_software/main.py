import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from lexical_analyzer import LexicalAnalyzer

class LexicalAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Lexical Analyzer")
        master.resizable(False, False)  # Make the window not resizable

        # Top Frame for scrolled text areas
        top_frame = tk.Frame(master)
        top_frame.pack(side=tk.TOP)

        # Scrolled Text Area 1
        self.text_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, width=80, height=25)
        self.text_area.grid(row=0, column=0, padx=10, pady=20)

        # Scrolled Text Area 2
        self.output_area = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, width=70, height=25)
        self.output_area.grid(row=0, column=1, padx=10, pady=20)

        # Analyze Button
        self.analyze_button = tk.Button(top_frame, text="Analyze", command=self.analyze_code, width=30, height=3, bg='blue')
        self.analyze_button.grid(row=1, column=0,  )

        # Clear Button
        self.clear_button = tk.Button(top_frame, text="Clear", command=self.clear_text, width=30, height=3, bg='red')
        self.clear_button.grid(row=1, column=1, padx=10, pady=10)

        # Download Button
        self.download_button = tk.Button(top_frame, text="Download", command=self.download_output, width=30, height=3, bg='green')
        self.download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        
    def analyze_code(self):
        input_program = self.text_area.get("1.0", tk.END)

        if not input_program.strip():
            messagebox.showerror("Error", "Please enter code for analysis.")
            return

        lexer = LexicalAnalyzer()
        tokens = lexer.tokenize_and_categorize(input_program)

        # Clear the output area before displaying new tokens
        self.output_area.delete("1.0", tk.END)

        for lexeme, token in tokens:
            formatted_lexeme = f"{lexeme:<20}"
            formatted_token = f"{token:^15}"
            self.output_area.insert(tk.END, f"{formatted_lexeme}{formatted_token}\n")

    def clear_text(self):
        # Clear both the input and output text areas
        self.text_area.delete("1.0", tk.END)
        self.output_area.delete("1.0", tk.END)

    def download_output(self):
        output_content = self.output_area.get("1.0", tk.END)

        if not output_content.strip():
            messagebox.showerror("Error", "There is no output to download.")
            return

        try:
            with open("output.txt", "w") as output_file:
                output_file.write(output_content)
            messagebox.showinfo("Success", "Output saved to 'output.txt'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save output: {e}")

def main():
    root = tk.Tk()
    root.geometry("1280x720")
    app = LexicalAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
