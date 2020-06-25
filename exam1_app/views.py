from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'login.html')

def register(request):
    print(request.POST)
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        safe_pw = bcrypt.hashpw(request.POST['registration_password'].encode(), bcrypt.gensalt()).decode()
        print(safe_pw)

        new_user = User.objects.create(first_name = request.POST['registration_first_name'], last_name = request.POST['registration_last_name'], email = request.POST['registration_email'], password = safe_pw)
        request.session['user_id'] = new_user.id
        return redirect('/quotes')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = User.objects.get(email = request.POST['login_email'])
        request.session['user_id'] = logged_user.id
        print(logged_user.id)
        print('***************')
        return redirect('/quotes')

def quotes(request):
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'all_posts' : Post.objects.all()
    }
    return render(request, 'quotes_main.html', context)

def delete_post(request, postid):
    destroy_post = Post.objects.get(id= postid).delete()
    return redirect('/quotes')

def add_like (request, postid):
    user_obj = User.objects.get(id = request.session['user_id'])
    post_obj = Post.objects.get(id = postid)
    new_like = user_obj.posts_liked.add(post_obj)     
    return redirect('/quotes')
        
def add_quote(request):
    errors = Post.objects.post_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        Post.objects.create(author = request.POST['quote_author'], quote = request.POST['quote_quote'], poster = User.objects.get(id = request.session['user_id']))
        return redirect('/quotes')

def edit_account(request, userid):
    
    account_edit = User.objects.get(id = userid)
    context = {
        'account_edit' : account_edit
    }
    return render (request, 'edit.html', context)

def update_account(request, userid):
    print('************************************************')
    print(request.POST)
    errors = User.objects.edit_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/myaccount/{userid}')
    else:
        update = User.objects.get(id = userid)
        update.first_name = request.POST['index_first_name'] 
        update.last_name = request.POST['index_last_name']
        update.email = request.POST['index_email']
        update.save()
        return redirect('/quotes')

def user_quotes(request, userid):
    user_obj = User.objects.get(id = userid)
    user_likes = user_obj.posts_liked.all()
    context = {
        'user_obj' : user_obj,
        'user_likes' : user_likes
    }
    return render(request, 'user.html', context)





def logout(request):
    request.session.clear
    return redirect('/')

# Create your views here.
