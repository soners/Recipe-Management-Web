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

IP = 'http://35.246.134.21'


class AboutView(TemplateView):
    template_name = 'index.html'


class LoginView(TemplateView):
    template_name = 'login.html'


def main(request):
    if data.user:
        return render(request, 'index.html', context={'id': data.user[0]})
    else:
        return render(request, 'index.html')


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
        data.logUser(user[0], user[1], user[2], csrf)
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

    d = []
    for x in rs:
        d.append({
            'id': x[0],
            'name': x[1],
            'details': x[2][:100] + '...'
        })
    print(d)

    return render(request, 'recipes.html', context={'recipes': d})


def add_recipe(request):

    return render(request, 'add_recipe.html')


def detail(request, id):

    command = """select * from recipe where id = {0}""".format(id)
    cursor.execute(command)
    recipe = cursor.fetchone()
    recipe_id = recipe[0]
    recipe_name = recipe[1]
    recipe_detail = recipe[2]
    url = '{0}/detail/{1}'.format(IP, recipe_id)

    return render(request, 'detail.html', context={'id': recipe_id, 'name': recipe_name, 'detail': recipe_detail, 'share': url})


def delete(request, id):
    command = "delete from user2recipe where recipe_id = {0}".format(id)
    cursor.execute(command)
    db.commit()

    command = "delete from recipe where id = {0}".format(id)
    cursor.execute(command)
    db.commit()

    return render(request, 'index.html', context={'id': data.user[0]})


def process_recipe(request):

    name = request.GET.get('recipe_name')
    details = request.GET.get('details')
    ingredients = request.GET.get('ingredients')
    steps = request.GET.get('cooking_steps')

    command = """insert into recipe(name, details) values('{0}', '{1}') returning id""".format(name, details)
    cursor.execute(command)
    db.commit()
    recipe_id = cursor.fetchone()[0]

    command = """insert into user2recipe(user_id, recipe_id) values({0}, {1})""".format(data.user[0], recipe_id)
    cursor.execute(command)
    db.commit()

    command = """select r.id, r.name, r.details from recipe r
                 left join user2recipe ur on ur.recipe_id = r.id
                 left join users u on ur.user_id = u.id"""

    cursor.execute(command)
    rs = cursor.fetchall()
    rs = rs if rs else []

    d = []
    for x in rs:
        d.append({
            'id': x[0],
            'name': x[1],
            'details': x[2]
        })
    print(d)

    return render(request, 'recipes.html', context={'recipes': d})


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
