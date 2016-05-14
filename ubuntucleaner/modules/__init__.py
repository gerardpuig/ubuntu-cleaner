import os
import sys
import logging
import inspect

from ubuntucleaner.settings.debug import log_traceback

log = logging.getLogger('ModuleLoader')

def module_cmp(m1, m2):
    return cmp(m1.get_title(), m2.get_title())


class ModuleLoader:
    module_table = None
    category_table = None

    category_names = (
        ('broken', _('Broken Modules')),
        ('application', _('Applications')),
        ('appearance', _('Appearance')),
        ('startup', _('Startup')),
        ('desktop', _('Desktop')),
        ('personal', _('Personal')),
        ('system', _('System')),
        ('other', _('Other')),
    )

    default_features = ('janitor',)

    search_loaded_table = {}
    fuzz_search_table = {}

    def __init__(self, feature, user_only=False):
        self.module_table = {}
        self.category_table = {}
        self.feature = feature

        for k, v in self.category_names:
            self.category_table[k] = {}

        # First import system staff
        if not user_only:
            log.info("Loading system modules for %s..." % feature)
            try:
                m = __import__('ubuntucleaner.%s' % self.feature, fromlist='ubuntucleaner')
                self.do_folder_import(m.__path__[0])
            except ImportError, e:
                log.error(e)

    @classmethod
    def fuzz_search(cls, text):
        modules = []
        text = text.lower()
        for k, v in cls.fuzz_search_table.items():
            if text in k and v not in modules:
                modules.append(v)

        return modules

    def do_single_import(self, path, mark_user=False):
        module_name = os.path.splitext(os.path.basename(path))[0]
        log.debug("Try to load module: %s" % module_name)
        if module_name in sys.modules:
            del sys.modules[module_name]

        try:
            package = __import__(module_name)
        except Exception, e:
            log.error("Module import error: %s", str(e))
        else:
            for k, v in inspect.getmembers(package):
                self._insert_module(k, v, mark_user)

    def do_folder_import(self, path, mark_user=False):
        if path not in sys.path:
            sys.path.insert(0, path)

        for f in os.listdir(path):
            full_path = os.path.join(path, f)

            if os.path.isdir(full_path) and \
                    os.path.exists(os.path.join(path, '__init__.py')):
                self.do_single_import(f, mark_user)
            elif f.endswith('.py') and f != '__init__.py':
                self.do_single_import(f, mark_user)

    def _insert_module(self, k, v, mark_user=False):
        if self.is_module_active(k, v):
            self.module_table[v.get_name()] = v

            if mark_user:
                v.__user_extension__ = True

            if v.get_category() not in dict(self.category_names):
                self.category_table['other'][v.get_name()] = v
            else:
                self.category_table[v.get_category()][v.get_name()] = v
            if hasattr(v, '__keywords__'):
                for attr in ('name', 'title', 'description', 'keywords'):
                    value = getattr(v, 'get_%s' % attr)()
                    self.fuzz_search_table[value.lower()] = v

    @classmethod
    def is_module_active(cls, k, v):
        from ubuntucleaner.janitor import JanitorPlugin
        try:
            if "Plugin" in k and k not in ('JanitorPlugin', 'JanitorCachePlugin') and \
                    issubclass(v, JanitorPlugin) and hasattr(v, '__utmodule__'):
                return v.is_active()
            return False
        except Exception:
            log_traceback(log)
            return False

    def get_categories(self):
        for k, v in self.category_names:
            yield k, v

    def get_modules_by_category(self, category):
        modules = self.category_table.get(category).values()
        modules.sort(module_cmp)
        return modules

    def get_module(self, name):
        return self.module_table[name]
