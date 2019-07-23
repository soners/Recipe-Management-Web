from django.http import JsonResponse
from crescendo.management.connect import connect


def api_recipe(request, id):

    if not id:
        return JsonResponse({})

    else:
        command = """select id, name, details, description,
                     ingredients, ingredient_photos, 
                     cooking_steps, cooking_steps_photos,
                     tags, final_photos from recipe where id = {0}""".format(id)
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
                'description': recipe[3],
                'ingredients': recipe[4],
                'ingredient_photos': recipe[5],
                'cooking_steps': recipe[6],
                'cooking_steps_photos': recipe[7],
                'tags': recipe[8],
                'final_photos': recipe[9]
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
        command = """insert into users(name, email, password, delete_threshold) values('{0}', '{1}', '{2}', 90) returning id""".format(name, email, password)
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
    user_id = request.GET.get('user_id')

    if not name or not details or not user_id:
        return JsonResponse({'id': 0})

    name = name.replace("'", "''")
    details = details.replace("'", "''")

    db = connect()
    cursor = db.cursor()

    command = """insert into recipe(name, details) values('{0}', '{1}') returning id""".format(name, details)
    cursor.execute(command)
    recipe_id = cursor.fetchone()[0]
    db.commit()

    command = """insert into user2recipe(user_id, recipe_id) values({0}, {1})""".format(user_id, recipe_id)
    cursor.execute(command)
    db.commit()

    command = """select id, name, details from recipe where id = {0}""".format(recipe_id)
    cursor.execute(command)
    recipe = cursor.fetchone()

    return JsonResponse({
        'id': recipe[0],
        'name': recipe[1],
        'details': recipe[2]
    })


def api_add_details_recipe(request, id):

    description = request.GET.get('description')
    ingredients = request.GET.get('ingredients')
    ingredients_photos_list = request.GET.get('ingredients_photos')
    cooking_steps = request.GET.get('cooking_steps')
    cooking_steps_photos_list = request.GET.get('cooking_steps_photos')
    final_photos_list = request.GET.get('final_photos')
    """
    if not name or not description or not ingredients or not ingredients_photos_list or not cooking_steps or not cooking_steps_photos_list or not final_photos_list:
        return JsonResponse({'id': 0})
    """
    db = connect()
    cursor = db.cursor()

    command = """update recipe set details = '{0}' where id = {1}""".format(description, id)
    cursor.execute(command)
    db.commit()

    command = """update recipe set ingredients = '{0}' where id = {1}""".format(ingredients, id)
    cursor.execute(command)
    db.commit()

    command = """update recipe set cooking_steps = '{0}' where id = {1}""".format(cooking_steps, id)
    cursor.execute(command)
    db.commit()

    command = """update recipe set ingredient_photos = '{0}' where id = {1}""".format(ingredients_photos_list, id)
    cursor.execute(command)
    db.commit()

    command = """update recipe set cooking_steps_photos = '{0}' where id = {1}""".format(cooking_steps_photos_list, id)
    cursor.execute(command)
    db.commit()

    command = """update recipe set final_photos = '{0}' where id = {1}""".format(final_photos_list, id)
    cursor.execute(command)
    db.commit()


    return JsonResponse({'status': 'OK'})


def api_delete_recipe(request, id):

    db = connect()
    cursor = db.cursor()

    command = """delete from user2recipe where recipe_id = {0}""".format(id)
    cursor.execute(command)
    db.commit()

    command = """delete from recipe where id = {0}""".format(id)
    cursor.execute(command)
    db.commit()

    return JsonResponse({'status': 'OK'})

def api_save_threshold(request, id):

    threshold = request.GET.get('threshold')

    db = connect()
    cursor = db.cursor()

    command = """update users set delete_threshold  = {0} where id = {0}""".format(int(threshold), id)
    cursor.execute(command)
    db.commit()

    return JsonResponse({'status': 'OK'})


def api_get_threshold(request, id):

    db = connect()
    cursor = db.cursor()

    command = """select delete_threshold from users where id = {0}""".format(id)
    cursor.execute(command)
    db.commit()

    try:
        return JsonResponse({'threshold': db.fetchone()[0]})
    except:
        return JsonResponse({'threshold': 90})

