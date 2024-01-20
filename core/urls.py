#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.urls import path

from core.auth import sign_in, sign_out
from core.views import index, grader, report, goto

urlpatterns = [
    path('', index, name='home'),

    path('g-<int:pk>/<status>/nomoz-<type>', grader, name='gr'),

    # report
    path('r/y-<int:year>/m-<int:month>/', report, name='report'),
    path('goto/', goto, name='goto'),

    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),
]