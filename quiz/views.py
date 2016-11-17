#Imports {{{1
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest,\
    HttpResponseServerError, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import Verb

#}}}
#Variables {{{1
__all__ = ['main', 'verb']

verb_forms = {
    '1': 'base_form',
    '2': 'past_simple',
    '3': 'past_participle'
}

#}}}
def main(request): #{{{1
    if request.method == 'GET':
        from random import randint

        if 'verbs' not in request.session:
            request.session['verbs'] = {
                'base_form': [],
                'past_simple': [],
                'past_participle': []
            }
            Vs = Verb.objects.all()
            for V in Vs:
                request.session['verbs']['base_form'].append(V.base_form)
                request.session['verbs']['past_simple'].append(V.past_simple)
                request.session['verbs']['past_participle'].append(V.past_participle)

        verb_form = 'base_form' # default form
        get_keys = request.GET.keys()
        if not get_keys:
            pass # default is taken
        else:
            key = get_keys[-1]
            if key in ('1', '2', '3'):
                verb_form = verb_forms[key]
            else:
                message = 'Bad GET, url: {}; GET must be "1", "2" or "3".\n'.format(
                    request.build_absolute_uri())
                return HttpResponseBadRequest(message)
        verbs = request.session['verbs'][verb_form]
        try:
            verb = verbs.pop(randint(0, len(verbs)-1))
        except IndexError:
            return HttpResponseNotFound('%s verbs have been exhausted!\n' % verb_form)
        request.session.modified = True

        return HttpResponse('%s\n' % verb, content_type='text/plain')

    else:
        return HttpResponseNotAllowed(['GET'])

#}}}
#def verb(request): {{{1
@csrf_exempt
def verb(request, verb):
    if request.method == 'POST':
        verb_form_question = 'base_form' # default
        verb_form_answer = 'past_simple' # default
        error_msg = 'Bad GET, url: {}; GET format must be "[1-3],[1-3]", e.g "1,2".\n'.format(
            request.build_absolute_uri())

        get_keys = request.GET.keys()
        if not get_keys:
            pass # default is taken
        else:
            key = get_keys[-1]
            if ',' not in key:
                return HttpResponseBadRequest(error_msg)
            key1, key2 = key.split(',', 1)
            if key1 in ('1', '2', '3'):
                verb_form_question = verb_forms[key1]
            else:
                return HttpResponseBadRequest(error_msg)
            if key2 in ('1', '2', '3'):
                verb_form_answer = verb_forms[key2]
            else:
                return HttpResponseBadRequest(error_msg)

        if verb_form_answer == verb_form_question:
            error_msg = 'Verb forms must be different; url: {}.\n'.format(
                request.build_absolute_uri())
            return HttpResponseBadRequest(error_msg)

        if verb_form_question == 'base_form':
            try:
                verb_obj = Verb.objects.get(pk=verb)
            except ObjectDoesNotExist:
                return HttpResponseNotFound('Verb "%s" not found as base form.\n' % verb)
        elif verb_form_question == 'past_simple':
            try:
                verb_obj = Verb.objects.filter(past_simple=verb).get()
            except ObjectDoesNotExist:
                return HttpResponseNotFound('Verb "%s" not found as past simple.\n' % verb)
        elif verb_form_question == 'past_participle':
            try:
                verb_obj = Verb.objects.filter(past_participle=verb).get()
            except ObjectDoesNotExist:
                return HttpResponseNotFound('Verb "%s" not found as past participle.\n' % verb)
        else:
            return HttpResponseServerError('Wrong verb_form_question')
        
        right_answer = getattr(verb_obj, verb_form_answer)

        answer = request.POST.keys()[-1]

        response = 'NO'
        if answer == right_answer: # first, because right answer may be like "was,were"
            response = 'YES'
        elif ',' in right_answer:
            if answer in right_answer.split(','):
                response = 'YES'

        # Session
        try:
            request.session[response] += 1
        except KeyError:
            request.session[response] = 1

        return HttpResponse(response+'\n', content_type='text/plain')

    else:
        return HttpResponseNotAllowed(['POST'])

#}}}
