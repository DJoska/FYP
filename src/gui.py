from os import link
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog, ttk
import os
from calib import calib, app, extract, utils, plotting
import get_points as pt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import pickle

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        Initialise the main application
        """
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Montserrat', size=18)
        self.normal_font = tkfont.Font(family='Montserrat', size=12)
        self.project_dir = "No project folder chosen"

        container = tk.Frame(self, width=1130, height=720)
        nav_bar = tk.Frame(self, width=150, height=720, background="#2c3e50")
        container.pack_propagate(False)
        nav_bar.pack_propagate(False)
        nav_bar.place(relx=0, rely=0)
        container.place(x=150,y=0)
        
        self.home_label = tk.Label(nav_bar, text="Home", font=self.title_font, bg="#2c3e50", fg="#ffffff", width=150, cursor="hand2")
        self.home_label.place(relx=0.5, y=30, anchor="center")
        self.build_label = tk.Label(nav_bar, text="Build", font=self.title_font, bg="#2c3e50", fg="#ffffff", width=150, cursor="hand2")
        self.build_label.place(relx=0.5, y=80, anchor="center")
        self.analyse_label = tk.Label(nav_bar, text="Analyse", font=self.title_font, bg="#2c3e50", fg="#ffffff", width=150, cursor="hand2")
        self.analyse_label.place(relx=0.5, y=130, anchor="center")

        self.home_label.bind("<Enter>", self.home_on_enter)
        self.home_label.bind("<Leave>", self.home_on_leave)
        self.home_label.bind("<Button-1>", self.home)

        self.build_label.bind("<Enter>", self.build_on_enter)
        self.build_label.bind("<Leave>", self.build_on_leave)
        self.build_label.bind("<Button-1>", self.build)

        self.analyse_label.bind("<Enter>", self.analyse_on_enter)
        self.analyse_label.bind("<Leave>", self.analyse_on_leave)
        self.analyse_label.bind("<Button-1>", self.analyse)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.place(x=0,y=0)

        self.show_frame("StartPage")

    # Binding events to change label appearances on enter, exit, and click
    def home(self, event):
        self.show_frame("StartPage")

    def home_on_enter(self, event):
        self.home_label.configure(bg="#34495e")

    def home_on_leave(self, event):
        self.home_label.configure(bg="#2c3e50")

    def build(self, event):
        self.show_frame("PageOne")

    def build_on_enter(self, event):
        self.build_label.configure(bg="#34495e")

    def build_on_leave(self, event):
        self.build_label.configure(bg="#2c3e50")

    def analyse(self, event):
        self.show_frame("PageTwo")

    def analyse_on_enter(self, event):
        self.analyse_label.configure(bg="#34495e")

    def analyse_on_leave(self, event):
        self.analyse_label.configure(bg="#2c3e50")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialise a frame for the home page
        """
        tk.Frame.__init__(self, parent, height=720, width=1130, bg="#ffffff")
        self.controller = controller
        self.pack_propagate(False)
        
        # --- Define functions to be used by GUI components ---

        def choose_folder():
            currdir = os.getcwd()
            controller.project_dir = filedialog.askdirectory(parent=self, initialdir=currdir, title='Please Select a Project Folder:')
            if len(controller.project_dir) > 0:
                print("You chose %s" % controller.project_dir)
                label_folder.configure(text=controller.project_dir)
        
        # --- Define and place GUI components ---

        label_folder = tk.Label(self, text=controller.project_dir, font=controller.normal_font, bg="#ffffff")
        label_folder.place(relx=0.5, rely=0.55, anchor="center")
        label = tk.Label(self, text="Home", font=controller.title_font, bg="#ffffff")
        label.place(relx=0.5, rely=0.1, anchor="center")
        button1 = tk.Button(self, text="Choose Project Folder", command=choose_folder)
        button1.place(relx=0.5, rely=0.5, anchor="center")
        

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialise a frame for the build page
        """
        tk.Frame.__init__(self, parent, height=720, width=1130, background="#ffffff")
        self.controller = controller
        self.pack_propagate(False)

        # --- Initialise class-wide variables ---

        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111, projection="3d")
        a.view_init(elev=20., azim=60)
        frame_no = 30
        x_free = tk.IntVar()
        y_free = tk.IntVar()
        z_free = tk.IntVar()

        parts_dict = {}
        points_dict = {}
        dof_dict = {}
        skel_dict = {}
        links_list = []

        # --- Define functions to be used by GUI components ---

        def update_canvas() -> None:
            """
            Replots canvas on the GUI with updated points
            """
            canvas = FigureCanvasTkAgg(f, self)
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            canvas._tkcanvas.place(relx=0.5, rely=0.45, anchor="center")

        def plot_points() -> None:
            """
            Plots extracted 3D points
            """
            #label = tk.Label(self, text=controller.project_dir, font=controller.normal_font, background="#ffffff")
            #label.place(relx=0.5, rely=0.5, anchor="center")
            parts = pt.get_bodyparts(controller.project_dir)

            for part in parts:
                vals = pt.plot_skeleton(controller.project_dir, part)
                #parts_dict[part] = [vals[0][frame_no],vals[1][frame_no],vals[2][frame_no]]
                #points_dict[part] = a.scatter(parts_dict[part][0],parts_dict[part][1],parts_dict[part][2])
                #update_canvas()
            
            combo.configure(values=parts)
            combo2.configure(values=parts)
            combo_move.configure(values=parts)
        
        def make_link() -> None:
            """
            Makes a link between the two defined bodyparts
            """
            part1 = combo.get()
            part2 = combo2.get()
            part_to_move = combo_move.get()

            a.plot3D([parts_dict[part1][0], parts_dict[part2][0]],
             [parts_dict[part1][1], parts_dict[part2][1]], 
             [parts_dict[part1][2], parts_dict[part2][2]], 'b')

            link_arr = [part1, part2]
            links_list.append(link_arr)
            update_canvas()
        
        def rotate_right() -> None:
            """
            Rotates the axes right
            """
            azimuth = a.azim
            a.view_init(elev=20., azim=azimuth+10)
            update_canvas()
        
        def rotate_left() -> None:
            """
            Rotates the axes left
            """
            azimuth = a.azim
            a.view_init(elev=20., azim=azimuth-10)
            update_canvas()
        
        def move_point() -> None:
            """
            Moves/places the selected point to the defined x, y, z
            """
            part_to_move = combo_move.get()

            if part_to_move in points_dict:
                point_to_move = points_dict[part_to_move]
                point_to_move.remove()

            new_x = float(x_spin.get())
            new_y = float(y_spin.get())
            new_z = float(z_spin.get())

            points_dict[part_to_move] = a.scatter(new_x,new_y, new_z)
            parts_dict[part_to_move] = [new_x, new_y, new_z]
            dof_dict[part_to_move] = [int(x_free.get()), int(y_free.get()), int(z_free.get())]

            update_canvas()

        def save_skeleton() -> None:
            """
            Writes the currently built skeleton to a pickle file
            """
            currdir = os.getcwd()
            skel_name = (field_name.get())
            output_dir = os.path.join(currdir, "skeletons", (skel_name + ".pickle"))

            skel_dict["links"] = links_list
            skel_dict["dofs"] = dof_dict
            skel_dict["positions"] = parts_dict

            print(output_dir)
            print(skel_dict)

            with open(output_dir, 'wb') as f:
                pickle.dump(skel_dict, f)

        # --- Define and place GUI components ---

        update_canvas()

        label_name = tk.Label(self, text="Enter skeleton name: ", font=controller.normal_font, background="#ffffff")
        label_name.place(relx=0.4, rely=0.15, anchor = "center")

        field_name = tk.Entry(self)
        field_name.place(relx=0.6, rely=0.15, anchor="center")

        label_plus = tk.Label(self, text="+", font=controller.title_font, background="#ffffff")
        label_plus.place(relx=0.45, rely=0.8, anchor = "center")

        combo = ttk.Combobox(self, values=["Empty"])
        combo.place(relx=0.3,rely=0.8, anchor = "center")
        combo2 = ttk.Combobox(self, values=["Empty"])
        combo2.place(relx=0.6,rely=0.8, anchor = "center")
        combo_move = ttk.Combobox(self, values=["Empty"])
        combo_move.place(relx=0.2,rely=0.4, anchor = "center")

        x_spin = tk.Spinbox(self, from_=0, to=10, increment=0.05)
        x_spin.place(relx=0.2, rely=0.45, anchor="center")
        y_spin = tk.Spinbox(self, from_=0, to=10, increment=0.05)
        y_spin.place(relx=0.2, rely=0.5, anchor="center")
        z_spin = tk.Spinbox(self, from_=0, to=10, increment=0.05)
        z_spin.place(relx=0.2, rely=0.55, anchor="center")

        label_x = tk.Label(self, text="x: ", font=controller.normal_font, background="#ffffff")
        label_x.place(relx=0.13, rely=0.45, anchor="center")
        label_y = tk.Label(self, text="y: ", font=controller.normal_font, background="#ffffff")
        label_y.place(relx=0.13, rely=0.5, anchor="center")
        label_z = tk.Label(self, text="z: ", font=controller.normal_font, background="#ffffff")
        label_z.place(relx=0.13, rely=0.55, anchor="center")

        label_dof = tk.Label(self, text="Degrees of Freedom", font=controller.normal_font, background="#ffffff")
        label_dof.place(relx=0.2, rely=0.27, anchor="center")

        x_check = tk.Checkbutton(self, text = "x", variable = x_free, \
                 onvalue = 1, offvalue = 0, bg = "#ffffff")
        x_check.place(relx = 0.15, rely = 0.3, anchor="center")
        y_check = tk.Checkbutton(self, text = "y", variable = y_free, \
                 onvalue = 1, offvalue = 0, bg = "#ffffff")
        y_check.place(relx = 0.2, rely = 0.3, anchor="center")
        z_check = tk.Checkbutton(self, text = "z", variable = z_free, \
                 onvalue = 1, offvalue = 0, bg = "#ffffff")
        z_check.place(relx = 0.25, rely = 0.3, anchor="center")

        button_update = tk.Button(self, text="Place", command=move_point)
        button_update.place(relx=0.2, rely=0.6, anchor="center")

        button_link = tk.Button(self, text="Make Link", command=make_link)
        button_link.place(relx=0.8, rely=0.8, anchor="center")

        label = tk.Label(self, text="Build", font=controller.title_font, background="#ffffff")
        label.place(relx=0, rely=0)
        button = tk.Button(self, text="Load Points", command=plot_points)
        button.place(relx=0.5, rely=0.1, anchor="center")

        button_right = tk.Button(self, text="Right", command=rotate_right)
        button_right.place(relx=0.8, rely=0.3, anchor="center")
        button_left = tk.Button(self, text="Left", command=rotate_left)
        button_left.place(relx=0.8, rely=0.4, anchor="center")

        button_save = tk.Button(self, text="Save Model", command=save_skeleton)
        button_save.place(relx=0.5, rely=0.9, anchor="center")

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        """
        Initialise a frame for the analyse page
        """
        tk.Frame.__init__(self, parent, height=720, width=1130, background="#ffffff")
        self.controller = controller
        self.pack_propagate(False)
        label = tk.Label(self, text="Analyse", font=controller.title_font, background="#ffffff")
        label.place(relx=0, rely=0)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

if __name__ == "__main__":
    app = Application()
    app.geometry("1280x720")
    app.title("Final Year Project")
    app.mainloop()