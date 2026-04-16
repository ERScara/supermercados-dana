from django.shortcuts import render

def acerca_de(request):
    return render(request, 'acerca_de.html')