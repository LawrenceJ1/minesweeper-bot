import pyautogui

width, height = pyautogui.size()
boxes = []

for i in pyautogui.locateAllOnScreen("square.png", confidence=0.98):
    boxes.append(i)
    pyautogui.moveTo(i[0], i[1], 0.2)
print(len(boxes))