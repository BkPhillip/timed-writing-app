from tkinter import *
from tkinter import filedialog as fd
from math import floor

FONT = ("Purisa", 18)
HIGHLIGHT_COLORS = ["#980000", "#ff0000", "#ff9900", "#ffff00", "#00ff00"]
TOTAL_TIME_DEFAULT = 300
INTERVAL_TIME_DEFAULT = 5

class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("900x900")
        self.window.resizable(False, False)
        self.window.title("Timed Text Writing App")
        self.timer = None
        self.started_typing = False
        self.total_sec = TOTAL_TIME_DEFAULT
        self.interval_sec = INTERVAL_TIME_DEFAULT
        self.total_sec_custom = None
        self.interval_sec_custom = None
        self.word_count = 0
        # ------ Timer
        self.total_timer_label = Label(text="Time: 00:00", font=FONT)
        self.total_timer_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.set_clock(TOTAL_TIME_DEFAULT)
        self.interval_timer_label = Label(text="5", font=FONT)
        self.interval_timer_label.place(relx=0.8, rely=0.05, anchor=CENTER)
        self.settings_button = Button(text="Settings", command=self.settings_window)
        self.settings_button.place(relx=0.2, rely=0.05, anchor=CENTER)
        # ------ Text Field
        self.text_field = Text(height=28,
                               font=("Purisa", 22),
                               wrap=WORD,
                               width=60,
                               highlightthickness=11,
                               highlightcolor=HIGHLIGHT_COLORS[4])
        self.text_field.place(relx=0.5, rely=0.5, anchor=CENTER)
        # ------ Word Count
        self.word_count_label = Label(text=f"Word Count: {self.word_count}", font=FONT)
        self.word_count_label.place(relx=0.5, rely=0.95, anchor=CENTER)
        # ------
        self.window.bind('<Key>', self.key_press)
        self.window.mainloop()

    def key_press(self, event):
        if self.interval_sec_custom is None:  # Check if custom interval time is given
            self.interval_sec = INTERVAL_TIME_DEFAULT
        else:
            self.interval_sec = self.interval_sec_custom
        if event.char == event.keysym and not self.started_typing:
            self.count_down(self.total_sec)
            self.started_typing = True
        self.update_word_count()

    def update_word_count(self):
        inp = self.text_field.get(1.0, END)
        self.word_count = len(inp.split())
        self.word_count_label.configure(text=f"Word Count: {self.word_count}")

    def set_clock(self, seconds):
        timer_sec = seconds % 60
        timer_min = floor(seconds / 60)
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"  # Add 0 in front of single digit seconds
        if timer_min < 10:
            timer_min = f"0{timer_min}"  # Add 0 in front of single digit minutes
        self.total_timer_label.configure(text=f"Time: {timer_min}:{timer_sec}")

    def count_down(self, count):
        self.timer = self.window.after(1000, self.count_down, count - 1)

        # ------ Update clock labels
        self.set_clock(count)
        self.interval_timer_label.configure(text=f"{self.interval_sec}")
        highlight_thickness = 21 - (2 * self.interval_sec)  # Highlight thickness increase at each interval second
        if self.interval_sec >= 5 or self.interval_sec == self.interval_sec_custom:
            highlight_color = HIGHLIGHT_COLORS[4]
        else:
            highlight_color = HIGHLIGHT_COLORS[self.interval_sec - 1]
        self.text_field.configure(highlightthickness=highlight_thickness, highlightcolor=highlight_color)

        # ------ Check if either timer has reached zero
        if self.interval_sec == 0 or self.total_sec == 0:
            self.window.after_cancel(self.timer)
            self.end_session_window()

        # ----- Increment time
        self.total_sec -= 1
        self.interval_sec -= 1

    def settings_window(self):
        top = Toplevel(self.window)
        top.geometry("400x400")
        top.title("Settings")
        # ------ Total Timer settings, 30 seconds to 10 minutes at 30 second intervals
        time_minutes_label = Label(top, text="Total Time Minutes")
        time_minutes_label.pack(pady=10)
        timer_minutes_var = DoubleVar()
        timer_minutes_var.set(self.total_sec / 60)
        time_minutes_spinbox = Spinbox(top, from_=0.5, to=10, width=5,  increment=0.5, textvariable=timer_minutes_var)
        time_minutes_spinbox.pack()
        # ------ Interval Time Settings, 1 to 10 seconds
        interval_time_label = Label(top, text="Interval Time Seconds")
        interval_time_label.pack(pady=10)
        interval_var = IntVar()
        interval_var.set(self.interval_sec)
        interval_time_spinbox = Spinbox(top, from_=1, to=10, width=3,  increment=1, textvariable=interval_var)
        interval_time_spinbox.pack()
        # ------ Update Button
        update_button = Button(top,
                               text="Update",
                               command=lambda: [self.update_settings(timer_minutes_var.get(), interval_var.get()),
                                                top.destroy()])
        update_button.pack(pady=10)

    def update_settings(self, timer_minutes, interval_seconds):
        self.total_sec_custom = int(timer_minutes * 60)  # Convert timer minutes to seconds
        self.total_sec = self.total_sec_custom
        self.interval_sec_custom = interval_seconds
        self.interval_sec = self.interval_sec_custom

        self.interval_timer_label.configure(text=f"{self.interval_sec}")
        self.set_clock(self.total_sec)
        highlight_thickness = 21 - (2 * self.interval_sec)  # Highlight thickness increase at each interval second
        self.text_field.configure(highlightthickness=highlight_thickness)

    def end_session_window(self):
        self.window.withdraw()  # Hide main Window
        top = Toplevel(self.window)  # Create new toplevel window with results and export and reset options
        top.geometry("300x200")
        top.title("Results")
        if self.total_sec_custom is not None:
            starting_seconds = self.total_sec_custom
        else:
            starting_seconds = TOTAL_TIME_DEFAULT
        results_label = Label(top, text=f"You typed {self.word_count} words in {starting_seconds - self.total_sec} seconds!")
        results_label.place(relx=0.5, rely=0.3, anchor=CENTER)

        export_button = Button(top, text="Export", command=self.export_text)  # export text to .txt file
        export_button.place(relx=0.5, rely=0.5, anchor=CENTER)

        reset_button = Button(top, text="Reset", command=lambda: [self.reset_app(), top.destroy()])  # Start over
        reset_button.place(relx=0.5, rely=0.7, anchor=CENTER)

    def reset_app(self):
        self.window.deiconify()
        self.text_field.delete(1.0, END)  # Delete previous text
        self.text_field.configure(highlightthickness=1, highlightcolor=HIGHLIGHT_COLORS[4])  # Reset border

        # ------ Reset values to default
        self.started_typing = False

        # Check if custom total time value is given
        if self.total_sec_custom is None:
            self.total_sec = TOTAL_TIME_DEFAULT
        else:
            self.total_sec = self.total_sec_custom

        # Check if custom interval time is given
        if self.interval_sec_custom is None:
            self.interval_sec = INTERVAL_TIME_DEFAULT
        else:
            self.interval_sec = self.interval_sec_custom
        self.update_word_count()

        # ------ Reset timer labels
        self.set_clock(self.total_sec)
        self.interval_timer_label.configure(text=f"{self.interval_sec}")

    def export_text(self):
        filename = fd.asksaveasfile(mode="w", defaultextension=".txt")
        if filename is None:  # if no name is given for file then exit
            return
        text2save = str(self.text_field.get(1.0, END))
        filename.write(text2save)
        filename.close()


app = App()
