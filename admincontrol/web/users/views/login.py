from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import View
import subprocess
from web.users.forms.login_form import LogInForm
from web.users.models import AeeUser


class LogInView(View):
    template_name = 'login.html'

    def get(self, request):

        command = "python /Users/omairshamshir/Documents/testing.py"
        pipe = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        result = pipe.stdout.read() # this is the output of the process


        return render(request, self.template_name, dict(login_form=LogInForm()))

    def post(self, request):
        response = None
        sign_in_form = LogInForm(request.POST)
        response_message = ''

        if sign_in_form.is_valid():
            username = sign_in_form.cleaned_data.get('username')
            password = sign_in_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                pass

            response = render(request, self.template_name, dict(msg=response_message, login_form=sign_in_form))

        return response
