import datetime
import json

from cloudinary import CloudinaryImage
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LocationForm
from .models import Location, User

def index(request):
    location_items = list(Location.objects.order_by('city').values())
    for item in location_items:
        #convert cloudinary field to image url to be used in template
        photo = item["sticker_img"]
        photo_url = str(photo)
        img_url = CloudinaryImage(photo_url).build_url(
            width = 200, height = 200, crop = 'fill', radius = 10)
        item["sticker_img"] = img_url
    #create json output for use in javascript
    location_json = json.dumps(location_items)
    context = {'locations': location_json}
    return render(request, 'sticker/index.html', context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sticker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sticker/login.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sticker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "sticker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sticker/register.html")
    
def new_sticker(request):
    if request.method == "POST":
        #receive new sticker data from web page via POST
        country = request.POST["country"]
        city = request.POST["city"]
        latitude = float(request.POST["latitude"])
        longitude = float(request.POST["longitude"])
        img = request.FILES["sticker_img"]

        # Create a new post
        location = Location(
            owner=request.user,
            country=country,
            city=city,
            latitude=latitude,
            longitude=longitude,
            sticker_img=img,
            date_added=datetime.datetime.now(),
        )
        
        # save new post
        location.save()

        #display index page including new sticker
        return HttpResponseRedirect(reverse("index"))
        #return render(request, "sticker/index.html", {'lat': latitude, 'lng': longitude}) 
    else:
        form = LocationForm()
    return render(request, "sticker/new_sticker.html",{'form': form})
# Create your views here.
