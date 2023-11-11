import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import random
import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Eisenhower Matrix")
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack()

        # Draw the quadrants
        self.canvas.create_line(200, 0, 200, 400, arrow=tk.LAST)  # Add arrow
        self.canvas.create_line(0, 200, 400, 200, arrow=tk.LAST)  # Add arrow

        # Add labels
        self.canvas.create_text(210, 10, text="重要", anchor="w")  # Add label "Important" on the left
        self.canvas.create_text(370, 220, text="紧急", anchor="w")  # Add label "Urgent" on the right

        # Create a button to add a sticker
        self.add_sticker_button = tk.Button(self, text="新建", command=self.add_sticker)
        self.add_sticker_button.pack()
        self.usage_button = tk.Button(self, text="使用方法", command=self.show_usage)
        self.usage_button.pack()
        # Initialize an empty list to store the stickers
        self.stickers = []
    def change_text(self, event):
        # Change the text of the sticker
        widget = event.widget
        new_text = simpledialog.askstring("输入", "创建新任务:")
        if new_text is not None:
            widget.config(text=new_text)
    
    def show_usage(self):
        messagebox.showinfo("使用方法", "点击“新建”按钮创建新任务，双击编辑，右键删除。") #可以改为默认创建一个贴纸，显示使用方法

    def delete_sticker(self, event):
        # Delete the sticker
        widget = event.widget
        widget.destroy()
        self.stickers.remove(widget)

    def add_sticker(self):
        # Create a new sticker as a draggable label
        sticker = tk.Label(self.canvas, text="Sticker", bg="yellow", relief="raised")
        sticker.bind("<Button-1>", self.start_drag)
        sticker.bind("<B1-Motion>", self.drag)
        sticker.bind("<ButtonRelease-1>", self.stop_drag)
        sticker.bind("<Double-Button-1>", self.change_text)  # Add double click binding
        sticker.bind("<Button-3>", self.delete_sticker)  # Add right click binding

        # Ensure the sticker does not overlap with existing stickers
        while True:
            x = random.randint(0, 400)
            y = random.randint(0, 400)
            overlap = False
            for existing_sticker in self.stickers:
                if abs(existing_sticker.winfo_x() - x) < 50 and abs(existing_sticker.winfo_y() - y) < 50:
                    overlap = True
                    break
            if not overlap:
                break

        sticker.place(x=x, y=y)

        # Add the sticker to the list
        self.stickers.append(sticker)
    def stop_drag(self, event):
        pass

    def start_drag(self, event):
        # Record the starting position of the sticker
        widget = event.widget
        widget.start_x = event.x
        widget.start_y = event.y

    def drag(self, event):
        # Move the sticker by the distance dragged
        widget = event.widget
        x = widget.winfo_x() - widget.start_x + event.x
        y = widget.winfo_y() - widget.start_y + event.y
        widget.place(x=x, y=y)
    
    import json

    def save_stickers(self):
        # Save the stickers to a file
        stickers_data = []
        for sticker in self.stickers:
            stickers_data.append({
                'text': sticker.cget("text"),
                'x': sticker.winfo_x(),
                'y': sticker.winfo_y()
            })
        with open('stickers.json', 'w') as f:
            json.dump(stickers_data, f)

    def load_stickers(self):
        # Load the stickers from a file
        try:
            with open('stickers.json', 'r') as f:
                stickers_data = json.load(f)
        except FileNotFoundError:
            return

        for sticker_data in stickers_data:
            self.add_sticker(text=sticker_data['text'], x=sticker_data['x'], y=sticker_data['y'])
root = tk.Tk()
app = Application(master=root)
app.mainloop()