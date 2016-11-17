from django.http import Http404, HttpResponse

__all__ = ['csv2sql']

def superuser_required(view_func): #{{{1
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            # To enhance a security 404 instead of 403.
            raise Http404
        return view_func(request, *args, **kwargs)
    return wrapper

#}}}
#def csv2sql(request): {{{1
@superuser_required
def csv2sql(request):
    import csv
    from .models import Verb

    # Clear the table
    Verb.objects.all().delete()

    F = open('resources/irregular_verbs_table.csv')
    i = 0
    for row in csv.reader(F, delimiter=';'):
        Verb.objects.create(base_form=row[0], past_simple=row[1], past_participle=row[2])
        i += 1

    return HttpResponse('%d entries added successfully.' % i, content_type='text/plain')

#}}}
