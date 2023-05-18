from django.shortcuts import render, redirect
from .models import Trainee, Person, Seasontrainee, Stageincludetrainee
from django.db.models import Max
import re
# Create your views here.

# Home page
def home(request):
    return render(request,'index.html')

def trainee(request):
    if request.method == 'GET':
        
        searched = request.GET.get('searched')
        if searched:
            x = re.search("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]", searched)
            if x:
                trainees = Trainee.objects.filter(ssn = searched)
                
                temp = Seasontrainee.objects.filter(ssn_trainee = searched)
                count = temp.count()
                
                temp2 = Stageincludetrainee.objects.filter(ssn_trainee = searched)
                max = temp2.aggregate(Max('ep_no'))['ep_no__max']
                if not max:
                    max = 1

                return render(request, 'trainee.html', {'trainees':trainees, 'count':count, 'max':max})
            else:
                trainees = Person.objects.filter(fname__contains = searched) or Person.objects.filter(lname__contains = searched)
                return render(request, 'trainee.html', {'trainees':trainees})
        else:
            trainees = Trainee.objects.all()
            return render(request, 'trainee.html', {'trainees':trainees, })

