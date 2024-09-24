from tkinter import Frame, NSEW, Label
from tkinter import Tk, BOTH
from tkinter import ttk

from src.views import jag_view


class TeamView(Tk):

    def __init__(self, client):
        super().__init__()

        self.client = client
        self.frames_created = False
        self.jag_view_map = {}

        width = 1800
        height = 800
        self.title('JAG Visualizer')
        # screen_width = self.winfo_screenwidth()
        # window_width = self.winfo_width()
        # distance = screen_width - window_width
        # x_left = int(distance)
        # y_top = int(0)
        # self.geometry("+{}+{}".format(x_left, y_top))
        self.geometry(str(width) + 'x' + str(height))
        self['bg'] = 'white'

        self.style = ttk.Style(self)
        self.style.configure('TLabel', background='white', foreground='black')
        self.style.configure('Treeview', background='white', foreground='black')
        self.style.configure('Treeview.complete', background='green', foreground='black')

        # Create Frame widget
        self.team_frame = Frame(self, width=width, height=height, bg='white')
        self.team_frame.pack(expand=True, fill=BOTH)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.team_frame.grid_rowconfigure(0, weight=1)

        if self.client is not None:
            self.team_frame.after(100, self.update)
            self.label = Label(self.team_frame, width=width, text='No players yet...')
            self.label.pack(expand=True, fill=BOTH)

    def get_team_frame(self):
        return self.team_frame

    def add_jag_view(self, teammate, frame):
        column_index = len(self.jag_view_map)
        self.team_frame.grid_columnconfigure(column_index, weight=1)
        frame.grid(row=0, column=column_index, sticky=NSEW)
        self.jag_view_map[teammate] = frame

    def update(self):
        if self.frames_created:
            for player in self.jag_view_map.keys():
                jag_view_frame = self.jag_view_map[player]
                jag_view_frame.update()
        else:
            if len(self.client.players()) > 0:
                self.label.destroy()
                for player in self.client.players().values():
                    callsign = player.callsign.lower()
                    jag_view_frame = jag_view.JagView(self.team_frame, callsign, player.joint_activity_model)
                    self.add_jag_view(callsign, jag_view_frame)
                self.frames_created = True

        self.team_frame.after(100, self.update)
