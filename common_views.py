from django.http import HttpResponse

__all__ = ('whoami', 'stats', 'clear_stats')


def whoami(request): #{{{1
    """Return current user."""
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = 'AnonymousUser'

    return HttpResponse('You are logged as "%s".' % username)

#}}}
def stats(request): #{{{1
    yes = request.session.get('YES', 0)
    no = request.session.get('NO', 0)

    return HttpResponse('YES: %d, NO: %d\n' % (yes, no), content_type='text/plain')

#}}}
def clear_stats(request): #{{{1
    request.session.flush()
    return HttpResponse('session has been flushed.', content_type='text/plain')

#}}}
