from django.contrib.auth.decorators import login_required
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.views import redirect_to_login
from django.urls import resolve


class RejectAnonymousUsersMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if request.user.is_authenticated:
            return

        current_route = resolve(request.path_info).route
        print("Route", current_route)

        if not current_route.startswith("accounts"):
            return redirect_to_login(request.path)
