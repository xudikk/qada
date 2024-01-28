#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.urls import path

from core.auth import sign_in, sign_out, hide_alert, sign_up
from core.views import index, grader, report, goto, qada_events

urlpatterns = [
    path('', index, name='home'),

    path('g-<int:pk>/<status>/nomoz-<type>', grader, name='gr'),

    # report
    path('r/y-<int:year>/m-<int:month>/', report, name='report'),
    path('goto/', goto, name='goto'),
    path('qada-events/', qada_events, name='qada_events'),

    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),
    path('regis/', sign_up, name='regis'),
    path('hide_alert/', hide_alert, name='hide_alert'),
]