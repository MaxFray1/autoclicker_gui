import csv
import time
import pyautogui
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pathlib import Path
from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Automate:
    def __init__(self):
        self.event_log = []
        self.screenshots = []
        self.key_dict = {
            'Key.alt': Key.alt,
            'Key.alt_l': Key.alt_l,
            'Key.alt_r': Key.alt_r,
            'Key.alt_gr': Key.alt_gr,
            'Key.ctrl': Key.ctrl,
            'Key.ctrl_l': Key.ctrl_l,
            'Key.ctrl_r': Key.ctrl_r,
            'Key.shift': Key.shift,
            'Key.shift_l': Key.shift_l,
            'Key.shift_r': Key.shift_r,
            'Key.backspace': Key.backspace,
            'Key.cmd': Key.cmd,
            'Key.cmd_l': Key.cmd_l,
            'Key.cmd_r': Key.cmd_r,
            'Key.down': Key.down,
            'Key.up': Key.up,
            'Key.right': Key.right,
            'Key.left': Key.left,
            'Key.delete': Key.delete,
            'Key.home': Key.home,
            'Key.end': Key.end,
            'Key.page_up': Key.page_up,
            'Key.page_down': Key.page_down,
            'Key.insert': Key.insert,
            'Key.space': Key.space,
            'Key.tab': Key.tab,
            'Key.enter': Key.enter,
            'Key.esc': Key.esc,
            'Key.f1': Key.f1,
            'Key.f2': Key.f2,
            'Key.f3': Key.f3,
            'Key.f4': Key.f4,
            'Key.f5': Key.f5,
            'Key.f6': Key.f6,
            'Key.f7': Key.f7,
            'Key.f8': Key.f8,
            'Key.f9': Key.f9,
            'Key.f10': Key.f10,
            'Key.f11': Key.f11,
            'Key.f12': Key.f12,
            'Key.f13': Key.f13,
            'Key.f14': Key.f14,
            'Key.f15': Key.f15,
            'Key.f16': Key.f16,
            'Key.f17': Key.f17,
            'Key.f18': Key.f18,
            'Key.f19': Key.f19,
            'Key.f20': Key.f20,
            'Key.menu': Key.menu,
            'Key.num_lock': Key.num_lock,
            'Key.pause': Key.pause,
            'Key.print_screen': Key.print_screen,
            'Key.scroll_lock': Key.scroll_lock
        }
        self.button_dict = {
            'Button.left': Button.left,
            'Button.right': Button.right,
            'Button.middle': Button.middle
        }
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.count = 0
        self.file = 'file.csv'
        self.delay = 0

    def on_release(self, key):
        self.screenshots.append(pyautogui.screenshot())
        # myScreenshot.save(r'Path to save screenshot\file name.png')
        try:
            self.event_log.append([self.count, 'keyboard', 'release', 0, 0, key.char, round(time.time() - self.delay, 2)])
            print(self.count, '[keyboard', 0, 0, key.char, 'release]', sep=', ')
        except AttributeError:
            self.event_log.append([self.count, 'keyboard', 'release', 0, 0, str(key), round(time.time() - self.delay, 2)])
            print(self.count, '[keyboard', 0, 0, str(key), 'release]', sep=', ')
            if key == keyboard.Key.esc:
                return False
        self.count += 1
        self.delay = time.time()

    def on_press(self, key):
        self.screenshots.append(pyautogui.screenshot())
        # myScreenshot.save(r'Path to save screenshot\file name.png')
        try:
            self.event_log.append([self.count, 'keyboard', 'press', 0, 0, key.char, round(time.time() - self.delay, 2)])
            print(self.count, '[keyboard', 0, 0, key.char, 'press]', sep=', ')
        except AttributeError:
            self.event_log.append([self.count, 'keyboard', 'press', 0, 0, str(key), round(time.time() - self.delay, 2)])
            print(self.count, '[keyboard', 0, 0, key, 'press]', sep=', ')
        self.count += 1
        self.delay = time.time()

    def on_click(self, x, y, button, pressed):
        self.screenshots.append(pyautogui.screenshot())
        # myScreenshot.save(r'Path to save screenshot\file name.png')
        self.event_log.append([self.count, 'mouse', 'press' if pressed else 'release', x, y, str(button), round(time.time() - self.delay, 2)])
        print(self.count, '[mouse', x, y, button, 'press]' if pressed else 'release]', sep=', ')
        self.count += 1
        self.delay = time.time()

    def on_scroll(self, x, y, dx, dy):
        self.screenshots.append(pyautogui.screenshot())
        # myScreenshot.save(r'Path to save screenshot\file name.png')
        self.event_log.append([self.count, 'mouse', 'scroll', x, y, dx, dy, 0.01])
        print(self.count, '[mouse', x, y, dx, dy, 'down' if dy < 0 else 'up', 'scroll]', sep=', ')
        self.count += 1
        self.delay = time.time()

    def monitoring(self):
        self.event_log.clear()
        self.delay = time.time()
        with mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        return self.event_log

    def export_data(self, file='-'):
        if file != '-':
            self.file = file
        with open(self.file, 'w') as f:
            write = csv.writer(f)
            write.writerows(self.event_log)
        directory_path = Path(file).resolve().parent
        for i in range(len(self.screenshots)):
            self.screenshots[i].save(str(directory_path) + '/images/screnshoot' + str(i) + '.png')

    def open_data(self, file='-'):
        self.event_log.clear()
        if file != '-':
            self.file = file

        with open(self.file, newline='') as f:
            reader = csv.reader(f)
            self.event_log = list(reader)

    def run_script(self, steps):
        for i in steps:
            if i[5] != keyboard.Key.backspace:
                time.sleep(float(i[6]))
            if i[1] == 'mouse':
                self.mouse_controller.position = (int(i[3]), int(i[4]))
                if i[2] == 'scroll':
                    self.mouse_controller.scroll(i[5], i[6])
                elif i[2] == 'press':
                    self.mouse_controller.press(self.button_dict.get(i[5]))
                elif i[2] == 'release':
                    self.mouse_controller.release(self.button_dict.get(i[5]))
            elif i[1] == 'keyboard':
                if i[2] == 'press':
                    if len(i[5]) > 3:
                        self.keyboard_controller.press(self.key_dict.get(i[5]))
                    else:
                        self.keyboard_controller.press(i[5])
                elif i[2] == 'release':
                    if len(i[5]) > 2:
                        self.keyboard_controller.release(self.key_dict.get(i[5]))
                    else:
                        self.keyboard_controller.release(i[5])


class GUI:
    def __init__(self, window):
        self.automate = Automate()
        self.window = window
        self.data = []
        self.count = 0
        self.file = 'file.csv'
        self.window.title('AutoClicker')
        # root.iconbitmap('')
        self.window.geometry("726x870")
        self.window.configure(bg="#FFFFFF")

        self.canvas = tk.Canvas(window, bg="#FFFFFF", height=870, width=726,
                        bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        # self.screenshot = tk.PhotoImage(
        #     file=relative_to_assets("image_1.png"))
        # self.screenshot_show = self.canvas.create_image(
        #     375.0, 174.0, image=self.screenshot)

        self.tree_frame = tk.Frame(root)
        self.tree_frame.place(x=22.0, y=370.0, width=686.0, height=224.0)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.my_tree.pack()

        self.tree_scroll.config(command=self.my_tree.yview)

        self.my_tree['columns'] = ('id', 'Type', 'Action', 'X', 'Y', 'Button', 'Delay')
        self.my_tree.bind("<Double-1>", self.onDoubleClick)

        self.my_tree.column("#0", width=0, stretch=tk.NO)
        self.my_tree.column('id', anchor=tk.W, width=60)
        self.my_tree.column('Type', anchor=tk.W, width=120)
        self.my_tree.column('Action', anchor=tk.W, width=120)
        self.my_tree.column('X', anchor=tk.CENTER, width=80)
        self.my_tree.column('Y', anchor=tk.CENTER, width=80)
        self.my_tree.column('Button', anchor=tk.W, width=120)
        self.my_tree.column('Delay', anchor=tk.W, width=80)

        self.my_tree.heading("#0", text="", anchor=tk.W)
        self.my_tree.heading('id', text='id', anchor=tk.W)
        self.my_tree.heading('Type', text='Type', anchor=tk.W)
        self.my_tree.heading('Action', text='Action', anchor=tk.W)
        self.my_tree.heading('X', text='X', anchor=tk.CENTER)
        self.my_tree.heading('Y', text='Y', anchor=tk.CENTER)
        self.my_tree.heading('Button', text='Button', anchor=tk.W)
        self.my_tree.heading('Delay', text='Delay', anchor=tk.W)

        self.select_record = tk.Button(self.window, text="Select", command=self.select_record)
        self.select_record.place(x=22.0, y=762.0, width=106.0, height=40.0)

        self.update_record = tk.Button(self.window, text="Update", command=self.update_record)
        self.update_record.place(x=22.0, y=820.0, width=106.0, height=40.0)

        self.add_record = tk.Button(self.window, text='Add', command=self.add_record)
        self.add_record.place(x=166.0, y=762.0, width=106.0, height=40.0)

        self.remove_record = tk.Button(self.window, text='Remove', command=self.remove_record)
        self.remove_record.place(x=166.0, y=820.0, width=106.0, height=40.0)

        self.record = tk.Button(self.window, text='Record', command=self.record)
        self.record.place(x=598.0, y=762.0, width=106.0, height=40.0)

        self.run = tk.Button(self.window, text='Run', command=self.run_script)
        self.run.place(x=600.0, y=820.0, width=106.0, height=40.0)

        self.import_button = tk.Button(self.window, text='Import', command=self.import_data)
        self.import_button.place(x=310.0, y=762.0, width=106.0, height=40.0)

        self.export_button = tk.Button(self.window, text='Export', command=self.export_data)
        self.export_button.place(x=310.0, y=820.0, width=106.0, height=40.0)

        self.nl = tk.Label(text='id', bg='#fff', fg='#000')
        self.nl.place(x=22.0, y=612.0)

        self.nl = tk.Label(text='Type', bg='#fff', fg='#000')
        self.nl.place(x=166.0, y=612.0)

        self.nl = tk.Label(text='Action', bg='#fff', fg='#000')
        self.nl.place(x=310.0, y=612.0)

        self.nl = tk.Label(text='X', bg='#fff', fg='#000')
        self.nl.place(x=454.0, y=612.0)

        self.nl = tk.Label(text='Y', bg='#fff', fg='#000')
        self.nl.place(x=598.0, y=612.0)

        self.nl = tk.Label(text='Button', bg='#fff', fg='#000')
        self.nl.place(x=22.0, y=678.0)

        self.nl = tk.Label(text='Delay', bg='#fff', fg='#000')
        self.nl.place(x=166.0, y=678.0)

        self.nl = tk.Label(text='Count', bg='#fff', fg='#000')
        self.nl.place(x=500.0, y=800.0)

        self.id_box = tk.Entry(bg='#fff', fg='#000')
        self.id_box.place(x=22.0, y=644.0, width=120.0)

        self.type_box = tk.Entry(bg='#fff', fg='#000')
        self.type_box.place(x=166.0, y=644.0, width=120.0)

        self.action_box = tk.Entry(bg='#fff', fg='#000')
        self.action_box.place(x=310.0, y=644.0, width=120.0)

        self.x_box = tk.Entry(bg='#fff', fg='#000')
        self.x_box.place(x=454.0, y=644.0, width=120.0)

        self.y_box = tk.Entry(bg='#fff', fg='#000')
        self.y_box.place(x=598.0, y=644.0, width=120.0)

        self.button_box = tk.Entry(bg='#fff', fg='#000')
        self.button_box.place(x=22.0, y=710.0, width=120.0)

        self.delay_box = tk.Entry(bg='#fff', fg='#000')
        self.delay_box.place(x=166.0, y=710.0, width=120.0)

        self.count_box = tk.Entry(bg='#fff', fg='#000')
        self.count_box.place(x=500.0, y=832.0, width=80.0)

    def run_script(self):
        count = self.count_box.get()
        if count:
            for i in range(int(count)):
                self.automate.run_script(self.data)

    def grabdata(self):
        self.data.clear()
        for line in self.my_tree.get_children():
            values = self.my_tree.item(line)['values']
            self.data.append([values[0], values[1], values[2], values[3], values[4], values[5], values[6]])

    def open_data(self, file='-'):
        self.data.clear()
        if file != '-':
            self.file = file
        with open(self.file, newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)

    def record(self):
        self.data = self.automate.monitoring()
        for record in self.data:
            self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
            self.count += 1

    def import_data(self):
        filename = askopenfilename()
        if filename != '':
            self.open_data(filename)
            for i in self.my_tree.get_children():
                self.my_tree.delete(i)
            for record in self.data:
                self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                                    values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
                self.count += 1

    def export_data(self, file=''):
        file = asksaveasfilename()
        self.automate.export_data(file)
        # if file != '':
        #     self.file = file
        # with open(self.file, 'w') as f:
        #     write = csv.writer(f)
        #     write.writerows(self.data)

    def add_record(self):
        self.my_tree.insert(parent='', index='end', iid=self.count, text='',
                            values=(self.id_box.get(), self.type_box.get(), self.action_box.get(), self.x_box.get(),
                                    self.y_box.get(), self.button_box.get(), self.delay_box.get()))
        self.count += 1
        self.id_box.delete(0, tk.END)
        self.type_box.delete(0, tk.END)
        self.action_box.delete(0, tk.END)
        self.x_box.delete(0, tk.END)
        self.y_box.delete(0, tk.END)
        self.button_box.delete(0, tk.END)
        self.delay_box.delete(0, tk.END)
        self.grabdata()

    def remove_record(self):
        x = self.my_tree.selection()
        for i in x:
            self.my_tree.delete(i)
        self.grabdata()

    def select_record(self):
        self.id_box.delete(0, tk.END)
        self.type_box.delete(0, tk.END)
        self.action_box.delete(0, tk.END)
        self.x_box.delete(0, tk.END)
        self.y_box.delete(0, tk.END)
        self.button_box.delete(0, tk.END)
        self.delay_box.delete(0, tk.END)

        selected = self.my_tree.focus()
        values = self.my_tree.item(selected, 'values')
        self.id_box.insert(0, values[0])
        self.type_box.insert(0, values[1])
        self.action_box.insert(0, values[2])
        self.x_box.insert(0, values[3])
        self.y_box.insert(0, values[4])
        self.button_box.insert(0, values[5])
        self.delay_box.insert(0, values[6])

    def update_record(self):
        selected = self.my_tree.focus()
        self.my_tree.item(selected, text='', values=(self.id_box.get(), self.type_box.get(),
                                                     self.action_box.get(), self.x_box.get(),
                                                     self.y_box.get(), self.button_box.get(), self.delay_box.get()))
        self.grabdata()
        self.id_box.delete(0, tk.END)
        self.type_box.delete(0, tk.END)
        self.action_box.delete(0, tk.END)
        self.x_box.delete(0, tk.END)
        self.y_box.delete(0, tk.END)
        self.button_box.delete(0, tk.END)
        self.delay_box.delete(0, tk.END)

    def onDoubleClick(self, event):
        self.id_box.delete(0, tk.END)
        self.type_box.delete(0, tk.END)
        self.action_box.delete(0, tk.END)
        self.x_box.delete(0, tk.END)
        self.y_box.delete(0, tk.END)
        self.button_box.delete(0, tk.END)
        self.delay_box.delete(0, tk.END)
        selected = self.my_tree.identify('item', event.x, event.y)
        values = self.my_tree.item(selected, 'values')
        self.id_box.insert(0, values[0])
        self.type_box.insert(0, values[1])
        self.action_box.insert(0, values[2])
        self.x_box.insert(0, values[3])
        self.y_box.insert(0, values[4])
        self.button_box.insert(0, values[5])
        self.delay_box.insert(0, values[6])


root = tk.Tk()
my_gui = GUI(root)
root.mainloop()
