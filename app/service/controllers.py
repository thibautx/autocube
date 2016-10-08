from flask import Blueprint, render_template, request, jsonify, redirect, url_for

service_module = Blueprint('_service', __name__, url_prefix='/service')

@service_module.route('/')
def home():
    return render_template("service/index.html")