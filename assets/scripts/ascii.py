import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageEnhance, ExifTags, ImageTk

ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._`' "



CHAR_WIDTH = 8
CHAR_HEIGHT = 12

class ASCIIApp:
    def __init__(self, root, image_path):
        self.root = root
        self.image_path = image_path
        self.original_image = self.load_image(image_path)
        self.show_photo = False
        self.dark_theme = False
        self.resize_after_id = None
        self.contrast = 1.0

        self.setup_ui()
        self.render()

    def load_image(self, path):
        img = Image.open(path)
        try:
            for orientation in ExifTags.TAGS:
                if ExifTags.TAGS[orientation] == 'Orientation':
                    exif = img._getexif()
                    if exif:
                        val = exif.get(orientation)
                        if val == 3:
                            img = img.rotate(180, expand=True)
                        elif val == 6:
                            img = img.rotate(270, expand=True)
                        elif val == 8:
                            img = img.rotate(90, expand=True)
                    break
        except Exception:
            pass
        return img

    def setup_ui(self):
        self.root.title("Responsive ASCII & Photo Viewer")

        toolbar = tk.Frame(self.root, bg="lightgray")
        toolbar.pack(side="top", fill="x")
        tk.Button(toolbar, text="Toggle Theme", command=self.toggle_theme).pack(side="left", padx=5)
        tk.Button(toolbar, text="Choose New Photo", command=self.choose_photo).pack(side="left", padx=5)
        tk.Button(toolbar, text="Show Real Photo", command=self.toggle_photo).pack(side="left", padx=5)
        tk.Button(toolbar, text="Contrast +", command=self.increase_contrast).pack(side="left", padx=5)
        tk.Button(toolbar, text="Contrast -", command=self.decrease_contrast).pack(side="left", padx=5)

        self.content = tk.Frame(self.root)
        self.content.pack(fill="both", expand=True)

        self.left_frame = tk.Frame(self.content)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.content)

        self.text = tk.Text(self.left_frame, wrap="none", font=("Courier", 8), bd=0, highlightthickness=0)
        self.text.place(x=0, y=0)

        self.photo_label = tk.Label(self.right_frame)
        self.photo_label.place(x=0, y=0)

        self.root.bind("<Configure>", self.on_resize)

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.apply_theme()

    def toggle_photo(self):
        self.show_photo = not self.show_photo
        self.render()

    def choose_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.image_path = path
            self.original_image = self.load_image(path)
            self.render()

    def increase_contrast(self):
        self.contrast = min(5.0, self.contrast + 0.2)
        print(f"[INFO] Contraste augmenté : {self.contrast:.2f}")
        self.render_ascii()

    def decrease_contrast(self):
        self.contrast = max(0.1, self.contrast - 0.2)
        print(f"[INFO] Contraste diminué : {self.contrast:.2f}")
        self.render_ascii()

    def apply_theme(self):
        bg = "black" if self.dark_theme else "white"
        fg = "white" if self.dark_theme else "black"
        for widget in [self.left_frame, self.right_frame, self.content, self.text, self.photo_label]:
            widget.config(bg=bg)
        self.text.config(fg=fg)

    def on_resize(self, event):
        if self.resize_after_id:
            self.root.after_cancel(self.resize_after_id)
        self.resize_after_id = self.root.after(100, self.render)

    def render(self):
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()

        if self.show_photo:
            self.left_frame.pack(side="left", fill="both", expand=True)
            self.right_frame.pack(side="right", fill="both", expand=True)
            self.render_photo()
        else:
            self.left_frame.pack(side="left", fill="both", expand=True)

        self.render_ascii()
        self.apply_theme()

    def render_ascii(self):
        self.left_frame.update_idletasks()
        w = self.left_frame.winfo_width()
        h = self.left_frame.winfo_height()
        if w < 20 or h < 20:
            return

        cols = max(10, w // CHAR_WIDTH)
        rows = max(5, h // CHAR_HEIGHT)

        img = self.original_image.resize((cols, rows)).convert("L")
        img = ImageEnhance.Contrast(img).enhance(self.contrast)
        pixels = img.getdata()

        ascii_str = "".join(ASCII_CHARS[p * (len(ASCII_CHARS) - 1) // 255] for p in pixels)
        ascii_img = "\n".join(ascii_str[i:i + cols] for i in range(0, len(ascii_str), cols))

        self.text.config(
            wrap="none",
            font=("Courier", 8),
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            spacing1=0,
            spacing3=0
        )
        self.text.place(x=0, y=0, width=w, height=h)
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", ascii_img)

    def render_photo(self):
        self.right_frame.update_idletasks()
        w = self.right_frame.winfo_width()
        h = self.right_frame.winfo_height()
        if w < 20 or h < 20:
            return

        img = self.original_image.copy()
        img.thumbnail((w, h), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.photo_label.config(image=photo)
        self.photo_label.image = photo
        self.photo_label.place(x=0, y=0, width=photo.width(), height=photo.height())

def main():
    root = tk.Tk()
    root.geometry("1000x600")
    root.withdraw()
    path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
    if not path:
        return
    root.deiconify()
    app = ASCIIApp(root, path)
    root.mainloop()

if __name__ == "__main__":
    main()
