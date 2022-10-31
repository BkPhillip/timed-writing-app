"""
Timed Writing App
Bryson Phillip
October 30, 2022

A writing app with both a timer and a short interval timer to end the session if no keys are pressed before it reaches
zero. Then either timer reaches zero, the word count and total time spent writing are displayed. The user has the option
to reset the writing pad or export their writing to file. This app is designed to help users not overthink when writing.
Good for stream of conscious writing.

"""
from tkinter import *
from tkinter import filedialog as fd
from math import floor

LABEL_FONT = ("Arial", 18)
TEXT_FONT = ("Arial", 22)
HIGHLIGHT_COLORS = ["#980000", "#ff0000", "#ff9900", "#ffff00", "#00ff00"]
TOTAL_TIME_DEFAULT = 300
INTERVAL_TIME_DEFAULT = 5


class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x900")
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
        self.total_timer_label = Label(text="Time: 00:00", font=LABEL_FONT)
        self.total_timer_label.place(relx=0.5, rely=0.05, anchor=CENTER)
        self.set_clock(TOTAL_TIME_DEFAULT)
        self.interval_timer_label = Label(text="5", font=LABEL_FONT)
        self.interval_timer_label.place(relx=0.8, rely=0.05, anchor=CENTER)
        self.settings_button = Button(text="Settings", command=self.settings_window)
        self.settings_button.place(relx=0.2, rely=0.05, anchor=CENTER)
        # ------ Text Field
        self.text_field = Text(height=28,
                               font=TEXT_FONT,
                               wrap=WORD,
                               spacing2=10,
                               highlightthickness=11,
                               highlightcolor=HIGHLIGHT_COLORS[4])
        self.text_field.focus_set()
        self.text_field.place(relx=0.5, rely=0.5, anchor=CENTER)
        # ------ Word Count
        self.word_count_label = Label(text=f"Word Count: {self.word_count}", font=LABEL_FONT)
        self.word_count_label.place(relx=0.5, rely=0.95, anchor=CENTER)
        # ------
        self.window.bind('<Key>', self.key_press)
        self.window.mainloop()

    # This function starts clock on first key press, resets interval time, and calls update_word_count
    def key_press(self, event):
        if self.interval_sec_custom is not None:  # Use custom interval time if assigned
            self.interval_sec = self.interval_sec_custom
        else:
            self.interval_sec = INTERVAL_TIME_DEFAULT
        if event.char == event.keysym and not self.started_typing:  # Start clock once first letter key is pressed
            self.count_down(self.total_sec)
            self.started_typing = True
        self.update_word_count()  # Calculate word count with every key press

    # This function counts the number of words in the text field and updates the label on main window
    def update_word_count(self):
        inp = self.text_field.get(1.0, END)
        self.word_count = len(inp.split())
        self.word_count_label.configure(text=f"Word Count: {self.word_count}")

    # This function updates the clock
    def set_clock(self, seconds):
        timer_sec = seconds % 60
        timer_min = floor(seconds / 60)
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"  # Add 0 in front of single digit seconds
        if timer_min < 10:
            timer_min = f"0{timer_min}"  # Add 0 in front of single digit minutes
        self.total_timer_label.configure(text=f"Time: {timer_min}:{timer_sec}")

    # This function updates the text field highlight thickness and color. Highlight color is green at
    # interval timer >= 5 seconds or when no seconds counted down even on custom interval times. Color changes to yellow
    # at 4 seconds, orange at 3 seconds, red at 2 seconds, and dark red at 1 seconds remaining. Highlight thickness
    # increases as interval timer reaches zero.
    def update_highlight_border(self):
        highlight_thickness = 21 - (2 * self.interval_sec)  # Highlight thickness increase at each interval second
        if self.interval_sec >= 5 or self.interval_sec == self.interval_sec_custom:  # Highlight stays green > 5 seconds
            highlight_color = HIGHLIGHT_COLORS[4]
        else:
            highlight_color = HIGHLIGHT_COLORS[self.interval_sec - 1]
        self.text_field.configure(highlightthickness=highlight_thickness, highlightcolor=highlight_color)

    # This function is called every second to subtract one second from the time on the clock and the interval timer
    # and check if either timer has reached zero to end session.
    def count_down(self, count):
        self.timer = self.window.after(1000, self.count_down, count - 1)
        # ------ Update clock labels
        self.set_clock(count)  # Update Clock
        self.interval_timer_label.configure(text=f"{self.interval_sec}")  # Update Interval Count
        self.update_highlight_border()  # Update Highlight Border color and thickness
        # ------ Check if either timer has reached zero
        if self.interval_sec == 0 or self.total_sec == 0:
            self.window.after_cancel(self.timer)
            self.results_window()
        # ----- Increment time
        self.total_sec -= 1
        self.interval_sec -= 1

    # This functions opens a toplevel window with options to select new clock length and interval time
    def settings_window(self):
        top = Toplevel(self.window)
        top.geometry("400x200")
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
                                                top.destroy()])  # Update settings and close toplevel window
        update_button.pack(pady=10)

    # This function, called from a settings menu button, updates the clock and interval time to the selected values
    def update_settings(self, timer_minutes, interval_seconds):
        self.total_sec = self.total_sec_custom = int(timer_minutes * 60)  # Convert timer minutes to seconds
        self.interval_sec = self.interval_sec_custom = interval_seconds
        self.interval_timer_label.configure(text=f"{self.interval_sec}")  # Update interval time
        self.set_clock(self.total_sec)  # Update clock
        highlight_thickness = 21 - (2 * self.interval_sec)  # Highlight thickness increase at each interval second
        self.text_field.configure(highlightthickness=highlight_thickness)  # Update text highlight thickness

    # This function opens a new window to display results of timed writing. Gives option to reset writing app or
    # export written text to .txt file
    def results_window(self):
        self.window.withdraw()  # Hide main Window
        top = Toplevel(self.window)  # Create new toplevel window with results and export and reset options
        top.geometry("300x200")
        top.title("Results")
        # Check if custom clock time is given
        if self.total_sec_custom is not None:  # Use custom total time value if assigned
            starting_seconds = self.total_sec_custom  # Used fo calculating time spent typing
        else:
            starting_seconds = TOTAL_TIME_DEFAULT
        # ------ Results Label, displays word count and seconds spent typing
        results_label = Label(top,
                              text=f"You typed {self.word_count} words in {starting_seconds - self.total_sec} seconds!")
        results_label.place(relx=0.5, rely=0.3, anchor=CENTER)
        # ------ Export Button
        export_button = Button(top, text="Export", command=self.export_text)  # export text to .txt file
        export_button.place(relx=0.5, rely=0.5, anchor=CENTER)
        # ------ Reset Button
        reset_button = Button(top, text="Reset", command=lambda: [self.reset_app(), top.destroy()])  # Start over
        reset_button.place(relx=0.5, rely=0.7, anchor=CENTER)
        # Close App if User closes results window using the window manager
        top.protocol("WM_DELETE_WINDOW", self.window.destroy)

    # This function resets app text field and clock. Clock and interval time will be reset to custom values if set.
    # This function is called from a results window button
    def reset_app(self):
        self.window.deiconify()  # Hide main window
        self.text_field.delete(1.0, END)  # Delete previous text
        # ------ Reset values to default
        self.started_typing = False
        # Check if custom clock time is given
        if self.total_sec_custom is not None:  # Use custom total time value if assigned
            self.total_sec = self.total_sec_custom
        else:
            self.total_sec = TOTAL_TIME_DEFAULT
        # Check if custom interval time is given
        if self.interval_sec_custom is not None:  # Use custom interval time if assigned
            self.interval_sec = self.interval_sec_custom
        else:
            self.interval_sec = INTERVAL_TIME_DEFAULT
        self.update_highlight_border()  # Reset border thickness and color
        # ------ Reset labels
        self.update_word_count()  # Reset wordcount to zero
        self.set_clock(self.total_sec)  # Update Clock
        self.interval_timer_label.configure(text=f"{self.interval_sec}")  # Reset Interval label

    # This function exports the text in the text field to a file. This function is called from a results window button
    def export_text(self):
        filename = fd.asksaveasfile(mode="w", defaultextension=".txt")
        if filename is None:  # if no name is given for file then exit
            return
        text2save = str(self.text_field.get(1.0, END))
        filename.write(text2save)
        filename.close()


app = App()
