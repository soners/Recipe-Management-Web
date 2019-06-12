from django.shortcuts import *
from django.http import HttpResponse
from django.views.generic import TemplateView
from django import forms
from crescendo.management.connect import connect
from django.http import HttpResponseNotFound
from crescendo.management.data import *

data = Data()
db = connect()
cursor = db.cursor()
logged = False

class AboutView(TemplateView):
    template_name = 'index.html'


class LoginView(TemplateView):
    template_name = 'login.html'


def signin(request):
    print(data.user)
    email = request.GET.get('email').replace("'", "''")
    password = request.GET.get('password').replace("'", "''")
    csrf = request.GET.get('csrfmiddlewaretoken')

    command = "select * from users where email = '{0}' and password = '{1}'".format(email, password)
    cursor.execute(command)
    user = cursor.fetchone()

    if not user:
        command = "select * from users where email = '{0}'".format(email)
        cursor.execute(command)
        user = cursor.fetchone()

        if user:
            return render(request, 'login.html', context={'status_message': 'Incorrect information'})
        else:
            return render(request, 'login.html', context={'status_message': 'User doesn\'t exist please sign up'})
    else:
        data.logUser(user[1], user[2], user[3])
        return render(request, 'index.html', context={'id': user[0]})


def signup(request):
    print(data.user)

    name = request.GET.get('name')
    email = request.GET.get('email')
    password = request.GET.get('password')

    if not name or not email or not password or len(name) == 0 or len(email) == 0 or len(password) == 0:
        return render(request, 'login.html', context={'status_message': 'Please enter information correctly'})

    name = name.replace("'", "''")
    email = email.replace("'", "''")
    password = password.replace("'", "''")

    csrf = request.GET.get('csrfmiddlewaretoken')

    command = "select * from users where email = '{0}'".format(email)
    cursor.execute(command)
    user = cursor.fetchone()
    if not user:
        command = "insert into users(name, email, password) values('{0}', '{1}', '{2}') returning id".format(name, email, password)
        cursor.execute(command)
        db.commit()
        return render(request, 'index.html', context={'id': cursor.fetchone()[0]})

    else:
        return render(request, 'login.html', context={'status_message': 'User already exists, please sign in'})


def recipes(request):
    print(data.user)
    command = """select * from recipe r
                 left join user2recipe ur on ur.recipe_id = r.id
                 left join users u on ur.user_id = u.id"""

    cursor.execute(command)
    rs = cursor.fetchall()

    return render(request, 'recipes.html', context={'recipes': rs if rs else []})


def add_recipe(request):

    return render(request, 'add_recipe.html')

def process_recipe(request):
    pass


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
