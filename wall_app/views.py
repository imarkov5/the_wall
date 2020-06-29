from django.shortcuts import render, redirect
from django.contrib import messages
from log_reg_app.models import *


def wall(request):
    if 'name' in request.session:
        context = {
            'all_messages': Message.objects.order_by("-created_at"),
            'logged_user': User.objects.get(id=request.session['id'])
        }
        return render(request, 'wall_ajax.html', context)
    return redirect('../')

def logout(request):
    request.session.flush()
    return redirect('../')

def post_message(request):
    Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['id']))
    return redirect('/wall')

def post_message_ajax(request):
    message = Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['id']))
    context = {
            'message': message,
            'logged_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'message_snippet.html', context)

def post_comment(request, mess_id):
    Comment.objects.create(comment=request.POST['comment'], poster=User.objects.get(id=request.session['id']), message=Message.objects.get(id=mess_id))
    return redirect('/wall')

def post_comment_ajax(request):
    comment = Comment.objects.create(comment=request.POST['comment'], poster=User.objects.get(id=request.session['id']), message=Message.objects.get(id=request.POST['mess_id']))
    context = {
        'comment': comment
    }
    return render(request, 'comment_snippet.html', context)

def delete_message(request, mess_id):
    Message.objects.get(id=mess_id).delete()
    return redirect('/wall')

def edit_message(request, mess_id):
    context = {
        'message_to_edit': Message.objects.get(id=mess_id)
    }
    if request.method == 'POST':
        edited_message = Message.objects.get(id=mess_id)
        edited_message.message = request.POST['edited_message']
        edited_message.save()
        return redirect('/wall')
    return render(request, 'edit_message.html', context)

def like(request, mess_id):
    liked_message = Message.objects.get(id=mess_id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.like.add(user_liking)
    return redirect('/wall')

def unlike(request, mess_id):
    liked_message = Message.objects.get(id=mess_id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.like.remove(user_liking)
    return redirect('/wall')

def edit_profile(request):
    context ={
        'user': User.objects.get(id=request.session['id'])
    }
    if request.method == 'POST':
        errors = User.objects.profile_validator(request.POST, request.session['id'])
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wall/edit_profile')
        user = User.objects.get(id=request.session['id'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('/wall')
    return render(request, 'edit_profile.html', context)