# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from invitations.models import Invitation
from main.models import Point
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation, \
    ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import simplejson
from django.conf import settings
from django.core.validators import email_re
import uuid
from django.template import RequestContext

def sendInvitations(request):
    if request.method=="POST":
        if request.user.is_authenticated():
            if request.method=="POST":
                correos = request.POST['mails']
                listaCorreos = correos.split(',')
                user = request.user
                for correo in listaCorreos:
                    if not sendMail(correo.strip(), user):
                        break;
                return HttpResponseRedirect("/#sent")
            else:
                return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/login")
    elif request.is_ajax():
        user = request.user
        message = {'invitation_data': render_to_response("invite_dialog.html", {'remaining_invitations':user.profile.remaining_invitations},context_instance=RequestContext(request)).content}
        json = simplejson.dumps(message)
        return HttpResponse(json, mimetype='application/json')
        

def sendMail(email, user):
    if isValidEmail(email):
        if user.profile.remaining_invitations <= 0:
            return False
        token = uuid.uuid1().hex
        link = settings.WEB_URL + "/register?email=" + email + "&token=" + token + "&id="+ str(user.id)
        message = u'¡Nuestro usuario ' + user.first_name + u' ' + user.last_name + u' quiere trocar contigo! ¡Únete a esta gran comunidad que recicla e intercambia sin dinero! \n \n Sólo ingresa a \n' + link
        subject = user.first_name + u' te invitó Trueque'
#        send_mail( subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        print message
        inv = Invitation(id_sender=user, email=email, token=token, pending=True)
        inv.save()
        profile = user.profile
        profile.remaining_invitations = profile.remaining_invitations-1
        puntos = Point.objects.get(action="invitation_sent")
        profile.quds = profile.quds + puntos.qty
        profile.save()
        return True

def isValidEmail(email):
    return True if email_re.match(email) else False
