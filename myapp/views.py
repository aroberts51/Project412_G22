from django.template.loader import get_template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User


def user_page(request):
    ######################################DATA TO BE SWAPPED
    games = [
        {'id': 1, 'name': 'Game 1'},
        {'id': 2, 'name': 'Game 2'},
        {'id': 3, 'name': 'Game 3'},
    ]
    ######################################DATA TO BE SWAPPED
    context = {
        'username': 'JohnDoe',  
        'email': 'johndoe@example.com',  
        'profile_picture': None,  
        'games': games,
    }
    try:
        template = get_template('myapp/user_page.html')  
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    
def edit_account(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        profile_picture = request.FILES.get('profile_picture', None)
        print(f"Updated account: Username={username}, Email={email}, Password={password}, Profile Picture={profile_picture}")
        return redirect('user_page')
    return render(request, 'myapp/edit_account.html')

def list_page(request):
    ######################################DATA TO BE SWAPPED
    following = [
        {
            'username': 'User1',
            'games': [
                {'name': 'Game A', 'genre': 'Action'},
                {'name': 'Game B', 'genre': 'Adventure'},
            ],
        },
        {
            'username': 'User2',
            'games': [
                {'name': 'Game X', 'genre': 'RPG'},
                {'name': 'Game Y', 'genre': 'Strategy'},
            ],
        },
    ]
    try:
        template = get_template('myapp/list_page.html')
        feed = [(user['username'], user['games']) for user in following]
        context = {'feed': feed}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
######################################DATA TO BE SWAPPED
FOLLOWERS = [
    {'name': 'UserA', 'is_following_back': True},
    {'name': 'UserB', 'is_following_back': False},
    {'name': 'UserC', 'is_following_back': False},
]
######################################DATA TO BE SWAPPED
FOLLOWING = ['User4', 'User5', 'User6']


def followers_page(request):
    try:
        query = request.GET.get('q', '').lower()
        filtered_followers = [f for f in FOLLOWERS if query in f['name'].lower()] if query else FOLLOWERS
        template = get_template('myapp/followers_page.html')
        context = {'followers': filtered_followers}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def following_page(request):
    try:
        query = request.GET.get('q', '').lower()
        filtered_following = [u for u in FOLLOWING if query in u.lower()] if query else FOLLOWING
        template = get_template('myapp/following_page.html')
        context = {'following': filtered_following}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def search_followers(request):
    query = request.GET.get('q', '').lower()
    filtered_followers = [f for f in FOLLOWERS if query in f['name'].lower()]
    return render(request, 'myapp/followers_page.html', {'followers': filtered_followers})


def search_following(request):
    query = request.GET.get('q', '').lower()
    filtered_following = [u for u in FOLLOWING if query in u.lower()]
    return render(request, 'myapp/following_page.html', {'following': filtered_following})


def unfollow_user(request, username):
    if request.method == 'POST':
        messages.success(request, f"You have unfollowed {username}.")
    return redirect('following')


def follow_back_user(request, username):
    if request.method == 'POST':
        messages.success(request, f"You are now following {username}.")
    return redirect('followers')

######################################DATA TO BE SWAPPED 
GAMES = [
        {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
        {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
        {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
    ]

def search_page(request):
    query = request.GET.get('q', '') 
    search_results = []
    if query:
        search_results = [game for game in GAMES if query.lower() in game['name'].lower()]
    context = {
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'myapp/search_page.html', context)

def signup_page(request):
    if request.method == 'POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'myapp/signup_page.html', {'error_message': 'Username or email already exists.'})
        User.objects.create_user(username=username, email=email,password=password)
        return redirect('login_page')
    return render(request, 'myapp/signup_page.html')
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====  

def login_page(request):
    ######################################DATA TO BE SWAPPED
    USERS = [
        {'username': 'user1', 'password': 'pass1'},
        {'username': 'user2', 'password': 'pass2'},
        {'username': 'user3', 'password': 'pass3'}
    ]
    if request.method == 'POST':
        queryUsername = request.POST.get('username')
        queryPassword = request.POST.get('password')
        user = None
        for userOne in USERS:
                if userOne['username'] == queryUsername and userOne['password'] == queryPassword:
                    user = userOne
                    break
        if(user):
            return redirect('user_page') 
        else:
            return render(request, 'myapp/login_page.html', {'error_message': 'Invalid username or password.'})       
    return render(request, 'myapp/login_page.html')

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====





# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def profile_page(request):
    return render(request, 'myapp/profile_page.html')


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====





def game_info_page(request, game_id):
    game = next((game for game in GAMES if game['id'] == game_id), None)
    
    if not game:
        raise Http404("Game not found")
    ######################################DATA TO BE SWAPPED
    context = {
        'game_title': game['name'],
        'description': game['description'],
        'release_date': game['release_date'],
    }
    return render(request, 'myapp/game_info_page.html', context)


#Mock user list (replace with database queries)
USER_GAME_LIST = []

def add_game_to_list(request):
    if request.method == "POST":
        game_id = int(request.POST.get('game_id', 0))
        ######################################DATA TO BE SWAPPED
        GAMES = [
            {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
            {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
            {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
        ]
        game = next((game for game in GAMES if game['id'] == game_id), None)
        if game and game not in USER_GAME_LIST:
            USER_GAME_LIST.append(game)
            messages.success(request, f"{game['name']} has been added to your list.")
        else:
            messages.error(request, "Game could not be added or is already in your list.")
    return redirect('search_page')
