from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder
#from pyramid.session import SignedCookieSessionFactory

from sqlalchemy import engine_from_config

from .models import DBSession, Base

def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    """
    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
        
    config = Configurator(settings=settings,
                          session_factory=my_session_factory,
                          root_factory='tutorial.models.Root')
    """
    
    config = Configurator(settings=settings,
                          root_factory='tutorial.models.Root')
    config.include('pyramid_chameleon')

    # Security policies
    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_route('wiki_view', '/')
    config.add_route('hello', '/howdy')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('wikipage_add', '/add')
    config.add_route('wikipage_view', '/{uid}')
    config.add_route('wikipage_edit', '/{uid}/edit')
    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()