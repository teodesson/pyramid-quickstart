import colander
import deform.widget

import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(route_name='hello')
class TutorialViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'TutorialViews'
        
    @property
    def counter(self):
        session = self.request.session
        if 'counter' in session:
            session['counter'] += 1
        else:
            session['counter'] = 1

        return session['counter']

    @property
    def full_name(self):
        first = self.request.matchdict['first']
        last = self.request.matchdict['last']
        return first + ' ' + last

    @view_config(route_name='home', renderer='home.jinja2')
    def home(self):
        log.debug('In home view')
        return {'page_title': 'Home View'}

    # Retrieving /howdy/first/last the first time
    @view_config(renderer='hello.jinja2')
    @view_config(route_name='hello_json', renderer='json')
    def hello(self):
        log.debug('In hello view')
        return {'page_title': 'Hello View'}

    # Posting to /howdy/first/last via the "Edit" submit button
    @view_config(request_method='POST', renderer='edit.jinja2')
    def edit(self):
        new_name = self.request.params['new_name']
        return {'page_title': 'Edit View', 'new_name': new_name}

    # Posting to /howdy/first/last via the "Delete" submit button
    @view_config(request_method='POST', request_param='form.delete',
                 renderer='delete.jinja2')
    def delete(self):
        print ('Deleted')
        return {'page_title': 'Delete View'}
        
        
pages = {
    '100': dict(uid='100', title='Page 100', body='<em>100</em>'),
    '101': dict(uid='101', title='Page 101', body='<em>101</em>'),
    '102': dict(uid='102', title='Page 102', body='<em>102</em>')
}

class WikiPage(colander.MappingSchema):
    title = colander.SchemaNode(colander.String())
    body = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.RichTextWidget()
    )


class WikiViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def wiki_form(self):
        schema = WikiPage()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.wiki_form.get_widget_resources()

    @view_config(route_name='wiki_view', renderer='wiki_view.jinja2')
    def wiki_view(self):
        return dict(pages=pages.values())

    @view_config(route_name='wikipage_add',
                 renderer='wikipage_addedit.jinja2')
    def wikipage_add(self):
        form = self.wiki_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.wiki_form.validate(controls)
            except deform.ValidationFailure as e:
                # Form is NOT valid
                return dict(form=e.render())

            # Form is valid, make a new identifier and add to list
            last_uid = int(sorted(pages.keys())[-1])
            new_uid = str(last_uid + 1)
            pages[new_uid] = dict(
                uid=new_uid, title=appstruct['title'],
                body=appstruct['body']
            )

            # Now visit new page
            url = self.request.route_url('wikipage_view', uid=new_uid)
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='wikipage_view', renderer='wikipage_view.jinja2')
    def wikipage_view(self):
        uid = self.request.matchdict['uid']
        page = pages[uid]
        return dict(page=page)

    @view_config(route_name='wikipage_edit',
                 renderer='wikipage_addedit.jinja2')
    def wikipage_edit(self):
        uid = self.request.matchdict['uid']
        page = pages[uid]

        wiki_form = self.wiki_form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = wiki_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(page=page, form=e.render())

            # Change the content and redirect to the view
            page['title'] = appstruct['title']
            page['body'] = appstruct['body']

            url = self.request.route_url('wikipage_view',
                                         uid=page['uid'])
            return HTTPFound(url)

        form = wiki_form.render(page)

        return dict(page=page, form=form)