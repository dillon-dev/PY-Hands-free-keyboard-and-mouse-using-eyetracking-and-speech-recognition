import tkinter as tk
import re


def errorgui():
    root = tk.Tk()
    # message blocks
    command = 'Error: Try Again'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def commandgui():
    root = tk.Tk()
    # message blocks
    command = 'Command'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def keyboardgui():
    root = tk.Tk()
    # message blocks
    command = 'Keyboard'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def mousegui():
    root = tk.Tk()
    # message blocks
    command = 'Mouse'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def spellinggui():
    root = tk.Tk()
    # message blocks
    command = 'Spelling'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def lookingdownallowedgui():
    root = tk.Tk()
    # message blocks
    command = 'Clicking Disabled'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()


def lookingdownnotallowedgui():
    root = tk.Tk()
    # message blocks
    command = 'Clicking Enabled'

    h = 150
    w = 300

    # around using canvas
    canvas = tk.Canvas(root, height=h, width=w)
    canvas.pack()

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, 1220, 630))

                        # duck egg blue
    frame = tk.Frame(root, bg='#A6C0C5')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text=command, bg='#A6C0C5', font=("Calibri", 25))
    label.place(relwidth=1, relheight=1)

    root.resizable(False, False)

    # destory after 1 sec
    root.after(1000, root.destroy)

    root.mainloop()
