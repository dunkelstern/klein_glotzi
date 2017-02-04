import platform
import threading
from datetime import datetime
from time import sleep
import gi
from serial.tools import list_ports
import serial

# we need Gtk 3.0
gi.require_version('Gtk', '3.0')

# import everything we need for a Gtk Window
from gi.repository import Gtk, Gio, Gdk, GObject


# Control window
class ControlWindow(Gtk.Window):
    def __init__(self):
        self.connection = None
        self.old_h = -1
        self.old_v = -1

        # initialize window
        Gtk.Window.__init__(self, title="Klein Glotzi")

        # add header bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Klein Glotzi"
        self.set_titlebar(self.header)

        # video source buttons
        self.box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        # device drop down
        type_store = Gtk.ListStore(str, str)

        port_combobox = Gtk.ComboBox.new_with_model(type_store)
        renderer_text = Gtk.CellRendererText()
        port_combobox.pack_start(renderer_text, True)
        port_combobox.add_attribute(renderer_text, "text", 0)
        port_combobox.connect('changed', self.on_port_changed)
        port_combobox.set_vexpand(False)

        for port in list_ports.grep('2341:0043'):
            type_store.append([port.name, port.device])

        self.box.pack_start(port_combobox, True, True, 0)

        # sliders
        h_label = Gtk.Label("Horizontal")
        self.box.pack_start(h_label, True, True, 0)
        self.h_scale = Gtk.Scale()
        self.h_scale.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.h_scale.set_range(0,1023)
        self.h_scale.set_value(512)
        self.h_scale.set_draw_value(False)
        self.box.pack_start(self.h_scale, True, True, 0)

        v_label = Gtk.Label("Vertical")
        self.box.pack_start(v_label, True, True, 0)
        self.v_scale = Gtk.Scale()
        self.v_scale.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.v_scale.set_range(0,1023)
        self.v_scale.set_value(512)
        self.v_scale.set_draw_value(False)
        self.box.pack_start(self.v_scale, True, True, 0)

        # no border
        self.set_border_width(10)

        # show all window elements
        self.show_all()

        # resize the window and disable resizing by user if needed
        self.set_resizable(False)

        # on quit run callback to stop pipeline
        self.connect("delete-event", self.quit)

    def __del__(self):
        self.quit()

    def on_port_changed(self, combobox):
        index = combobox.get_active()
        if index is not None:
            model = combobox.get_model()
            entry = list(model[index])
            if self.connection:
                connection.close()
            self.connection = serial.Serial(entry[-1], 9600)
            GObject.timeout_add(100, self.on_timeout, None)


    def on_timeout(self, context):
        if self.connection:
            h = int(self.h_scale.get_value())
            v = int(self.v_scale.get_value())

            if v != self.old_v or h != self.old_h:
                self.connection.write(
                    '{},{}\n'.format(1023 - h,v).encode('ASCII')
                )

            self.old_h = h
            self.old_v = v

            return True
        else:
            return False


    def quit(self, sender, gparam):
        if self.connection:
            self.connection.write(
                '{},{}\n'.format(-1, -1).encode('ASCII')
            )

        Gtk.main_quit()
