from flask import Blueprint, render_template, url_for, redirect, flash, request
from . import db
from flask_login import current_user
from .models import User
from datetime import datetime, timedelta
from sqlalchemy import func

views = Blueprint('views', __name__)

@views.route('/')

@views.route('/')
def home():
    user = User.query.filter_by(id=1).first()
    first_name = str(user.first_name) if user and user.first_name else None
    return render_template('home.html', first_name=first_name)

