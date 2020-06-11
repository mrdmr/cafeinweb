import math
from django.contrib.auth.models import User
from kullanici.models import Kullanici
from restaruant.models import Restaruant
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import ast
import random
import base64
from django.core.files.storage import FileSystemStorage
import time
import os
from cafeinweb import settings

@csrf_exempt
def save_user(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    userID = output_dict['userID']
    email = output_dict['emailOrPhone']
    userName = output_dict['userName']
    profilUrl = output_dict['profilUrl']
    kisi = Kullanici.objects.filter(userID=userID).values()
    users_list = list(kisi)
    if len(users_list) == 0:
        while(True):
            username = "User"+str(random.randint(0, 99999))
            kisiListesi = Kullanici.objects.filter(userName=username).values()
            users_list = list(kisiListesi)
            if(len(users_list) == 0):
                break
        b = Kullanici(userID=userID, emailOrPhone=email, userName=username)
        b.save()
        return HttpResponse(True)
    else:
        return HttpResponse(True)


@csrf_exempt
def userOku(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    userID = output_dict['userID']
    # return ValuesQuerySet object
    kisi = Kullanici.objects.filter(userID=userID).values()
    # converts ValuesQuerySet into Python list
    list_result = [entry for entry in kisi]
    if len(list_result) == 0:
        return HttpResponse()
    else:
        return HttpResponse(json.dumps(list_result[0]), content_type="application/json")


@csrf_exempt
def usernameGuncelle(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    userID = output_dict['userID']
    newUser = output_dict['newName']
    kisi = Kullanici.objects.filter(userID=userID).update(userName=newUser)
    return HttpResponse("True")


@csrf_exempt
def takipciDuzenle(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    userID = output_dict['userID']
    karsiUserID = output_dict['karsiID']
    durum = output_dict['tur']
    print(durum)
    if durum == "takipbirak":
        kisi = Kullanici.objects.get(userID=userID)
        if karsiUserID in kisi.followers:
            kisi.followers.remove(karsiUserID)
        kisi.save()
        return HttpResponse("true")
    elif durum == "takipet":
        kisi = Kullanici.objects.get(userID=userID)
        kisi.followers.append(karsiUserID)
        kisi.save()
        return HttpResponse(True)


@csrf_exempt
def takipciGetir(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    takipci = output_dict['takipList']
    liste = str(takipci[1:-1:]).split(',')
    userList = []
    for i in liste:
        kisi = Kullanici.objects.filter(userID=i.strip()).values()
        list_result = [entry for entry in kisi]
        if len(list_result) == 0:
            pass
        else:
            userList.append(list_result[0])
    return HttpResponse(json.dumps({"results": userList}))


@csrf_exempt
def bildirimEkle(request):
    # karşı kişi update et
    userID = request.POST.get('userID')
    karsiUserID = request.POST.get('karsiID')
    durum = request.POST.get('tur')
    if durum == "ekle":
        kisi = User.objects.get(userID=userID)
        if karsiUserID in kisi.followers:
            kisi.bildirim.remove(karsiUserID)
        kisi.save()
        return HttpResponse("cikar")
    elif durum == "ekle":
        kisi = User.objects.get(userID=userID)
        kisi.bildirim.append(karsiUserID)
        kisi.save()
        return HttpResponse("true")


@csrf_exempt
def checkInKaydet(request):
    # karşı kişi update et
    userID = request.POST.get('userID')
    restID = request.POST.get('restID')
    kisi = User.objects.get(userID=userID)
    rest = Restaruant.objects.get(id=restID)
    # Restarunat modeline de ekle
    if restID not in kisi.followers:
        kisi.checkIn.append(restID)
        rest.checkin.append(userID)
    kisi.save()
    return HttpResponse("cikar")



@csrf_exempt
def checkInGoster(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    durum = output_dict['tur']
    if(durum == True or durum == "true"):
        userID = output_dict['userID']
        kisi = User.objects.filter(userID)
    else:
        restID = output_dict['restID']
    return HttpResponse(json.dumps({"results": ''}))

# Mesafe Hesaplayıp yakındakileri göstermek için
@csrf_exempt
def get_kafe(request):
    latitude = float(request.POST.get('latitude'))
    longitude = float(request.POST.get('longitude'))
    mesafe = float(request.POST.get('mesafe'))
    users = Restaruant.objects.all().values()
    users_list = list(users)
    a = []
    for i, j in enumerate(users_list):
        sonuc = distance(latitude, longitude, j['latitude'], j['longitude'],mesafe)
        if sonuc:
            a.append(j)
        else:
            del users_list[i]
    return HttpResponse(json.dumps({"status": "ok", "totalResults": len(a), "articles": a}, ensure_ascii=False),
                        content_type="application/json")


def distance(lat1, lon1, lat2, long2,mesafe):
    radius = 6371  # km
    dlat = math.radians(float(lat2)-float(lat1))
    dlon = math.radians(float(long2)-float(lon1))
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(float(lat1))) \
        * math.cos(math.radians(float(lat2))) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    if d < mesafe:
        return True
    else:
        return False


# Mesafe Ayar Değiştirme
@csrf_exempt
def updateMesafe(request):
    message = str(request.body.decode('utf-8'))
    ascii_message = message.encode('ascii')
    output_byte = base64.b64encode(ascii_message)
    msg_bytes = base64.b64decode(output_byte)
    ascii_msg = msg_bytes.decode('ascii')
    ascii_msg = ascii_msg.replace("'", "\"")
    output_dict = json.loads(ascii_msg)
    userID = output_dict['userID']
    mesafe = output_dict['mesafe']
    kisi = Kullanici.objects.filter(userID=userID).update(mesafe=mesafe)
    return HttpResponse(True)
@csrf_exempt
def upload_pic(request):
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        print(myfile)
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, myfile.name)):
            os.remove(os.path.join(settings.MEDIA_ROOT, myfile.name))
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("dosya URL " + fs.url(filename))
        return HttpResponse(json.dumps({"imageUrl": uploaded_file_url}, ensure_ascii=False),content_type="application/json")

@csrf_exempt
def updatePhotoInfo(request):
    userID = float(request.POST.get('userID'))
    imageUrl = float(request.POST.get('imageUrl'))
    kisi = Kullanici.objects.filter(userID=userID).update(imageUrl=imageUrl)
    return HttpResponse(True)