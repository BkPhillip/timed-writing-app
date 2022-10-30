from tkinter import *
from tkinter import filedialog as fd
from math import floor

FONT = ("Purisa", 18)

HIGHLIGHT_COLORS = ["#980000", "#ff0000", "#ff9900", "#ffff00", "#00ff00"]


class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("900x900")
        self.window.resizable(False, False)
        self.window.title("Timed Text Writing App")
        self.timer = None
        self.started_typing = False
        self.total_sec = 300
        self.short_sec = 5
        self.word_count = 0
        # ------ Timer
        self.timer_label = Label(text="Time: 05:00", font=FONT)
        self.timer_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.short_timer_label = Label(text="5", font=FONT)
        self.short_timer_label.place(relx=0.8, rely=0.05, anchor=CENTER)
        # ------ Text Field
        self.text_field = Text(height=28,
                               font=("Purisa", 22),
                               wrap=WORD,
                               width=60,
                               highlightthickness=1,
                               highlightcolor=HIGHLIGHT_COLORS[4])
        self.text_field.place(relx=0.5, rely=0.5, anchor=CENTER)
        # ------ Word Count
        self.word_count_label = Label(text=f"Word Count: {self.word_count}", font=FONT)
        self.word_count_label.place(relx=0.5, rely=0.95, anchor=CENTER)
        # ------
        self.window.bind('<Key>', self.key_press)
        self.window.mainloop()

    def key_press(self, event):
        self.short_sec = 5
        if event.char == event.keysym and not self.started_typing:
            self.count_down(self.total_sec)
            self.started_typing = True
        self.update_word_count()

    def update_word_count(self):
        inp = self.text_field.get(1.0, END)
        self.word_count = len(inp.split())
        self.word_count_label.configure(text=f"Word Count: {self.word_count}")

    def end_session_popup(self):
        self.window.withdraw()
        top = Toplevel(self.window)
        top.geometry("900x200")
        top.title("Results")
        results_label = Label(top, text=f"You typed {self.word_count} words in {300 - self.total_sec} seconds!")
        results_label.place(relx=0.5, rely=0.3, anchor=CENTER)
        export_button = Button(top, text="Export", command=self.export_text)
        export_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        reset_button = Button(top, text="Reset", command=lambda: [self.reset_app(), top.destroy()])
        reset_button.place(relx=0.5, rely=0.7, anchor=CENTER)

    def reset_app(self):
        self.window.deiconify()
        self.text_field.delete(1.0, END)  # Delete previous text
        self.text_field.configure(highlightthickness=1, highlightcolor=HIGHLIGHT_COLORS[4])  # Reset border
        # ------ Reset values to default
        self.started_typing = False
        self.total_sec = 300
        self.short_sec = 5
        self.word_count = 0
        # ------ Reset timer labels
        self.timer_label.configure(text=f"Time: 05:00")
        self.short_timer_label.configure(text=f"{self.short_sec}")

    def export_text(self):
        filename = fd.asksaveasfile(mode="w", defaultextension=".txt")
        if filename is None:  # if no name is given for file then exit
            return
        text2save = str(self.text_field.get(1.0, END))
        filename.write(text2save)
        filename.close()

    def count_down(self, count):
        self.timer = self.window.after(1000, self.count_down, count - 1)
        # ------ Get time as minutes and seconds
        timer_sec = count % 60
        timer_min = floor(count / 60)
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"  # Add 0 in front of single digit seconds
        if timer_min < 10:
            timer_min = f"0{timer_min}"  # Add 0 in front of single digit minutes
        # ------ Update Labels
        self.timer_label.configure(text=f"Time: {timer_min}:{timer_sec}")
        self.short_timer_label.configure(text=f"{self.short_sec}")
        highlight_thickness = 2 * (6 - self.short_sec)
        highlight_color = HIGHLIGHT_COLORS[self.short_sec - 1]
        self.text_field.configure(highlightthickness=highlight_thickness, highlightcolor=highlight_color)  # Border thickens to show time running out
        # ------ Check if either timer has reached zero
        if self.short_sec == 0 or self.total_sec == 0:
            self.window.after_cancel(self.timer)
            self.end_session_popup()
        # ----- Increment time
        self.total_sec -= 1
        self.short_sec -= 1


app = App()
