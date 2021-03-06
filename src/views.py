from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .forms import ExtendedUserCreationForm, VendorServiceForm, ExtendedVendorCreationForm, ServiceBookingForm, \
    AddStateForm, AddCityForm, PatientReportForm
from .models import City, VendorService, Chaperone, State, Patient, PatientReport
from reportlab.pdfgen import canvas
from django.http import HttpResponse


class Index(TemplateView):
    template_name = 'index.html'


def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')

        user = auth.authenticate(email=email, password=pass1)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request,
                           'Please enter a correct username and password. Note that both fields may be '
                           'case-sensitive.')
            return redirect('login')
    else:
        return render(request, 'registration/login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def userRegistration(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            ven = form.cleaned_data.get('user')
            print(ven)
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {email}.')
            return redirect('login')
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'registration/userRegistration.html', {'form': form})


def vendorRegistration(request):
    if request.method == 'POST':
        form1 = ExtendedVendorCreationForm(request.POST)
        if form1.is_valid():
            ven = form1.cleaned_data.get('vendor')
            print(ven)
            form1.save()
            email = form1.cleaned_data.get('email')

            messages.success(request, f'Account created for {email}.')
            return redirect('login')
    else:
        form1 = ExtendedVendorCreationForm()
    return render(request, 'registration/vendorRegistration.html', {'form1': form1})


@login_required()
def bookingService(request):
    if request.method == 'POST':
        bookingForm = ServiceBookingForm(request.POST, request.FILES)

        if bookingForm.is_valid():
            instance = bookingForm.save(commit=False)
            instance.holder = request.user
            instance.save()
            username = bookingForm.cleaned_data.get('patient')
            messages.success(request, f'Booking done successfully for {username}.')
            return redirect('serviceBooking')
    else:
        bookingForm = ServiceBookingForm()
    return render(request, 'patient/serviceBooking.html', {'bookingForm': bookingForm})


@login_required()
def patientProfile(request):
    qs1 = ""
    ret = ""
    try:
        qs1 = Patient.objects.filter(holder=request.user.id)
    except Exception as e:
        ret = "No record found"

    return render(request, 'patient/patientProfile.html', {"qs1": qs1, "ret": ret})


@login_required()
def patientStatus(request):
    qs2 = ""
    ret = ""
    qs1_id = ""
    try:
        qs1 = Patient.objects.filter(holder=request.user.id)
        for data in qs1:
            qs1_id = int(data.id)
        print(qs1)
        print(qs1_id)
        qs2 = PatientReport.objects.filter(id=int(qs1_id))
        print(qs2)

    except Exception as e:
        ret = "No record found"

    return render(request, 'patient/patientStatus.html', {"qs2": qs2, "ret": ret})


@login_required()
def getpdf(request, pid):
    qs = PatientReport.objects.filter(id=pid)
    print(qs)
    return render(request, 'patient/download-report.html', {'qs': qs})


@login_required()
def vendorProfile(request):
    qs1 = ""
    ret = ""
    try:
        qs1 = VendorService.objects.filter(identification=request.user.id)
    except Exception as e:
        ret = "No record found"

    return render(request, 'vendor/vendorProfile.html', {"qs1": qs1, "ret": ret})


@login_required()
def vendorService(request):
    if request.method == 'POST':
        vendorForm = VendorServiceForm(request.POST, request.FILES)

        if vendorForm.is_valid():
            instance = vendorForm.save(commit=False)
            instance.holder = request.user
            instance.save()
            username = vendorForm.cleaned_data.get('name')
            messages.success(request, f'Organization registration done successfully for {username}.')
            messages.info(request, f'Please wait for Organization verification!!!')
            return redirect('vendorService')
    else:
        vendorForm = VendorServiceForm()
    return render(request, 'vendor/vendorService.html', {'vendorForm': vendorForm})


@login_required()
def registerState(request):
    ctForm = AddCityForm()
    context = State.objects.all()
    contextCity = City.objects.all()

    if request.method == 'POST':
        stForm = AddStateForm(request.POST)
        if stForm.is_valid():
            stForm.save()
            name = stForm.cleaned_data.get('name')
            messages.success(request, f'{name} state added successfully.')
            return redirect('registerState')
        else:
            messages.error(request, f'State is already registered.')
            return redirect('registerState')

    else:
        stForm = AddStateForm()

    return render(request, 'vendor/addStateCity.html',
                  {'stForm': stForm, 'ctForm': ctForm, "viewState": context, "viewCity": contextCity})


@login_required()
def registerCity(request):
    if request.method == 'POST':
        ctForm = AddCityForm(request.POST)
        if ctForm.is_valid():
            ctForm.save()
            name = ctForm.cleaned_data.get('name')
            messages.success(request, f'{name} city added successfully.')
            return redirect('registerState')
        else:
            messages.error(request, f'City is already registered.')
            return redirect('registerState')
    else:
        ctForm = AddCityForm()
    return render(request, 'vendor/addCity.html', {'ctForm': ctForm})


def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'booking/city_dropdown_list_options.html', {'cities': cities})


def load_services(request):
    city_id = request.GET.get('city')
    services = VendorService.objects.filter(city_id=city_id).order_by('name')

    return render(request, 'booking/city_dropdown_list_options.html', {'services': services})


@login_required()
def vendorStatus(request):
    queryset1 = VendorService.objects.filter(registered_by=str(request.user.first_name + " " + request.user.last_name))
    # print(queryset1)
    # for data in queryset1:
    #     print(data.name)
    #     print(data.available)
    return render(request, 'vendor/serviceStatus.html', {"serviceStatus": queryset1})


@login_required()
def generateReport(request):
    qs = ""
    quid = ""
    ret = ""
    qs1 = ""
    try:
        qs = VendorService.objects.filter(identification=request.user.id)
        for data in qs:
            quid = data.id

        qs1 = Patient.objects.filter(service=quid)
        for data in qs1:
            print(data)
    except:
        ret = "No patient(s) is/are registered yet!!!"

    return render(request, 'vendor/generateReport.html', {"pdetails": qs1, "ret": ret})


@login_required()
def registeredPatient(request):
    qs = ""
    quid = ""
    ret = ""
    qs1 = ""
    try:
        qs = VendorService.objects.filter(identification=request.user.id)
        for data in qs:
            quid = data.id

        qs1 = Patient.objects.filter(service=quid)
        for data in qs1:
            print(data)
    except:
        ret = "No patient(s) is/are registered yet!!!"

    return render(request, 'vendor/registeredPatient.html', {"pdetails": qs1, "ret": ret})


@login_required()
def generate(request, patient_id):
    print(patient_id)
    qs1 = Patient.objects.filter(id=patient_id)
    for data in qs1:
        print(data)
    if request.method == 'POST':
        prForm = PatientReportForm(request.POST)
        if prForm.is_valid():
            prForm.save()
            name = prForm.cleaned_data.get('pname')
            print(name)
            messages.success(request, f'Report generated for {name} .')
            return redirect('generateReport')
    else:
        prForm = PatientReportForm()
    return render(request, 'vendor/generate.html', {"pform": prForm, "patientDetails": qs1})
