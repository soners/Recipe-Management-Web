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
        command = "insert into users(name, email, password, delete_threshold) values('{0}', '{1}', '{2}', 90) returning id".format(name, email, password)
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
    command = """insert into recipe(name) values('') returning id"""
    cursor.execute(command)
    recipe_id = cursor.fetchone()[0]
    return render(request, 'add_recipe.html', context={
        'id': recipe_id,
        'user_id': data.user[0]
    })


def detail(request, id):

    command = """select r.id, r.name, r.details, r.ingredients, r.ingredient_photos, 
                 r.cooking_steps, r.cooking_steps_photos, r.tags, r.final_photos 
                 from recipe r
                 where r.id = {0}""".format(id)
    cursor.execute(command)
    x = cursor.fetchone()

    if not x:
        return render(request, 'detail.html', context={'id': 0})

    url = '{0}/detail/{1}'.format(IP, x[0])

    firebase_url = 'https://firebasestorage.googleapis.com/v0/b/ccrescendo-ff945.appspot.com/o'
    if x[4]:
        lenn = len(x[4].split(','))
        ing_photos = ["{0}/{1}%2F{2}%2Fing_photo{3}.jpg?alt=media".format(firebase_url, data.user[0], x[0], (i+1)) for i in range(lenn)]
    else:
        ing_photos = []

    if x[6]:
        lenn = len(x[6].split(','))
        cook_photos = ["{0}/{1}%2F{2}%2Fcook_photo{3}.jpg?alt=media".format(firebase_url, data.user[0], x[0], (i+1)) for i in range(lenn)]
    else:
        cook_photos = []

    if x[8]:
        lenn = len(x[8].split(','))
        final_photos = ["{0}/{1}%2F{2}%2Ffinal_photo{3}.jpg?alt=media".format(firebase_url, data.user[0], x[0], (i+1)) for i in range(lenn)]
    else:
        final_photos = []


    d = {
        'id': x[0],
        'name': x[1],
        'details': x[2],
        'ingredients': x[3],
        'ing_photos': ing_photos,
        'cooking_steps': x[5],
        'cooking_steps_photos': cook_photos,
        'tags': x[7],
        'final_photos': final_photos,
        'share': url,
    }

    return render(request, 'detail.html', context=d)


def delete(request, id):
    command = "delete from user2recipe where recipe_id = {0}".format(id)
    cursor.execute(command)
    db.commit()

    command = "delete from recipe where id = {0}".format(id)
    cursor.execute(command)
    db.commit()

    return render(request, 'index.html', context={'id': data.user[0]})


def process_recipe(request):

    id = request.GET.get('id')
    name = request.GET.get('recipe_name')
    details = request.GET.get('details')
    ingredients = request.GET.get('ingredients')
    steps = request.GET.get('cooking_steps')
    tags = request.GET.get('tags')
    ingphotos = request.GET.get('ing_photo')
    cookphotos = request.GET.get('cook_photo')
    finalphotos = request.GET.get('final_photo')



    try:
        ing_photos_names = ','.join(["{0}/{1}/ing_photo{2}.jpg".format(data.user[0], id, i+1) for i in range(int(ingphotos))])
    except:
        ing_photos_names = None

    try:
        cook_photo_names = ','.join(["{0}/{1}/cook_photo{2}.jpg".format(data.user[0], id, i+1) for i in range(int(cookphotos))])
    except:
        cook_photo_names = None
    try:
        final_photo_names = ','.join(["{0}/{1}/final_photo{2}.jpg".format(data.user[0], id, i+1) for i in range(int(finalphotos))])
    except:
        final_photo_names = None


    command = """delete from recipe where id = {0}""".format(id)
    cursor.execute(command)
    db.commit()

    command = """insert into recipe(id, name, details, ingredients, ingredient_photos, cooking_steps, cooking_steps_photos, tags, final_photos) values({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')""".format(id, name, details, ingredients, ing_photos_names, steps, cook_photo_names, tags, final_photo_names)
    cursor.execute(command)

    command = """insert into user2recipe(user_id, recipe_id) values({0}, {1})""".format(data.user[0], id)
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


def profile(request):
    if not data.user:
        return render(request, 'index.html')

    command = """select delete_threshold from users where id = {0}""".format(data.user[0])
    cursor.execute(command)
    threshold = cursor.fetchone()[0]

    return render(request, 'profile.html', context={'threshold': threshold})


def save_threshold(request):

    threshold = request.GET.get('threshold')


    try:
        command = """update users set delete_threshold = {0} where id = {1}""".format(int(threshold), data.user[0])
        cursor.execute(command)
    except:
        return render(request, 'profile.html', context={'id': data.user[0], 'status_message': 'Please enter a number!'})

    return render(request, 'index.html', context={'id': data.user[0]})


def search_recipe(request):

    search = request.GET.get('search')
    print(search)

    db = connect()
    cursor = db.cursor()

    command = """select * from recipe where tags ilike '%{0}%' or
                                             description ilike '%{0}%' or
                                             details ilike '%{0}%' or
                                             cooking_steps ilike '%{0}%' or
                                             ingredients ilike '%{0}%'""".format(search)
    print(command)
    cursor.execute(command)
    recipes = cursor.fetchall()

    if not recipes:
        return render(request, 'recipes.html', {
            'recipes': []
        })
    else:
        data = []

        for recipe in recipes:
            data.append({
                'id': recipe[0],
                'name': recipe[1],
                'details': recipe[2],
            })

        return render(request, 'recipes.html', {
            'recipes': data
        })


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()


class SignupForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
