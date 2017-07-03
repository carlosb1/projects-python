from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, json
from werkzeug import check_password_hash, generate_password_hash
from app import app
from app.data import db
from app.mod_users.models import User
from app.mod_users.models import Log
from app.factory_responses import FactoryResponse

import uuid
import os



mod_users = Blueprint('users',__name__,url_prefix='/capture_telegram/v1.0')

def print_exception(data):
	if data==None:
		app.logger.error("It was not possible print errors")
		return
	app.logger.error('It was sent a bad request...')
	app.logger.error('data')
	app.logger.error('---------------------------')
	app.logger.error(str(data))
	app.logger.error('---------------------------')


@mod_users.route('/users',methods=['POST'])
def post_users():
	responses = FactoryResponse();
	app.logger.info("Applying post new user...")
	resp = responses.new400()
	try:
        	if request.method == 'POST':
			app.logger.info("Applying user creation")
			data_user = json.loads(request.data)
			new_telegram_id=data_user['data']['telegramid']
			user = User.query.filter_by(telegramid=new_telegram_id).first()
			if user is not None:
				return responses.new403()
			new_user = User.create(telegramid=new_telegram_id)
			resp = jsonify({'id':new_user.id}), 201
	except:
		print_exception(request.data)
        return resp


@mod_users.route('/logs',methods=['POST'])
def post_logs():
	responses = FactoryResponse();
	app.logger.info("Applying post logs...")
	resp = responses.new400()	
	if request.method == 'POST':
		try:
			data_logs = json.loads(request.data)['data']['logs']
			for log in data_logs:
				app.logger.info(str(log))
				Log.create(textlog=log['textlog'],username=log['username'])
			resp = responses.new200()	
		except:
			print_exception(request.data)
	return resp
			

@mod_users.route('/logs',methods=['GET'])
def get_logs():
	responses = FactoryResponse();
	app.logger.info("Applying get logs...")
	resp = responses.new400()	
	if request.method == 'GET':
		try:
			logs = Log.query.all()
			page = request.args.get('page',1,type=int)
			pagination = Log.query.paginate(page,per_page=app.config['PER_PAGE'],error_out=False)
			logs = pagination.items
			prev=None
			if pagination.has_prev:
				prev=url_for('logs.get_logs',page=page-1,_external=True)
			next=None
			if pagination.has_next:
				next=url_for('logs.get_logs',page=page+1,_external=True)
			if pagination.has_prev:
				prev=url_for('logs.get_logs',page=page-1,_external=True)
			resp = jsonify({'data' :[log.serialize() for log in logs],'pagination':{'prev': prev,'next': next,'count':pagination.total}})
		except:
			print_exception(request.data)
	return resp
			
