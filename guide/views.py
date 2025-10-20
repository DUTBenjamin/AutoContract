from django.shortcuts import render

def guide_view(request):
    return render(request, 'guide.html')

