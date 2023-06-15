from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (IsAdminOrModeratorOrOwnerOrReadOnly, AdminOrReadOnly,
                          IsAdmin)
