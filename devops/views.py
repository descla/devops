from django.shortcuts import render,HttpResponse

# Create your views here.

def index(request):
    #return HttpResponse("Hello,world.You are at the all index")
    return render(request, 'index.html')

