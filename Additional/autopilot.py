from turtle import delay
import pyautogui
import time

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

#pyautogui.moveTo(currentMouseX, currentMouseY + 500, duration=2) # Move the mouse to XY coordinates.
time.sleep(5)
pyautogui.press('num3')
print("num3 pressed")

for _ in range(5):
    pyautogui.press('num1')
    time.sleep(0.5)
for _ in range(5):
    pyautogui.press('num2')
    time.sleep(0.5)

time.sleep(1)
pyautogui.press('num4')
print("num4 pressed")