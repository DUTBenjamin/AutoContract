from django.shortcuts import render

def word_view(request):
    return render(request,'word.html')
