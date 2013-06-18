# -*- coding: utf-8 -*-
from usuarios.models import Usuario
from invitations.models import Invitation
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation, \
    ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import simplejson
from django.conf import settings
from usuarios.views import is_loged
from django.core.validators import email_re
import uuid
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def sendInvitations(request):
    if is_loged(request):
        if request.method=="POST":
            correos = request.POST['mails']
            listaCorreos = correos.split(',')
            user = Usuario.objects.get(id_usuario=request.session['member_id'])
            for correo in listaCorreos:
                if not sendMail(correo.strip(), user):
                    break;
            return HttpResponseRedirect("#sent")
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/login")

def sendMail(email, user):
    print email
    if isValidEmail(email):
        if user.remaining_invitations <= 0:
            return False
        token = uuid.uuid1().hex
        link = settings.WEB_URL + "/register?email=" + email + "&token=" + token + "&id="+ str(user.id_usuario)
        message = u'¡Nuestro usuario ' + user.first_name + u' ' + user.last_name + u' quiere trocar contigo! ¡Únete a esta gran comunidad que recicla e intercambia sin dinero! \n \n Sólo ingresa a \n' + link
        subject = user.first_name + u' te invitó Trueque'
        send_mail( subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        inv = Invitation(id_sender=user, email=email, token=token, pending=True)
        inv.save()
        user.remaining_invitations = user.remaining_invitations-1
        user.save()
        return True

def isValidEmail(email):
    return True if email_re.match(email) else False
