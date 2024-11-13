import ctypes
import time
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

# Constants
user32 = ctypes.windll.user32

# Global variables
running = False
keep_awake = False  # Flag for Awake Mode
cps = 10  # Default CPS
click_type = "left"  # Default click type ('left', 'right', 'space', or a key)
toggle_key = 0x70  # Virtual key code for F1 (toggle start/stop)
SPACE_KEY_CODE = 0x20  # Virtual key code for spacebar

# Perform click or key press based on selection
def perform_click():
    global click_type
    print("Attempting to perform click of type:", click_type)  # Debug message
    
    try:
        if click_type == "left":
            user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse down
            user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse up
        elif click_type == "right":
            user32.mouse_event(8, 0, 0, 0, 0)  # Right mouse down
            user32.mouse_event(16, 0, 0, 0, 0)  # Right mouse up
        elif click_type == "space":
            user32.keybd_event(SPACE_KEY_CODE, 0, 0, 0)  # Space key down
            user32.keybd_event(SPACE_KEY_CODE, 0, 2, 0)  # Space key up
        else:
            # Simulate a keyboard key press for other keys
            key_code = ord(click_type.upper())  # Convert character to ASCII code
            user32.keybd_event(key_code, 0, 0, 0)  # Key down
            user32.keybd_event(key_code, 0, 2, 0)  # Key up
        print("Click performed successfully.")
    except Exception as e:
        print("Error performing click:", e)

# Auto-clicker function
def auto_clicker():
    global running, keep_awake
    while running:
        perform_click()
        time.sleep(1 / cps)  # Adjust the delay for CPS (Clicks per second)

# Perform the action to keep the system awake (move mouse by 10 pixels right and left with 1 second delay)
def perform_awake_action():
    # Move mouse by 10 pixels to the right
    user32.mouse_event(0x0001, 10, 0, 0, 0)  # Move mouse 10 pixels to the right
    time.sleep(1)  # Wait for 1 second
    # Move mouse by 10 pixels to the left (back to the original position)
    user32.mouse_event(0x0001, -10, 0, 0, 0)  # Move mouse 10 pixels to the left
    time.sleep(1)  # Wait for 1 second

# Awake mode function with alternating right-left movement
def awake_mode():
    global keep_awake
    while keep_awake:
        perform_awake_action()  # Perform the action to keep the system awake

# Start clicking or "Awake Mode"
def start_clicking():
    global running
    if not running:
        running = True
        threading.Thread(target=auto_clicker, daemon=True).start()  # Start auto-clicker thread
        print("Started clicking.")

# Stop clicking or "Awake Mode"
def stop_clicking():
    global running
    running = False
    print("Stopped clicking.")

# Set CPS
def input_cps():
    global cps
    cps_input = simpledialog.askstring("Input CPS", "Enter clicks per second:")
    if cps_input and cps_input.isdigit():
        cps = int(cps_input)
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")

# Set click type
def set_click_type():
    global click_type
    click_type_input = simpledialog.askstring("Set Click Type", "Enter 'left', 'right', 'space', or a single key:")
    if click_type_input:
        click_type_input = click_type_input.lower()
        if click_type_input in ['left', 'right', 'space'] or (len(click_type_input) == 1 and click_type_input.isalpha()):
            click_type = click_type_input
        else:
            messagebox.showerror("Invalid Input", "Enter 'left', 'right', 'space', or a single key.")
    else:
        messagebox.showerror("Invalid Input", "Please enter a valid click type.")

# Toggle "Awake Mode"
def toggle_awake_mode():
    global keep_awake
    keep_awake = not keep_awake
    if keep_awake:
        # Start the awake mode in a new thread
        threading.Thread(target=awake_mode, daemon=True).start()
        messagebox.showinfo("Awake Mode", "Awake Mode activated. Your computer will stay awake.")
    else:
        messagebox.showinfo("Awake Mode", "Awake Mode deactivated.")

# Check for the toggle key press (F1)
def check_for_keypress():
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(toggle_key) & 0x8000:
            if running:
                stop_clicking()
            else:
                start_clicking()
            time.sleep(0.5)
        time.sleep(0.1)

# Create the main window
def create_window():
    window = tk.Tk()
    window.title("Auto Clicker and Awake Mode")
    window.attributes("-topmost", True)

    # Original buttons
    start_button = tk.Button(window, text="Start Clicking", command=start_clicking)
    start_button.pack(pady=10)

    stop_button = tk.Button(window, text="Stop Clicking", command=stop_clicking)
    stop_button.pack(pady=10)

    cps_button = tk.Button(window, text="Set CPS", command=input_cps)
    cps_button.pack(pady=10)

    click_type_button = tk.Button(window, text="Set Click Type", command=set_click_type)
    click_type_button.pack(pady=10)

    # New button for "Awake Mode"
    awake_button = tk.Button(window, text="Toggle Awake Mode", command=toggle_awake_mode)
    awake_button.pack(pady=10)

    exit_button = tk.Button(window, text="Exit", command=window.quit)
    exit_button.pack(pady=10)

    window.mainloop()

# Run the GUI and key listening thread
if __name__ == "__main__":
    threading.Thread(target=check_for_keypress, daemon=True).start()
    create_window()











