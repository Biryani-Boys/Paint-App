import os
import subprocess
from tkinter import *
from tkinter import messagebox, colorchooser
from tkinter.filedialog import asksaveasfilename

import pyscreenshot as ImageGrab


class main:
    def __init__(self, master):
        self.root = master
        self.root.title("PAINT")
        self.root.geometry("800x520")
        self.color_fg = 'black'  # Colour of pen
        self.color_bg = 'white'  # Background colour
        self.root.configure(background='white')
        self.root.resizable(0, 0)
        self.color_frame = LabelFrame(self.root, relief=RIDGE, bg='white')
        self.color_frame.place(x=5, y=0, width=40, height=160)
        self.undo = open('undo.rec', 'w')


        # making colour buttons

        colors = ['blue', 'black', 'red', '#00a5f9', '#682cbf', '#009888']
        i = 7
        j = 0
        for color in colors:
            if color == 'blue':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colorblue).grid(
                    row=i, column=j)
            elif color == 'black':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colorblack).grid(
                    row=i, column=j)
            elif color == 'red':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colorred).grid(
                    row=i, column=j)
            elif color == '#00a5f9':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colora).grid(
                    row=i, column=j)
            elif color == '#682cbf':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colorb).grid(
                    row=i, column=j)
            elif color == '#009888':
                Button(self.color_frame, bd=2, bg=color, relief=RIDGE, width=4, command=self.change_colorc).grid(
                    row=i, column=j)
            i = i + 1

        # making other buttons and placing them in apprprite place
        self.color_button = Button(self.root, text='PALLET', font=('calibri', 10), bd=3, bg='white', command=self.choose_color,
                                    width=8, relief=RIDGE)
        self.color_button.place(x=0,y=190)

        self.erazer_button = Button(self.root, text='ERAZE', font=('calibri', 10), bd=3, bg='white', command=self.eraze,
                                    width=8, relief=RIDGE)
        self.erazer_button.place(x=0, y=215)
        self.clear_button = Button(self.root, text='CLEAR', bd=3, bg='white', command=self.clear, width=8, relief=RIDGE)
        self.clear_button.place(x=0, y=245)
        self.save_button = Button(self.root, text='SAVE', bd=3, bg='white', command=self.save, width=8, relief=RIDGE)
        self.save_button.place(x=0, y=275)
        self.pen_size_scale_frame = Label(self.root, text='SIZE', bd=3, bg='white', font=('calibri', 11), relief=RIDGE)
        self.pen_size_scale_frame.place(x=1, y=305)
        self.size_choosen = Text(self.root, width=3, height=1, bd=3, relief=RIDGE, font=('calibri', 11))
        self.size_choosen.place(x=33, y=305)
        self.size_choosen.insert(END, '3')
        self.undo_button = Button(self.root, text='Undo', font=('calibri', 10), bd=3, bg='white',
                                  command=self.undo_exec, width=8, relief=RIDGE)
        self.undo_button.place(x=0, y=400)


        # making the canvas and making it recognise movements of the mouse

        self.canvas = Canvas(self.root, bg='white', bd=3, relief=GROOVE, height=505, width=710)
        self.canvas.place(x=80, y=5)

        self.old_x = None
        self.old_y = None
        self.penwidth = 3
        self.tag = 0
        self.canvas.bind('<B1-Motion>', self.paint)  # drawing  line
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    # All functions are defined below

    def paint(self, e):
        '''creates a canvas where you can paint'''
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, e.x, e.y, width=self.size_choosen.get("0.0", "end-1c"),
                                    fill=self.color_fg,
                                    capstyle=ROUND, smooth=True, tag='my_tag' + str(self.tag))

        self.old_x = e.x
        self.old_y = e.y

    def reset(self, e):
        '''reseting or cleaning the canvas'''
        self.old_x = None
        self.old_y = None
        self.undo.write(f"self.canvas.delete('{'my_tag' + str(self.tag)}')\n")
        self.tag += 1

    def clear(self):
        '''clears the canvas'''
        self.canvas.delete(ALL)

    def change_colorblue(self):
        '''change colour to blue'''
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = 'blue'

    def change_colorblack(self):
        '''change colour to black'''
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = 'black'

    def change_colorred(self):
        '''change colour to red'''
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = 'red'

    def change_colora(self):
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = '#00a5f9'

    def change_colorb(self):
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = '#682cbf'

    def change_colorc(self):
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = '#009888'

    def eraze(self):
        '''erazing stuff simply by changing colour of the brush to white'''
        self.undo.write(f"self.color_fg='{self.color_fg}'\n")
        self.color_fg = 'white'

    def undo_exec(self):
        self.undo.close()
        # Find last line and execute it
        file = open("copy.txt", 'w')
        with open("undo.rec", 'r') as undo:
            length = sum(1 for x in undo)
        with open("undo.rec", 'r') as undo:
            count = 0
            for line in undo:
                count += 1
                if count != length:
                    file.write(line)
                pass
        file.close()
        os.replace(r'copy.txt', r'undo.rec')
        try:
            command = line
            with open("redo.rec", 'a') as redo:
                redo.write(command)
            exec(command)
        except UnboundLocalError:
            pass
        self.undo = open("undo.rec", 'a')

    def save(self):

        # Making values for a screenshort
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        screenshort = ImageGrab.grab().crop((x, y, x1, y1))

        # Asking format
        filename: str = asksaveasfilename(initialdir="/Desktop", title="Select file", filetypes=(
            ('JPEG', ('*.jpg', '*.jpeg', '*.jpe', '*.jfif')), ('PNG', '*.png'), ('PS', '*.ps'),
            ('BMP', ('*.bmp', '*.jdib')),
            ('GIF', '*.gif'),))
        print(filename)
        if filename.endswith('.ps'):
            # Saving a postscript file
            try:
                self.canvas.postscript(file=filename, colormode='color')
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('No file saved')

        else:
            try:
                screenshort.save(filename)
                messagebox.showinfo('File saved : ', str(filename))
            except:
                print('Error Saving File')
    def choose_color(self):
        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title="Choose color")
        self.color_fg=color_code





if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Paint')
    root.mainloop()
