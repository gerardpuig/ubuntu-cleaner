from gi.repository import GObject, Gtk


class BaseDialog(Gtk.MessageDialog):
    def __init__(self, **kwargs):
        title = kwargs.pop('title', '')
        message = kwargs.pop('message', '')

        GObject.GObject.__init__(self, **kwargs)

        if title:
            self.set_title(title)

        if message:
            self.set_content(message)

    def set_title(self, title):
        self.set_markup('<big><b>%s</b></big>' % title)

    def set_content(self, message):
        if self.get_property('text'):
            self.format_secondary_markup(message)
        else:
            self.set_markup(message)
    
    def launch(self):
        self.run()
        self.destroy()


class ErrorDialog(BaseDialog):
    def __init__(self, title='', message='', parent=None,
                 type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK):
        BaseDialog.__init__(self, title=title, message=message,
                            parent=parent, message_type=type, buttons=buttons)


class InfoDialog(BaseDialog):
    def __init__(self, title='', message='', parent=None,
                 type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK):
        BaseDialog.__init__(self, title=title, message=message,
                            parent=parent, message_type=type, buttons=buttons)


class WarningDialog(BaseDialog):
    def __init__(self, title='', message='', parent=None,
                 type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.OK):
        BaseDialog.__init__(self, title=title, message=message,
                            parent=parent, message_type=type, buttons=buttons)


class QuestionDialog(BaseDialog):
    def __init__(self, title='', message='', parent=None,
                 type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO):
        BaseDialog.__init__(self, title=title, message=message,
                            parent=parent, message_type=type, buttons=buttons)

