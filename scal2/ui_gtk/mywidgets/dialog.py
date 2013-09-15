from gi.repository import Gtk
from gi.repository import Gdk

class MyDialog:
    def startWaiting(self):
        self.queue_draw()
        self.vbox.set_sensitive(False)
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.WATCH))
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
    def endWaiting(self):
        self.get_window().set_cursor(Gdk.Cursor.new(Gdk.CursorType.LEFT_PTR))
        self.vbox.set_sensitive(True)
    def waitingDo(self, func, *args, **kwargs):
        self.startWaiting()
        try:
            func(*args, **kwargs)
        except Exception, e:
            raise e
        finally:
            self.endWaiting()



