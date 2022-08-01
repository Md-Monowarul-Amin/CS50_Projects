from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_aucction", views.create_auction, name="create_auction"),
    path("<int:listing_id>/create_bid", views.create_bid, name="create_bid"),
    path("<int:listing_id>/AddToWatchList", views.AddToWatchList, name="AddToWatchList"),
    path("VisitWatchList", views.VisitWatchList, name="VisitWatchList"),
    path("<int:listing_id>/RemoveFromWatchList", views.RemoveFromWatchList, name="RemoveFromWatchList"),
    path("<int:listing_id>/AddComment", views.AddComment, name="AddComment"),
    path("<int:listing_id>/CloseAuction", views.CloseAuction, name="CloseAuction"),
    path("<int:category_id>/SelectCategory", views.SelectCategory, name="SelectCategory"),
    path("VisitCategory", views.VisitCategory, name="VisitCategory"),
]

