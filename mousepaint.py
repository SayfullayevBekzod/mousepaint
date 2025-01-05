from PIL import Image, ImageDraw
import PIL
from tkinter import *

width = 500
height = 500
white = (255, 255, 255)

def save():
    filename = 'image.png'
    image1.save(filename)
    print(f"Rasm '{filename}' nomi bilan saqlandi.")

def paint(event):
    global last_x, last_y
    x, y = event.x, event.y

    if last_x is None or last_y is None:
        last_x, last_y = x, y

    cv.create_line(last_x, last_y, x, y, fill='black', width=5)
    draw.line([last_x, last_y, x, y], fill='black', width=5)

    last_x, last_y = x, y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

root = Tk()
root.title("Mouse as Pen")

cv = Canvas(root, width=width, height=height, bg='white')
cv.pack(expand=True, fill='both')

image1 = PIL.Image.new('RGB', (width, height), white)
draw = ImageDraw.Draw(image1)

last_x, last_y = None, None
cv.bind('<B1-Motion>', paint)
cv.bind('<ButtonRelease-1>', reset)

button = Button(root, text='Save', command=save)
button.pack(pady=10)

root.mainloop()
