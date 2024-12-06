from django.template.loader import get_template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib import messages
from .models import Users, Game, Gameplayers, Userfollowers, Userfollowing
from django.db import IntegrityError
from django.contrib import messages

def user_page(request):
    username=request.session.get('username')
    if not username:
        return redirect('login_page')
    try:
        user = Users.objects.get(username=username)
        all_gameplayers = Gameplayers.objects.all()
        user_game_ids = [gp.gameid for gp in all_gameplayers if gp.username==username]
        all_games = Game.objects.all()
        user_games = [game for game in all_games if game.gameid in user_game_ids]
        context={
            'username':user.username,
            'email':user.useremail,
            'profile_picture':None,
            'games':user_games,
        }
        return render(request,'myapp/user_page.html', context)
    except Users.DoesNotExist:
        return redirect('login_page')
    except Exception as e:
        return HttpResponse(f"Error:{str(e)}")

    
def edit_account(request):
    username='JohnDoe'
    try:
        user=Users.objects.get(username=username)
        if request.method == 'POST':
            user.username=request.POST.get('username',user.username)
            user.useremail=request.POST.get('email',user.useremail)
            user.userpassword=request.POST.get('password',user.userpassword)
            user.save()
            messages.success(request,"Account information updated!")
            return redirect('user_page')
        context={
            'username':user.username,
            'email':user.useremail,
            'password':user.userpassword,
        }
        return render(request, 'myapp/edit_account.html',context)
    except user.DoesNotExist:
        return redirect('user_page')

def list_page(request):
    ######################################DATA TO BE SWAPPED
    #following = [
    #    {
    #        'username': 'User1',
    #        'games': [
    #            {'name': 'Game A', 'genre': 'Action'},
    #            {'name': 'Game B', 'genre': 'Adventure'},
    #        ],
    #    },
    #    {
    #        'username': 'User2',
    #        'games': [
    #            {'name': 'Game X', 'genre': 'RPG'},
    #            {'name': 'Game Y', 'genre': 'Strategy'},
    #        ],
    #    },
    #]
    try:
        following=Users.objects.all()
        feed=[(user.username,[]) for user in following]
        context={'feed':feed}
        return render(request,'myapp/list_page.html',context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
######################################DATA TO BE SWAPPED
#FOLLOWERS = [
#    {'name': 'UserA', 'is_following_back': True},
#    {'name': 'UserB', 'is_following_back': False},
#    {'name': 'UserC', 'is_following_back': False},
#]
######################################DATA TO BE SWAPPED
#FOLLOWING = ['User4', 'User5', 'User6']


def followers_page(request):
    try:
        username =request.session.get('username')
        if not username:
            return redirect('login_page')
        all_followers=Userfollowers.objects.select_related('followerusername')
        user_followers=[follower for follower in all_followers if follower.username.username==username]
        query=request.GET.get('q','').lower()
        if query:
            filtered_followers=[follower.followerusername for follower in user_followers if query in follower.followerusername.username.lower()]
        else:
            filtered_followers=[follower.followerusername for follower in user_followers]

        all_following=Userfollowing.objects.select_related('followingusername')
        following_usernames=[following.followingusername.username for following in all_following if following.username.username==username]
        for follower in filtered_followers:
            follower.is_following_back=follower.username in following_usernames
        return render(request,'myapp/followers_page.html',{'followers':filtered_followers})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def following_page(request):
    try:
        following=Users.objects.all()
        query=request.GET.get('q', '').lower()
        if query:
            filtered_following=[follow for follow in following if query in follow.username.lower()]
        else:
            filtered_following=following
        template = get_template('myapp/following_page.html')
        context = {'following': filtered_following}
        return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


def search_followers(request):
    
    query= request.GET.get('q', '').lower()
    followers=Users.objects.all()
    filtered_followers = [follower for follower in followers if query in follower.username.lower()]
    return render(request, 'myapp/followers_page.html', {'followers': filtered_followers})


def search_following(request):
    query=request.GET.get('q', '').lower()
    following=Users.objects.all()
    filtered_following = [follow for follow in following if query in follow.username.lower()]
    return render(request, 'myapp/following_page.html', {'following': filtered_following})


def unfollow_user(request, username):
    if request.method== 'POST':
        messages.success(request, f"You have unfollowed {username}.")
    return redirect('following')


def follow_back_user(request, username):
    if request.method== 'POST':
        messages.success(request, f"You are now following {username}.")
    return redirect('followers')

######################################DATA TO BE SWAPPED 
#GAMES = [
#        {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
#        {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
#        {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
#    ]

def search_page(request):
    username=request.session.get('username')
    if not username:
        return redirect('login_page')
    query = request.GET.get('q', '') 
    search_results=[]
    if query:
        all_games=Game.objects.all()  
        for game in all_games:
            if query.lower() in game.gamename.lower(): 
                search_results.append(game)
    else:
        search_results=Game.objects.all() 
 ##FIX THE ADD BUTTON 
    if request.method=="POST":
        game_id=request.POST.get('game_id')
        try:
            user=Users.objects.get(username=username)
            game=Game.objects.get(gameid=game_id)
            Gameplayers.objects.create(user,game)
            messages.success(request, f"'{game.gamename}' has been added to your list.")
        except IntegrityError:
            messages.error(request,"Already in your list!")
        except Game.DoesNotExist:
            messages.error(request,"Game does not exist.")
        except Exception as e:
            messages.error(request,f"An unexpected error occurred: {str(e)}")

    context={
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'myapp/search_page.html', context)

def signup_page(request):
    if request.method == 'POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        all_users=Users.objects.all()
        username_exists=any(user.username == username for user in all_users)
        email_exists=any(user.useremail == email for user in all_users)
        
        if username_exists or email_exists:
            return render(request,'myapp/signup_page.html', {'error_message': 'Username or email already exists.'})
        #hash pass made too long
        #hash_password = make_password(password)
        Users.objects.create(username=username, useremail=email, userpassword=password)
        return redirect('login_page')
    return render(request,'myapp/signup_page.html')
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====  

def login_page(request):
    ######################################DATA TO BE SWAPPED
    #USERS = [
    #    {'username': 'user1', 'password': 'pass1'},
    #    {'username': 'user2', 'password': 'pass2'},
    #    {'username': 'user3', 'password': 'pass3'}
    #]
    if request.method=='POST':
        queryUsername=request.POST.get('username', '').strip()
        queryPassword=request.POST.get('password', '').strip()
        try:
            user=Users.objects.get(username=queryUsername)
            if user.userpassword==queryPassword:  
                request.session['username']=user.username
                return redirect('user_page')  
            else:
                return render(request, 'myapp/login_page.html', {'error_message': 'Invalid username or password.'})
        except Users.DoesNotExist:
            return render(request, 'myapp/login_page.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'myapp/login_page.html')
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====





# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def profile_page(request):
    return render(request, 'myapp/profile_page.html')


# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====





def game_info_page(request, game_id):
    #username=request.session.get('username')
    try:
        game=Game.objects.get(gameid=game_id)
        
        if not game:
            raise Http404("Game not found")
        ######################################DATA TO BE SWAPPED
        context = {
            'game_title': game.gamename,
            'description': game.summary,
            'release_date': game.releasedate,
        }
        return render(request, 'myapp/game_info_page.html', context)
    except Game.DoesNotExist:
        raise Http404("Game not found")


#Mock user list (replace with database queries)
#USER_GAME_LIST = []

def add_game_to_list(request):
    if request.method == "POST":
        game_id = int(request.POST.get('game_id', 0))
        ######################################DATA TO BE SWAPPED
        #GAMES = [
        #    {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
        #    {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
        #    {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
        #]
        try:
            game=Game.objects.get(gameid=game_id)
            Gameplayers.objects.create(username=request.user.username, gameid=game)
            messages.success(request,f"{game.gamename} has been added successfully to your list.")
        except Game.DoesNotExist:
            messages.error(request, "Failed to add game.")
    return redirect('search_page')
