from django.shortcuts import render
from django.http import HttpResponse
from airtable import Airtable
import re
import hashlib
from datetime import date as date_ref

airtable = Airtable('appsa9Pz4MHCU6SAE', 'userdetails', api_key='keyCF870WzQlzT3of')

airtables = Airtable('appsa9Pz4MHCU6SAE', 'medicines', api_key='keyCF870WzQlzT3of')


# Cate your views here.
def hi(request):
    return render(request, 'demoapp/hi.html')


def exp(request):
    return render(request, 'demoapp/exp.html')


def home(request):
    return render(request, 'demoapp/home.html')


def signUp(request):
    return render(request, 'demoapp/signup.html')


def signin(request):
    return render(request, 'demoapp/signin.html')


def contact(request):
    return render(request, 'demoapp/contact.html')


def home(request):
    return render(request, 'demoapp/home.html')


def medicine(request):
    return render(request, 'demoapp/medilist.html')


def check_old_meds():
    meds = airtables.get_all()

    expired_med_ids = []

    today = date_ref.today()
    this_year, this_month, this_date = map(int, str(today).split('-'))

    for med in meds:
        if not med["fields"]: continue

        expire_date = med["fields"]["Exdate"]
        year, month, date = map(int, expire_date.split('-'))

        if this_year > year:
            expired_med_ids.append(med["id"])

        elif this_year == year:
            if this_month > month:
                expired_med_ids.append(med["id"])

            elif this_month == month:
                if this_date > date:
                    expired_med_ids.append(med["id"])

    for exp_med_id in expired_med_ids:
        airtables.delete(exp_med_id)


def take(request):
    check_old_meds()
    mn = request.POST["mediname"]
    mn2 = airtables.search("MedName", mn.lower())
    if mn2:
        details = []

        for i in range(len(mn2)):
            username = mn2[i]['fields']['userdetails']
            mn3 = airtable.search("Username", username)
            try:
                details.append(mn3[0]['fields'])
            except IndexError:
                pass
        print(details)
        return render(request, 'demoapp/take.html', {'details': details})
    return render(request, 'demoapp/take.html', {"phone": 'REQUIRED MEDICINE IS NOT FOUND'})


def registrationSuccess(request):
    print(request)
    name = request.POST["name"]
    username = request.POST['uname']
    password = request.POST['pwd']
    emailid = request.POST['email']
    phoneno = request.POST['pno']
    address = request.POST['adres']
    passwordhash = hashlib.md5(password.encode())
    userdata = airtable.search("Username", username)
    if (userdata != []):
        return render(request, "demoapp/signup.html", {"error": "Username already exists"})
    userdata = airtable.search("Email", emailid)
    if (userdata != []):
        return render(request, "demoapp/signup.html", {"error": "Email already registered"})
    userdata = airtable.search("Phoneno", phoneno)
    print(userdata)
    if (userdata != []):
        return render(request, "demoapp/signup.html")

    user_details = {
        "Username": username,
        "Password": passwordhash.hexdigest(),
        "Name": name,
        "Email": emailid,
        "Phoneno": phoneno,
        "Address": address,
    }
    airtable.insert(user_details)

    return render(request, 'demoapp/registrationSuccess.html')


def loginsucess(request):
    username = request.POST['uname']
    password = request.POST['pwd']
    passwordhash = hashlib.md5(password.encode())
    userdata = airtable.search("Username", username)
    if (userdata == []):
        return render(request, "demoapp/signin.html", {"error": "Invalid UserName"})
    if (passwordhash.hexdigest() != userdata[0]["fields"]["Password"]):
        return render(request, "demoapp/signin.html", {"error": "Invalid Password"})
    return render(request, "demoapp/loginsucc.html")



def medilist(request):
    print(request)
    n = request.POST["mediname"]
    username = request.POST["username"]
    ed = request.POST["exdate"]
    medicine_details = {
        "MedName": n.lower(),

        "userdetails": username,
        "Exdate": ed,

    }
    airtables.insert(medicine_details)

    return render(request, "demoapp/medilist.html")