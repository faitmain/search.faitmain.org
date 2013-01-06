from pyramid.config import Configurator


def includeme(config):
    config.include("cornice")
    config.scan("trouvailles.views")


def main(global_config, **settings):
    config = get_configurator(global_config, **settings)
    config.include(includeme)
    return config.make_wsgi_app()
