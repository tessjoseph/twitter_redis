from flask import Blueprint, render_template, url_for, redirect, flash, request
from . import db
from flask_login import current_user
from .models import Transaction
from datetime import datetime, timedelta
from sqlalchemy import func

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')
