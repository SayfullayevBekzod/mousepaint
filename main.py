import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import pytesseract
import re


class MouseAsPenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse as Pen & Save Image")

        # Oyna o'lchamini o'rnatish
        self.canvas_width = 1000
        self.canvas_height = 900

        # Tkinter canvas
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # PIL image & draw
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Sichqoncha hodisalarini bog'lash
        self.canvas.bind("<B1-Motion>", self.draw_with_mouse)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Qo'shimcha tugmalar
        self.save_button = tk.Button(root, text="Save Image", command=self.save_image)
        self.save_button.pack(pady=10)

        # Rasm chizish boshlandi yoki yo'q
        self.is_drawing = False

    def draw_with_mouse(self, event):
        """Sichqoncha harakati bilan chizish"""
        x, y = event.x, event.y
        if not self.is_drawing:
            self.last_x, self.last_y = x, y
            self.is_drawing = True
        self.canvas.create_line(self.last_x, self.last_y, x, y, fill="black", width=2)
        self.draw.line([self.last_x, self.last_y, x, y], fill="black", width=2)
        self.last_x, self.last_y = x, y

    def stop_drawing(self, event):
        """Chizishni to'xtatish"""
        self.is_drawing = False

    def save_image(self):
        """Chizilgan rasmni saqlash va matematik amallarni bajarish"""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)
            print(f"Image saved to {file_path}")

            # OCR yordamida rasmdan sonlarni aniqlash va amallarni bajarish
            self.aniqlash_va_chiqarish(file_path)

    def aniqlash_va_chiqarish(self, image_path):
        """Rasmni ochish va OCR yordamida matematik ifodalarni aniqlash"""
        rasm = Image.open(image_path)

        # OCR yordamida matnni olish
        matn = pytesseract.image_to_string(rasm, config='--psm 6')  # PSM 6 - blokli matnlarni o'qish uchun
        print(f"Rasmdan o'qilgan matn: {matn}")

        # Matematik ifodalarni qidirish
        self.bajarish(matn)

    def bajarish(self, matn):
        """Matnni tahlil qilish va matematik amallarni bajarish"""
        # Matematik ifodalarni aniqlash (raqamlar va amallar)
        matn = matn.replace("x", "*").replace("X", "*")  # 'x' yoki 'X' ko'pincha ko'paytirish belgisi
        # Regex yordamida ifodalarni topish
        matematik_ifodalar = re.findall(r'\d+[\+\-\*/\^]\d+', matn)

        if not matematik_ifodalar:
            print("Matematika ifodasi topilmadi.")
            return

        print("Matematika ifodalari:")
        for ifoda in matematik_ifodalar:
            try:
                # Python eval() yordamida ifodani hisoblash
                natija = eval(ifoda)
                print(f"{ifoda} = {natija}")
            except Exception as e:
                print(f"Xatolik yuz berdi: {e}")


# Dastur ishga tushirilishi
if __name__ == "__main__":
    root = tk.Tk()
    app = MouseAsPenApp(root)
    root.mainloop()
