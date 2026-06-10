from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.audit.models import AuditLog
from apps.audit.services import log_action
from apps.common.responses import fail, ok
from .serializers import LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)
        if user is None or user.status != user.ACTIVE:
            return fail("Invalid email or password.", status=401)

        refresh = RefreshToken.for_user(user)
        log_action(user, AuditLog.USER_LOGIN, target_type="USER",
                   target_id=user.id, request=request)
        return ok({
            "token": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }, message="Login successful")


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return ok(UserSerializer(request.user).data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        log_action(request.user, AuditLog.USER_LOGOUT, request=request)
        return ok(message="Logout successful")
