from django.http import JsonResponse
from crescendo.management.connect import connect


def api_recipe(request, id):

    if not id:
        return JsonResponse({})

    else:
        command = """select * from recipe where id = {0}""".format(id)
        db = connect()
        cursor = db.cursor()
        cursor.execute(command)
        recipe = cursor.fetchone()

        print(recipe)

        if not recipe:
            return JsonResponse({})
        else:
            return JsonResponse({
                'id': recipe[0],
                'name': recipe[1],
                'detail': recipe[2],
            })


def api_recipes(request, id):

    if not id:
        return JsonResponse({
            'recipes': []
        })
    else:
        command = """select r.id, r.name, r.details from recipe r
                     left join user2recipe ur on ur.recipe_id = r.id
                     left join users u on ur.user_id = u.id
                     where u.id = {0}""".format(id)
        db = connect()
        cursor = db.cursor()
        cursor.execute(command)
        recipes = cursor.fetchall()

        if not recipes:
            return JsonResponse({
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

            return JsonResponse({
                'recipes': data
            })


def api_login(request):

    email = request.GET.get('email')
    password = request.GET.get('password')

    if not email or not password:
        return JsonResponse({
            'id': 0,
            'status': 'Please enter information correctly'
        })

    email = email.replace("'", "''")
    password = password.replace("'", "''")

    db = connect()
    cursor = db.cursor()

    command = """select id, name, email from users where email = '{0}' and password = '{1}'""".format(email, password)
    cursor.execute(command)
    user = cursor.fetchone()

    if not user:
        return JsonResponse({
            'id': 0,
            'status': 'Please enter information correctly'
        })
    else:
        return JsonResponse({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })


def api_signup(request):

    name = request.GET.get('name')
    email = request.GET.get('email')
    password = request.GET.get('password')

    if not email or not password or not name:
        return JsonResponse({
            'id': 0,
            'status': 'Please enter information correctly'
        })

    name = name.replace("'", "''")
    email = email.replace("'", "''")
    password = password.replace("'", "''")

    db = connect()
    cursor = db.cursor()

    command = """select * from users where email = '{0}'""".format(email)
    cursor.execute(command)
    prev = cursor.fetchone()

    if prev:
        return JsonResponse({
            'id': 0,
            'status': 'User already exists, please sign in'
        })

    else:
        command = """insert into users(name, email, password) values('{0}', '{1}', '{2}') returning id""".format(name, email, password)
        cursor.execute(command)
        db.commit()
        user_id = cursor.fetchone()

        command = """select id, name, email from users where id = {0}""".format(user_id[0])
        cursor.execute(command)
        user = cursor.fetchone()

        return JsonResponse({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })


def api_add_recipe(request):

    name = request.GET.get('name')
    details = request.GET.get('details')

    if not name or not details:
        return JsonResponse({'id': 0})

    name = name.replace("'", "''")
    details = details.replace("'", "''")

    db = connect()
    cursor = db.cursor()

    command = """insert into recipe(name, details) values('{0}', '{1}') returning id""".format(name, details)
    cursor.execute(command)
    recipe_id = cursor.fetchone()[0]
    db.commit()

    command = """select id, name, details from recipe where id = {0}""".format(recipe_id)
    cursor.execute(command)
    recipe = cursor.fetchone()

    return JsonResponse({
        'id': recipe[0],
        'name': recipe[1],
        'details': recipe[2]
    })


def api_delete_recipe(request, id):

    db = connect()
    cursor = db.cursor()

    command = """delete from recipe where id = {0}""".format(id)
    cursor.execute(command)
    db.commit()

    return JsonResponse({'status': 'OK'})

