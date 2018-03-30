import os
import logging
import StringIO
import traceback

import gi
gi.require_version("Notify", "0.7")
from gi.repository import Gtk, Gdk, Notify

from ubuntucleaner.utils import system
from ubuntucleaner.settings.constants import CONFIG_ROOT

#The terminal has 8 colors with codes from 0 to 7
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ =  "\033[1m"

#The background is set with 40 plus the number of the color,
#and the foreground with 30
COLORS = {
    'WARNING':  COLOR_SEQ % (30 + YELLOW) + 'WARNING' + RESET_SEQ,
    'INFO':     COLOR_SEQ % (30 + WHITE) + 'INFO' + RESET_SEQ,
    'DEBUG':    COLOR_SEQ % (30 + BLUE) + 'DEBUG' + RESET_SEQ,
    'CRITICAL': COLOR_SEQ % (30 + YELLOW) + 'CRITICAL' + RESET_SEQ,
    'ERROR':    COLOR_SEQ % (30 + RED) + 'ERROR' + RESET_SEQ,
}


def on_copy_button_clicked(widget, text):
    notify = Notify.Notification()
    notify.update(summary=_('Error message has been copied'),
                  body=_('Now click "Report" to enter the bug '
                         'report website. Make sure to attach the '
                         'error message in "Further information".'),
                  icon='ubuntu-cleaner')
    notify.show()


def run_traceback(level, textview_only=False, text_only=False):
    '''Two level: fatal and error'''
    from ubuntucleaner.gui import GuiBuilder

    output = StringIO.StringIO()
    exc = traceback.print_exc(file=output)

    worker = GuiBuilder('traceback.xml')

    textview = worker.get_object('%s_view' % level)

    buffer = textview.get_buffer()
    iter = buffer.get_start_iter()
    anchor = buffer.create_child_anchor(iter)
    button = Gtk.Button(label=_('Copy Error Message'))
    button.show()

    textview.add_child_at_anchor(button, anchor)

    error_text = "\nDistribution: %s\nApplication: %s\nDesktop:%s\n\n%s" % (system.DISTRO,
                                       system.APP,
                                       system.DESKTOP,
                                       output.getvalue())

    buffer.insert(iter, error_text)
    button.connect('clicked', on_copy_button_clicked, error_text)

    if text_only:
        return error_text

    if textview_only:
        return textview
    else:
        dialog = worker.get_object('%sDialog' % level.capitalize())
        dialog.destroy()
        output.close()


def get_traceback():
    return run_traceback('error', text_only=True)


def log_traceback(log):
    log.error(get_traceback())


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            record.levelname = COLORS.get(record.levelname, record.levelname)
        return logging.Formatter.format(self, record)


class CleanerLogger(logging.Logger):
    COLOR_FORMAT = "[" + BOLD_SEQ + "%(name)s" + RESET_SEQ + \
                   "][%(levelname)s] %(message)s (" + BOLD_SEQ + \
                   "%(filename)s" + RESET_SEQ + ":%(lineno)d)"
    NO_COLOR_FORMAT = "[%(name)s][%(levelname)s] %(message)s " \
                      "(%(filename)s:%(lineno)d)"
    LOG_FILE_HANDLER = None

    def __init__(self, name):
        logging.Logger.__init__(self, name)

        #Add two handlers, a stderr one, and a file one
        color_formatter = ColoredFormatter(CleanerLogger.COLOR_FORMAT)
        no_color_formatter = ColoredFormatter(CleanerLogger.NO_COLOR_FORMAT,
                                              False)

        #create the single file appending handler
        if CleanerLogger.LOG_FILE_HANDLER is None:
            filename = os.path.join(CONFIG_ROOT, 'ubuntu-cleaner.log')
            CleanerLogger.LOG_FILE_HANDLER = logging.FileHandler(filename, 'w')
            CleanerLogger.LOG_FILE_HANDLER.setFormatter(no_color_formatter)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(CleanerLogger.LOG_FILE_HANDLER)
        self.addHandler(console)
        return


def enable_debugging():
    logging.getLogger().setLevel(logging.DEBUG)


def disable_debugging():
    logging.getLogger().setLevel(logging.INFO)


def disable_logging():
    logging.getLogger().setLevel(logging.CRITICAL + 1)

logging.setLoggerClass(CleanerLogger)


def log_func(log):
    def wrap(func):
        def func_wrapper(*args, **kwargs):
            log.debug("%s:" % func)
            for i, arg in enumerate(args):
                log.debug("\targs-%d: %s" % (i + 1, arg))
            for k, v in enumerate(kwargs):
                log.debug("\tdict args-%d: %s: %s" % (k, v, kwargs[v]))
            return func(*args, **kwargs)
        return func_wrapper
    return wrap
