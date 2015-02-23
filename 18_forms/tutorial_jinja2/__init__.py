from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    config = Configurator(settings=settings,
                          session_factory=my_session_factory)
    config.include('pyramid_jinja2')
    ###
    config.add_route('wiki_view', '/')
    config.add_route('wikipage_add', '/wiki/add')
    config.add_route('wikipage_view', '/wiki/{uid}')
    config.add_route('wikipage_edit', '/wiki/{uid}/edit')
    config.add_static_view('deform_static', 'deform:static/')
    ###
    config.add_route('home', '/home')
    config.add_route('hello', '/howdy/{first}/{last}')
    config.add_route('hello_json', 'howdy.json')
    config.add_static_view(name='static', path='tutorial:static')    
    config.scan('.views')
    return config.make_wsgi_app()