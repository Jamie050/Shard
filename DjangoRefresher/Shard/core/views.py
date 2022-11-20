from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Post,User,Profile,Comment,ProfileFollowing
from .forms import MyUserCreationForm,PostForm,LoginForm,ProfileForm,CommentForm
# Create your views here.

#home page

def home(request):
    posts = Post.objects.all()
    form = PostForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST,files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
            return redirect('home')
        else:
            return HttpResponse("Error Dumbass")

    context = {'posts':posts,
               'form':form}
    return render(request,'core.html',context)

#registration and signup functions

def register(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Error Dumbass")

    context = {'form': form}
    return render(request,'register.html',context)


def loginUser(request):
    
    form = LoginForm()
    context = {'form':form}    
    if request.method == 'POST':
      form = LoginForm(request, data=request.POST)
      if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

      try:
           user = User.objects.get(username=username)

      except:
           return HttpResponse("Username does not exist")


      user = authenticate(request,username=username,password=password)

      if user is not None:
           login(request,user)
           return redirect('home')

      else:
           return HttpResponse("password is incorrect")

    return render(request,'login.html',context)

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('home')


#post crud

@login_required(login_url='/login')
def editPost(request,pk):
    post = Post.objects.get(id=pk)

    if request.user.id != post.author.id:
        return redirect('home')

    form = PostForm(instance=post)
    context={'form':form}
    if request.method == 'POST':
            form = PostForm(request.POST,instance=post)
            if form.is_valid():
                post = form.save(commit=True)
                return redirect('home')
            else:
                return HttpResponse("error")

    return render(request,'edit-post.html',context)

@login_required(login_url='/login')
def deletePost(request,pk):
    post = Post.objects.get(id=pk)
    if request.user.id == post.author.id:
      post.delete()
    else:
        return HttpResponse("You are not authorised to do this")

    return redirect('home')

#post comments
def commentSection(request,pk):
    post = Post.objects.get(id=pk)
    post_comments = post.comment_set.all()
    commentors = post.commentors.all()
    form = CommentForm()
    context = {'comments':post_comments,
               'commentors':commentors,
               'post':post,
               'form':form}

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.profile
            comment.post = post
            post.commentors.add(request.user)
            comment.save()
            return redirect('post-comments',pk)
        else:
            return HttpResponse("dumbass")

    return render(request,'postCommentSection.html',context)
#profile management
@login_required(login_url='/login')
def profilePage(request,pk):
    profile = Profile.objects.get(id=pk)
    #try add _ set if it doesnt work
    followers = profile.following.all()

    if ProfileFollowing.objects.filter(follower=request.user.profile,profile=profile):
      following = True 
    else:
        following = False

    print(following)
    context = {'profile':profile,
               'followers':followers,
               'following':following,
               }
    return render(request,'profile.html',context)

@login_required(login_url='/login')
def editProfile(request,pk):
    profile = Profile.objects.get(id=pk)

    if request.user.id != profile.user.id:
        return redirect('home')

    form = ProfileForm(instance=profile)
    context = {'form': form}
    if request.method == 'POST':
            form = ProfileForm(request.POST,instance=profile,files=request.FILES)
            if form.is_valid():
                profile = form.save(commit=True)
                return redirect('profile',pk)
            else:
                return HttpResponse("error")

    return render(request,'edit-profile.html',context)

@login_required(login_url='login')
def follow(request,pk):
    profile = Profile.objects.get(id=pk)
    if profile:
        if not ProfileFollowing.objects.filter(follower=request.user.profile,profile=profile):
            follow = ProfileFollowing.objects.create(
                profile =  profile,
                follower = request.user.profile
            )
    return redirect('profile',pk)

@login_required(login_url='login')
def unfollow(request,pk):
    profile = Profile.objects.get(id=pk)
    if profile:
        ProfileFollowing.objects.filter(follower=request.user.profile,profile=profile).delete()
    
    return redirect('profile',pk)