from django.template.loader import get_template
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import redirect
from django.contrib import messages
from .models import Users, Game
from django.db import connection
from django.http import HttpResponse
from django.contrib import messages


def user_page(request):
    username=request.session.get('username')
    if not username:
        return redirect('login_page')
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT g.gameid, g.gamename, ge.genrename
                FROM gameplayers gp
                JOIN game g ON gp.gameid= g.gameid
                LEFT JOIN gamegenres gg ON gg.gameid = g.gameid
                LEFT JOIN genres ge ON gg.genreid = ge.genreid
                WHERE gp.username= %s
            """, [username]) 
            user_games=cursor.fetchall()
        games=[{'gameid': game[0], 'gamename': game[1], 'genre': game[2]} for game in user_games]
        user=Users.objects.get(username=username)
        context={
            'username':user.username,
            'email':user.useremail,
            'profile_picture':None,
            'games':games,
        }
        return render(request,'myapp/user_page.html', context)
    except Users.DoesNotExist:
        return redirect('login_page')
    except Exception as e:
        return HttpResponse(f"Error:{str(e)}")

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
#NOT FUNCTIONAL DUE TO FOREIGN KEY OCNFLICT, NEED CASCADE
def edit_account(request):
    print("edit_account view called")
    username=request.session.get('username')
    with connection.cursor() as cursor:
        cursor.execute("""SELECT username, useremail,userpassword FROM users WHERE username= %s""", [username])
        user=cursor.fetchone()
    if not user:
        messages.error(request,"User not found.")
        return redirect('user_page')
    if request.method=='POST':
        messages.info(request,"This feature is under maintenance. Please try again later.")
        return redirect('edit_account')
    context={
        'username': user[0],
        'email': user[1],
        'password': user[2],
    }
    return render(request, 'myapp/edit_account.html', context)

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
        feed=[]
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users")
            users=cursor.fetchall()
            for user in users:
                username=user[0]
                cursor.execute("""
                    SELECT g.gameid, g.gamename, STRING_AGG(genres.genrename, ', ') AS genres
                    FROM gameplayers gp
                    JOIN game g ON gp.gameid = g.gameid
                    LEFT JOIN gamegenres gg ON g.gameid = gg.gameid
                    LEFT JOIN genres ON gg.genreid = genres.genreid
                    WHERE gp.username = %s
                    GROUP BY g.gameid, g.gamename
                """, [username])
                games=cursor.fetchall()
                game_list=[{'id': game[0],'name': game[1],'genre': game[2]} for game in games]
                feed.append((username,game_list))
        context={'feed':feed}
        return render(request, 'myapp/list_page.html',context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

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
        username=request.session.get('username')
        with connection.cursor() as cursor:
            cursor.execute("""SELECT f.followerusername, u.username FROM userfollowers f JOIN users u ON f.followerusername=u.username WHERE f.username = %s""", [username])
            user_followers=cursor.fetchall()
            query=request.GET.get('q', '').lower()
            filtered_followers=[follower for follower in user_followers if query in follower[1].lower()] if query else user_followers
            cursor.execute("""SELECT f.followingusername, u.username FROM userfollowing f JOIN users u ON f.followingusername=u.username WHERE f.username = %s""", [username])
            following_usernames=[following[1] for following in cursor.fetchall()]
            for follower in filtered_followers:
                follower.is_following_back=follower[1] in following_usernames
            return render(request,'myapp/followers_page.html',{'followers': filtered_followers})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def following_page(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT username FROM users""")
            following=cursor.fetchall()
            query=request.GET.get('q', '').lower()
            filtered_following=[follow for follow in following if query in follow[0].lower()] if query else following
        context={'following': filtered_following}
        return render(request,'myapp/following_page.html',context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
 
def search_followers(request):
    
    query= request.GET.get('q', '').lower()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT username FROM users WHERE username ILIKE %s""", ['%' + query + '%'])
        filtered_followers=cursor.fetchall()
    return render(request,'myapp/followers_page.html',{'followers':[{'username': follower[0]} for follower in filtered_followers]})
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def search_following(request):
    query=request.GET.get('q', '').lower()
    with connection.cursor() as cursor:
        cursor.execute("""SELECT username FROM users WHERE username ILIKE %s""", ['%' + query + '%'])
        filtered_following=cursor.fetchall()
    return render(request,'myapp/following_page.html',{'following':[{'username': follow[0]} for follow in filtered_following]})
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====


def unfollow_user(request, username):
    if request.method=='POST':
        current_user=request.session.get('username')
        if not current_user:
            return redirect('login_page')
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM userfollowing WHERE username=%s AND followingusername= %s""", [current_user, username])
        messages.success(request,f"You have unfollowed {username}.")
    return redirect('following')

# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def follow_back_user(request, username):
    if request.method== 'POST':
        current_user=request.session.get('username')
        if not current_user:
            return redirect('login_page')
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO userfollowing (username, followingusername) VALUES (%s, %s)""", [current_user, username])
        messages.success(request, f"You are now following {username}.")
    return redirect('followers')
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

######################################DATA TO BE SWAPPED 
#GAMES = [
#        {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
#        {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
#        {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
#    ]

def search_page(request):
   # username1 = request.session.get('username')
   # if not username1:
    #    return redirect('login_page')
    query=request.GET.get('q', '') 
    search_results=[]
    with connection.cursor() as cursor:
        if query:
            cursor.execute("""SELECT gameid,gamename FROM game WHERE gamename ILIKE %s """, ['%' + query + '%'])
            games=cursor.fetchall()
            for game in games:
                search_results.append({'gameid': game[0],'gamename': game[1]})
        else:
            cursor.execute("SELECT gameid,gamename FROM game")
            games = cursor.fetchall()
            for game in games:
                search_results.append({'gameid':game[0],'gamename':game[1]})

    context = {
        'query': query,
        'search_results': search_results,
    }
    return render(request,'myapp/search_page.html', context)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def signup_page(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        with connection.cursor() as cursor:
            cursor.execute("""SELECT username,useremail FROM users WHERE username =%s OR useremail = %s """, [username,email])
            existing_user =cursor.fetchone()
        if existing_user:
            return render(request, 'myapp/signup_page.html',{'error_message':'Username or email already exists.'})
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO users (username,useremail,userpassword) VALUES (%s, %s, %s) """, [username, email, password])
        return redirect('login_page')   
    return render(request, 'myapp/signup_page.html')
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
        with connection.cursor() as cursor:
            cursor.execute("""SELECT username, userpassword FROM users WHERE username = %s AND userpassword = %s """, [queryUsername, queryPassword])
            user = cursor.fetchone()
        if user:
            request.session['username'] = user[0]
            return redirect('user_page')  
        else:
            return render(request, 'myapp/login_page.html', {'error_message': 'Invalid username or password.'})
    return render(request, 'myapp/login_page.html')
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====

def profile_page(request, username):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT username FROM users WHERE username = %s", [username])
            user=cursor.fetchone()
            if not user:
                return HttpResponse("User not found",status=404)
        with connection.cursor() as cursor:
            cursor.execute("""SELECT g.gameid, g.gamename FROM gameplayers gp JOIN game g ON gp.gameid = g.gameid WHERE gp.username = %s""", [username])
            games=cursor.fetchall()
        games_list=[{'id': game[0], 'name':game[1]} for game in games]
        context={
            'profile_picture': None, 
            'username': username,
            'games': games_list,
        }
        return render(request, 'myapp/profile_page.html',context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}",status=500)
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
def game_info_page(request, game_id):
    #username=request.session.get('username')
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT gamename, summary, releasedate FROM game WHERE gameid = %s """, [game_id])
            game = cursor.fetchone()
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
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
#Mock user list (replace with database queries)
#USER_GAME_LIST = []
def add_game_to_list(request):
        ######################################DATA TO BE SWAPPED
        #GAMES = [
        #    {'id': 1, 'name': 'Game A', 'genre': 'Action', 'description': 'An action-packed game!', 'release_date': '2023-05-01'},
        #    {'id': 2, 'name': 'Game B', 'genre': 'Adventure', 'description': 'Explore vast lands!', 'release_date': '2022-11-15'},
        #    {'id': 3, 'name': 'Game C', 'genre': 'RPG', 'description': 'Role-playing at its finest.', 'release_date': '2024-01-20'},
        #]
    if request.method=="POST":
        game_id=request.POST.get('game_id')
        username=request.session.get('username')
        if not username:
            return redirect('login_page')
        with connection.cursor() as cursor:
            cursor.execute("""SELECT username FROM users WHERE username = %s""", [username])
            user=cursor.fetchone()
            if user:
                cursor.execute("""SELECT gameid FROM gameplayers WHERE username = %s AND gameid = %s""", [username, game_id])
                existing_game = cursor.fetchone()
                if existing_game:
                    messages.warning(request, f"Game is already in your list.")
                else:
                    cursor.execute("""INSERT INTO gameplayers (username, gameid) VALUES (%s, %s)""", [username, game_id])
                    messages.success(request, "Game has been added successfully to your list.")
            else:
                messages.error(request, "User session error. Please log in again.")
    return redirect('search_page')

def delete_game(request):
    if request.method=="POST":
        game_id=request.POST.get("game_id")
        username=request.session.get("username")
        try:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT gameid FROM gameplayers WHERE username=%s AND gameid= %s""",[username,game_id])
                existing_game=cursor.fetchone()
                if existing_game:
                    cursor.execute("""DELETE FROM gameplayers WHERE username =%s AND gameid=%s""",[username,game_id])
                    messages.success(request, "Game has been deleted successfully from your list.")
                else:
                    messages.error(request, "Game could not be deleted from your list.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('user_page')