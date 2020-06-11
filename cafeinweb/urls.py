
from django.contrib import admin
from django.urls import path
from api.views import *
from cafeinweb import settings
from django.templatetags.static import static
from django.conf.urls import url
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/saveuser', save_user),
    path('api/user/getdata', userOku),
    path('api/user/following', takipciDuzenle),
    path('api/user/updatename', usernameGuncelle),
    path('api/user/takipciGetir', takipciGetir),
    path('api/user/takipUpdate', takipciDuzenle),
    path('api/user/updatemesafe', updateMesafe),
    path('api/process/uploadImage', upload_pic),
    path('api/restaruant/get',get_kafe),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)