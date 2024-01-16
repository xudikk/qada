#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.urls import path

from core.auth import sign_in, sign_out
from core.views import index

urlpatterns = [
    path('', index, name='home'),


    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),
]