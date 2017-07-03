from flask import url_for, jsonify, json
from app.test_base import BaseTestCase
from app import app

from models import User
from models import Log
from app.data import db


class TestUsersModel(BaseTestCase):
    def test_create_user(self):
        user = User("telegramid")
        self.assertTrue(user.telegramid,"telegramid")
        
class TestLogsModel(BaseTestCase):
    def test_create_log(self):
        log = Log("user1","text for log")
        self.assertTrue(log.textlog,"text for log")
        self.assertTrue(log.username,"user1")


#TODO add acceptance tests...
class TestUsersView(BaseTestCase):
    def test_post_create_user_correct(self):
        with self.client:
            headers = { 'Accept': 'application/json'}
            data = { 'data': {
                    'telegramid':'testtelegramid3'
                }
            }
            response = self.client.post("/capture_telegram/v1.0/users",data=json.dumps(data),headers=headers)
            parsed_data = json.loads(response.data)
            self.assertTrue(response.status_code == 201 and parsed_data['id'] == 1)

    
    def test_post_create_user_incorrect(self):
        with self.client:
            headers = { 'Accept': 'application/json'}
            data = { 'invaliddata':  'invaliddata'}
            response = self.client.post("/capture_telegram/v1.0/users",data=json.dumps(data),headers=headers)
            self.assert_400(response)
 
    def test_post_create_two_times_user_error(self):
        with self.client:
            headers = { 'Accept': 'application/json'}
            data = { 'data': {
                    'telegramid':'testtelegramid' 
                }
            }
            response = self.client.post("/capture_telegram/v1.0/users",data=json.dumps(data),headers=headers)
            response = self.client.post("/capture_telegram/v1.0/users",data=json.dumps(data),headers=headers)
            self.assert_403(response)  


    def test_post_logs_correctly(self):
        with self.client:
            headers = { 'Accept': 'application/json'}
            data = { 'data': {
                'logs':[{'username': 'user1', 'textlog':'text with log1'},{'username':'user2', 'textlog':'text_wit_log2'}]  
                }
            }
            response = self.client.post("/capture_telegram/v1.0/logs",data=json.dumps(data),headers=headers)
            self.assert_200(response)  


    def test_get_logs_correctly(self):
        with self.client:
            headers = { 'Accept': 'application/json'}
            data = { 'data': {
                'logs':[{'username': 'user1', 'textlog':'text with log1'},{'username':'user2', 'textlog':'text_wit_log2'}]  
                }
            }
            response = self.client.post("/capture_telegram/v1.0/logs",data=json.dumps(data),headers=headers)          
            self.assert_200(response)  
                        
            response = self.client.get("/capture_telegram/v1.0/logs")
            parsed_data=json.loads(response.data)
            self.assertTrue(len(parsed_data['data'])>0)
            self.assert_200(response)
