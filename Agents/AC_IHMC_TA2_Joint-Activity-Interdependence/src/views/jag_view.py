from tkinter import BOTH, Frame, NSEW, Label
from tkinter import ttk
from tkinter.ttk import Treeview
from ..models.jags import asist_jags as aj


class JagView(Frame):

    def __init__(self, parent, callsign, model):
        super().__init__(parent, borderwidth=3, bg=callsign)

        self.model = model
        self.callsign = callsign
        label_text = callsign.upper() + ' Player'
        if callsign.lower() == 'black':
            label_text = 'TEAM'
        Label(self, text=label_text,  background=callsign, foreground='white').pack()
        self.treeview = Treeview(self)
        self.treeview.pack(expand=True, fill=BOTH)
        self.treeview.tag_configure('complete', foreground='black')
        self.treeview.tag_configure('active', foreground='black')
        self.treeview.tag_configure('ongoing', foreground=callsign)
        self.treeview.tag_configure('inactive', foreground='gray60')
        self.treeview.tag_configure('restricted', foreground='red')
        self.treeview.tag_configure(callsign, background=callsign)

    def update(self):
        for jag_instance in self.model.jag_instances:
            if jag_instance.urn != aj.SEARCH_AREA['urn'] and jag_instance.urn != aj.GET_IN_RANGE['urn'] and jag_instance.urn != aj.CLEAR_PATH['urn']:
                self.insert_or_update_jag_instance_node(self.treeview, '', jag_instance)

    def insert_or_update_jag_instance_node(self, treeview, parent_id, jag_instance, index='end'):
        # insert jag recursively if it does not exist
        if not treeview.exists(jag_instance.id):
            treeview.insert(parent_id, index, jag_instance.id, text=jag_instance.short_string())
            treeview.item(jag_instance.id, open=True)

        if self.callsign != 'black':
            treeview.item(jag_instance.id, text=jag_instance.short_string())
            if jag_instance.is_active():
                if jag_instance.is_ongoing():
                    treeview.item(jag_instance.id, tags='ongoing', open=True)
                else:
                    treeview.item(jag_instance.id, tags='active', open=True)
            else:
                if jag_instance.is_complete():
                    treeview.item(jag_instance.id, tags='complete', open=False)
                else:
                    treeview.item(jag_instance.id, tags='inactive', open=False)

            # only apply to top level node for rescue victim
            if jag_instance.urn == aj.RESCUE_VICTIM['urn']:
                role_restriction = jag_instance.get_role_restriction()
                if role_restriction is not None:
                    # currently, only one restriction type based on medic (red)
                    treeview.item(jag_instance.id, tags='restricted')

        for child in jag_instance.children:
            self.insert_or_update_jag_instance_node(treeview, jag_instance.id, child)

    def open_children(self, parent, treeview):
        treeview.item(parent, open=True)  # open parent
        for child in treeview.get_children(parent):
            self.open_children(child, treeview)  # recursively open children

