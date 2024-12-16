from django.urls import path
from . import views

urlpatterns = [
    path("helloworld/", views.printHelloWorld),
    path("modelresp/", views.modelResponse),
    path("plannerresp/", views.plannerResponse),
    path("plannertestresp/", views.plannerTestResponse),
    path("callerresp/", views.callerResponse),
    path("smartwatchstats/", views.getSmartWatchStats),
    path("detectAbnormality/", views.detectAbnormality),
    path("createReminder/", views.createReminders),
    path("getReminders/", views.getReminders),
    path("sendReminder/", views.sendReminders)
]
