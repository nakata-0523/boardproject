from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError  #登録ユーザー重複
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.

def signupfunc(request):#ユーザーの新規作成
    #object_list = User.objects.all() #Userというmodelの情報全てを取得
    # object = User.objects.get(username='nakataseiichirou') #Userというmodelのusername=seiの情報取得
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.create_user(username, '', password)#新規ユーザーの登録
            return redirect('login')

        except IntegrityError: #登録ユーザーの重複
            return render(request, 'signup.html', {'error':'このユーザーはすでに登録されています。'})

    return render(request, 'signup.html', {})

def loginfunc(request):
    if request.method == "POST":#リクエストの判定
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:#ログイン成功
            login(request, user)
            return redirect('list')
        else:#ログイン失敗
            return render(request, 'login.html', {})
    return render(request, 'login.html', {})#リクエストがGETの時

@login_required #ログイン状態の管理
def listfunc(request):
    object_list = BoardModel.objects.all()
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request): #ログアウト機能
    logout(request)
    return redirect('login')

def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk) #データがあれば取得し、なければ404エラーを表示する
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save() #変更の保存
    return redirect('list')

def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    
    if username in object.readtext:
        return redirect('list')
    else:
        object.read = object.read + 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('list')
    
class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'sns_image')
    success_url = reverse_lazy('list')