
from django.contrib.auth import authenticate, login as loginUser, logout #login user and logout user
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.
from  .models import TODO
from .forms import TODOForm
from django.contrib.auth.decorators import login_required 



@login_required(login_url='login' ) #if the user is loged in only they can access the page .
def home(request):#only accesible home page  when the user is loged in !
    if request.user.is_authenticated:#if user is logged in !
        user = request.user
        #getting user that is logged in !
        form =TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        #displaying onlythe login in users todo list
        #('-priority') forordering in decending order
        
        context ={
        'form':form,
        'todos':todos
            }
        return render(request, 'index.html', context)



def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home')

        else:
            context = {
                "form": form

            }
            return render(request, 'login.html', context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)

        context = {
            'form': form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'signup.html', context=context)


@login_required(login_url='login' ) #means you can only acess todo if your only loooged in.
def add_todo(request):
    if request.user.is_authenticated:#if user is logged in 
        user = request.user #getting logged in user
        print(user)#to see user
        form=TODOForm(request.POST)
        context = {
            'form':form
         }
        if form.is_valid():
             print(form.cleaned_data)
             todo= form.save(commit=False)
             todo.user=user
             todo.save()
             print(todo)#print saved to do in console
             return redirect("home")
        else:
            return render(request, 'index.html', context)    




def delete_todo(request, id):
    print(id)
    TODO.objects.get(pk=id).delete()
    return redirect('home')



def change_todo(request , id, status ):
    todo = TODO.objects.get(pk=id)
    todo.status = status #status we are getting from parameterss
    todo.save()#after that saving the status
    return redirect( 'home') 


def signout(request):
    logout(request)
    return  redirect('login')
    