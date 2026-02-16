from django.shortcuts import render
from ..users.forms import SignInForm
from django.contrib.auth import authenticate, login
from Shop.models import ShopDetails

