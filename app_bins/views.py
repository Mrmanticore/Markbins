from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import JsonResponse
from PIL import Image
import uuid  
import base64
from django.utils import timezone
from datetime import datetime, timedelta
import time
from .forms import ContactForm
import json
import requests
import re
import threading
import firebase_admin
from firebase_admin import credentials, firestore
import json
from dotenv import load_dotenv

def index(request):
    return render(request, './home.html')
def markbins(request):
    # Your view logic for markbins.html, if any
    return render(request, './markbins.html')
def spotfill(request):

    return render(request, './spotfill.html')


uploaded_image_ids = {}  # Dictionary to store uploaded image IDs
@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        unique_id = str(uuid.uuid4())[:8]  # Generate a unique ID
        image = request.FILES.get('image')
        if not image:
            return HttpResponseBadRequest('No image provided.')
        file_name, file_extension = os.path.splitext(image.name)
        new_file_name = f'{unique_id}{file_extension}'
        file_path = os.path.join('app_bins/media/downloads/user_images', new_file_name)
        with open(file_path, 'wb+') as f:
            for chunk in image:
                f.write(chunk)
        uploaded_image_ids[unique_id] = file_path  # Store the image ID and file path
        # Start a thread to delete the file after 1 minute
        delete_file_thread = threading.Thread(target=delete_file_after_delay, args=(file_path, unique_id))
        delete_file_thread.start()
        return JsonResponse({'success_message': 'Image uploaded successfully.', 'unique_id': unique_id})
    return HttpResponseBadRequest('Invalid request method.')



@csrf_exempt
def delete_expired_images(request):
    current_time = datetime.now()
    for unique_id, data in list(uploaded_image_ids.items()):
        creation_time = data['creation_time']
        if current_time - creation_time > timedelta(minutes=1):  # Check if more than 1 minute has passed
            file_path = data['file_path']
            os.remove(file_path)
            del uploaded_image_ids[unique_id]  # Remove the entry from the dictionary
    return JsonResponse({'status': 'success'})

def delete_file_after_delay(file_path, unique_id):
    time.sleep(120)  # Wait for 1 minute
    try:
        os.remove(file_path)  # Delete the file
        del uploaded_image_ids[unique_id]  # Remove the entry from the dictionary
    except OSError as e:
        print(f"Error deleting file: {e}")


@csrf_exempt
def capture_map(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            return HttpResponseBadRequest('No image provided.')

        # Save the image to the desired location as PNG
        file_path = os.path.join('app_bins/media/downloads/capture_pic', image.name)
        while os.path.exists(file_path):
            file_name, file_extension = os.path.splitext(file_path)
            file_name += '_'
            file_path = file_name + file_extension

        with open(file_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        if os.path.exists(file_path):
            message = 'Capture map image uploaded successfully.'
        else:
            message = 'Failed to save capture map image.'

        return JsonResponse({'success_message': message})

    return HttpResponseBadRequest('Invalid request method.')

@csrf_exempt
def submit_tweet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tweet = data.get('tweet')
        email = data.get('email')
        image_folder = 'app_bins/media/downloads/user_images'

        image_paths = []
        for filename in os.listdir(image_folder):
            if filename.endswith('.DS_Store'):
                continue  # Skip .DS_Store file
            if os.path.isfile(os.path.join(image_folder, filename)):
                with open(os.path.join(image_folder, filename), 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                    image_paths.append({'name': filename, 'data': image_data})

        # Extract URL from the tweet text
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)
        if urls:
            url = urls[0]  # Use the first URL found
            # Remove the URL from the tweet text
            tweet_cleaned = tweet.replace(url, '')
            # Append the URL at the end of the tweet
            tweet_cleaned += f' {url}'
        else:
            url = None
            tweet_cleaned = tweet

        # Remove HTML tags from the tweet text
        tweet_cleaned = re.sub(r'<[^>]*>', '', tweet_cleaned)

        # Print the tweet, email, and extracted URL
        print('Received Tweet:', tweet_cleaned)
        print('Received Email:', email)
        print('Extracted URL:', url)
        for image_path in image_paths:
            print('Image:', image_path['name'], 'Email:', email)  # Print the image file name and email address
            payload = {'tweet': tweet_cleaned, 'email': email, 'image': image_path['data'], 'image_name': image_path['name']}
            response = requests.post(url, json=payload)

        # Send the data to the Twitter bot server for each image
        

        url = 'https://markbins-bot.vercel.app/tweet'  # Update the URL if the server is hosted elsewhere
        # url = 'http://127.0.0.1:5000/tweet'  # Update the URL if the server is hosted elsewhere(local host)

        for image_path in image_paths:
            payload = {'tweet': tweet_cleaned, 'email': email, 'image': image_path['data'], 'image_name': image_path['name']}
            response = requests.post(url, json=payload)

            if response.status_code != 200:
                return JsonResponse({'status': 'error', 'message': f'Failed to send tweet to Twitter bot for image {image_path["name"]}'})
        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# ----------------------------

def guide_view(request):

    return render(request, 'Guide.html')  

def blogs_view(request):

    return render(request, 'blogs.html')  

def video_tutorial_view(request):

    return render(request, 'VideoTutorial.html')  

def about_view(request):

    return render(request, 'About.html')  

def contact_view(request):

    return render(request, 'contact.html')  

def mobile_view(request):
    return render(request, 'mobile.html')
#--------------------------------------------------------------Database------------------------------------------------
# if not firebase_admin._apps:
#     cred = credentials.Certificate("imp.json")
#     firebase_admin.initialize_app(cred)
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://markbinsdata-default-rtdb.firebaseio.com/'
#     })

# # Get a reference to the Firestore database
# db = firestore.client()


# def contact_view(request):
#     form = ContactForm()
#     return render(request, 'contact.html', {'form': form})

# def submit_contact_form(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             data = {
#                 'name': form.cleaned_data['name'],
#                 'email': form.cleaned_data['email'],
#                 'subject': form.cleaned_data['subject'],
#                 'message': form.cleaned_data['message'],
#             }
#             # Save data to Firestore
#             db.collection('contacts').add(data)
#             success = True
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form, 'success': success})


load_dotenv()


firebase_credentials_json = os.environ.get('FIREBASE_CREDENTIALS')


firebase_credentials = json.loads(firebase_credentials_json)

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)

# Get a reference to the Firestore database
db = firestore.client()

def contact_view(request):
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def submit_contact_form(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            # Save data to Firestore
            db.collection('contacts').add(data)
            success = True
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'success': success})