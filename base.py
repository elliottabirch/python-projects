import mss
import pyautogui
import keyboard
import time


# Global flag to monitor F12 key state
f12_pressed = False
last_press_time = 0
debounce_interval = 0.2  # 200 milliseconds

def on_f12_press(key):
    global f12_pressed, last_press_time
    current_time = time.time()
    if key.name == 'f12' and (current_time - last_press_time) > debounce_interval:
        f12_pressed = True
        last_press_time = current_time
        print("F12 pressed")  # Debugging print

def on_f12_release(key):
    global f12_pressed
    if key.name == 'f12':
        f12_pressed = False
        print("F12 released")  # Debugging print

keyboard.on_press(on_f12_press)
keyboard.on_release(on_f12_release)

def get_screen_capture(x, y, width, height):
    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        return sct_img

def get_pixel_color(sct_img, x, y):
    # Validate coordinates
    if x >= sct_img.width or y >= sct_img.height or x < 0 or y < 0:
        raise ValueError(f"Coordinates ({x}, {y}) are out of bounds.")

    # The width of a line in bytes
    width_bytes = sct_img.width * 4  # 4 bytes per pixel (BGRA)

    # Calculate the position in the raw data
    pos = y * width_bytes + x * 4

    # Check if pos is within the raw data range
    if pos + 4 > len(sct_img.raw):
        raise ValueError(f"Position {pos} is out of range in raw data.")

    # Extract the BGR values (ignoring Alpha)
    b, g, r, _ = sct_img.raw[pos:pos + 4]
    return r, g, b  # Return in RGB format

def check_pixels_and_press_key(pixel_checks):
    print("checking pixels")
    # screen_capture = get_screen_capture(0, 0, 200, 200)
    # for (x, y, color, key) in pixel_checks:
    #     if get_pixel_color(screen_capture, x, y) == color:
    #         pyautogui.press(key)
    #         break

def run_while_f12_held_down(pixel_checks):
    while True:
        if f12_pressed:
            # print("F12 is currently pressed.")  # Debugging print
            check_pixels_and_press_key(pixel_checks)
        elif keyboard.is_pressed('esc'):  # Exit condition
            print("Exiting...")  # Debugging print
            break

# Define the pixels, their expected colors, and associated key presses
pixel_checks = [
    # (122, 50, (0, 0, 0), 'x'),
    # (100, 199, (255, 0, 0), 'y'),
    # Add more as needed
]

# Run the function
run_while_f12_held_down(pixel_checks)