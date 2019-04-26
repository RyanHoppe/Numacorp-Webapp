from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from datetime import datetime
from django.views.generic import TemplateView

from form.models import MaterialsModel, ClockInModel, ClockOutModel
from form.functions import calculate_total_materials, Material, determine_schedules
from . forms import MaterialsForm, ClockInForm, ClockOutForm, DateSelectForm



# View for the main index page
def index(request):
    forms = MaterialsModel.objects.all()[:3]

    context ={
        'title': 'Employee Hub',
        'forms': forms
    }

    return render(request, 'form/index.html', context)


#View for the material form submission page
def materials_form_submission(request):
    form = MaterialsForm(request.POST)

    if request.method == "POST":
        form = MaterialsForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
    else:
        form = MaterialsForm()

    context = {
        'title' : 'Materials Form Submission',
        'form': form
    }

    return render(request, 'form/materials_form_submission.html', context)


#Details page for viewing a submission
def details(request, id):
    model = MaterialsModel.objects.get(id=id)
    
    context = {
        'title': 'Detailed Form View',
        'model': model
    }

    return render(request, 'form/details.html', context)


#Page used to edit materials form entries
def edit(request, id):
    model = MaterialsModel.objects.get(id=id)
    form = MaterialsForm(request.POST, instance=model)

    if request.method == "POST":
        form = MaterialsForm(request.POST, instance=model)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('/form/details/'+id)
    else:
        form = MaterialsForm(instance=model)

    context = {
        'title': 'Edit Form',
        'form': form
    }

    return render(request, 'form/edit.html', context)


#Delete page for a particular materials form entry
def delete(request, id):
    model = MaterialsModel.objects.get(id=id)

    if request.method == "POST":
        model.delete()
        return redirect('/form/view_all')
            

    context = {
        'title': 'Are you sure you wish to delete this entry? (Cannot undo this action)',
        'model': model
    }

    return render(request, 'form/delete.html', context)


#View for viewing all materials forms
def view_all(request):
    models = MaterialsModel.objects.all()

    context = {
        'title': 'All Material Submissions',
        'models': models
    }

    return render(request, 'form/viewall.html', context)


#for the page that displays used material totals
def used_materials(request):
    steel = Material("Steel",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Steel")))
    lumber = Material("Lumber",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Lumber")))
    shingles = Material("Shingles",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Shingles")))
    nails = Material("Nails",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Nails")))

    materials_list = [steel, lumber, shingles, nails]

    context = {
        'title': 'Total Used Material Amounts',
        'materials': materials_list
    }

    return render(request, 'form/used_materials.html', context)


#class used for a get/post form for filtering material totals by date
class SelectDate(TemplateView):
    template_name = 'form/select_date.html'

    def get(self, request):
        form = DateSelectForm()

        args = {
            'title': 'Please select a date',
            'form': form
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = DateSelectForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']

        steel = Material("Steel",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Steel",date_submitted=datetime(date.year,date.month,date.day))))
        lumber = Material("Lumber",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Lumber",date_submitted=datetime(date.year,date.month,date.day))))
        nails = Material("Nails",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Nails",date_submitted=datetime(date.year,date.month,date.day))))
        shingles = Material("Shingles",calculate_total_materials(MaterialsModel.objects.filter(materials_used="Shingles",date_submitted=datetime(date.year,date.month,date.day))))

        post_string = (
            steel.m + ": " + str(steel.q) + "\n" +
            lumber.m + ": " + str(lumber.q) + "\n" +
            nails.m + ": " + str(nails.q) + "\n" +
            shingles.m + ": " + str(shingles.q)
        )

        month_names = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }

        title = ('Total amounts for ' + month_names[date.month] + ' ' + str(date.day) + ', ' + str(date.year))
        args = {
            'title': title,
            'form': form,
            'post': post_string
        }

        return render(request, self.template_name, args)
    

#View for submitting a clock-in form
def clock_in_form_submission(request):
    form = ClockInForm(request.POST)

    if request.method == "POST":
        form = ClockInForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
    else:
        form = ClockInForm()

    context = {
        'title' : 'Clock-In Form Submission',
        'form': form
    }

    return render(request, 'form/clock_in_out_form.html', context)


#View for submitting a clock-out form
def clock_out_form_submission(request):
    model = ClockOutModel
    form = ClockOutForm(request.POST)

    if request.method == "POST":
        form = ClockOutForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')
 
    else:
        form = ClockOutForm()

    context = {
        'title' : 'Clock-Out Form Submission',
        'form': form
    }

    return render(request, 'form/clock_in_out_form.html', context)


#view for analyzing employee work hours (clock-in ---> clock-out)
def schedule_view(request):
    clock_in = ClockInModel.objects.all()
    clock_out = ClockOutModel.objects.all()
    schedule_list = determine_schedules(clock_in, clock_out)

    context = {
        'title': 'Employee Work Hours',
        'list': schedule_list
    }
    return render(request, 'form/schedule_view.html', context)