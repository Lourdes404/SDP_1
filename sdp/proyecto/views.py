from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages

""" import os
import subprocess

import msal
import requests

from sklearn.feature_extraction.text import TfidfVectorizer """


def index(request):
    return render(request,'index.html')