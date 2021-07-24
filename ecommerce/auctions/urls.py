from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("activeListing",views.active_listing,name = "activeListing"),
    path("createListing",views.create_listing,name = "createListing"),
    path("listings/<int:id>",views.listings, name = "listings"),
    path("watchlist",views.watchlist,name = "watchlist"),
    path("addtowatchlist/<int:item_id>", views.add_to_watchlist, name = "addToWatchlist"),
    path("removefromwatchlist/<int:item_id>", views.remove_from_watchlist, name = "removeFromWatchlist"),
    path("categories",views.categories,name = "categories"),
    path("category/<str:cat>",views.category, name = "category")

]
