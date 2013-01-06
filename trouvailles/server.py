from pyramid.config import Configurator


class SettingsDict(dict):

    separator = "."

    def copy(self):
        new_items = self.__class__()
        for k, v in self.iteritems():
            new_items[k] = v
        return new_items

    def getsection(self, section):
        section_items = self.__class__()
        # If the section is "" then get keys without a section.
        if not section:
            for key, value in self.iteritems():
                if self.separator not in key:
                    section_items[key] = value
        # Otherwise, get keys prefixed with that section name.
        else:
            prefix = section + self.separator
            for key, value in self.iteritems():
                if key.startswith(prefix):
                    section_items[key[len(prefix):]] = value
        return section_items

    def setdefaults(self, *args, **kwds):
        for arg in args:
            if hasattr(arg, "keys"):
                for k in arg:
                    self.setdefault(k, arg[k])
            else:
                for k, v in arg:
                    self.setdefault(k, v)
        for k, v in kwds.iteritems():
            self.setdefault(k, v)


def includeme(config):
    config.include("cornice")
    config.scan("trouvailles.views")


def main(global_config, **settings):
    settings = SettingsDict(settings)
    config = Configurator(settings={})
    settings.setdefaults(config.registry.settings)
    config.registry.settings = settings
    config.include(includeme)
    return config.make_wsgi_app()
