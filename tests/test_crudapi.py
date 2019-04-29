import unittest
import os
import json
from app import create_app, db


class CandidateTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.candidate = {"name":"Aslam", "degree_name":"BSCS", "address":"lahore"}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_candidate_creation(self):
        """Test API can create a Candidate (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a candidate by making a POST request
        res = self.client().post('/candidate',headers=dict(Authorization=access_token),data=self.candidate)
        self.assertEqual(res.status_code, 201)
        

    def test_get_all_candidates(self):
        """Test API can get a candidateslist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # create a candidate by making a POST request
        res = self.client().post('/candidate',headers=dict(Authorization=access_token),data=self.candidate)
        self.assertEqual(res.status_code, 201)
       
        # get all the candidatelist that belong to the test user by making a GET request
        res = self.client().get('/candidate_list',headers=dict(Authorization=access_token))
        self.assertEqual(res.status_code, 200)

    def test_api_get_candidate_by_enrolement_no(self):
        """Test API can get a single candidate by using it's enrolement number."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post('/candidate',headers=dict(Authorization=access_token),data=self.candidate) 
        self.assertEqual(rv.status_code, 201)

        results = json.loads(rv.data.decode())
        result = self.client().get('/candidate',headers=dict(Authorization=access_token),data={'enrolement_no':results['enrolement_no']})
        self.assertEqual(result.status_code, 200)

    def test_candidate_update(self):
        """Test API can edit an existing candidate. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        # first, we create a candidate by making a POST request
        rv = self.client().post('/candidate',headers=dict(Authorization=access_token),data=self.candidate)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())

        #then, we edit the created candidate by making a PUT request
        rv = self.client().put('/candidate',headers=dict(Authorization=access_token),
            data={"enrolement_no":results['enrolement_no'],
                  "name": "Ali", "address":"Islamabad", "degree_name":"BSCS"})
        self.assertEqual(rv.status_code, 200)

        # finally, we get the edited candidate to see if it is actually edited.
        results = self.client().get('/candidate',headers=dict(Authorization=access_token),data={'enrolement_no':results['enrolement_no']})
        self.assertEqual(result.status_code, 200)

    def test_candidate_deletion(self):
        """Test API can delete an existing candidate. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client().post('/candidate',headers=dict(Authorization=access_token),data=self.candidate)
        self.assertEqual(rv.status_code, 201)
        results = json.loads(rv.data.decode())

        # delete the candidate we just created
        res = self.client().delete('/candidate',headers=dict(Authorization=access_token),data={'enrolement_no':results['enrolement_no']})
        self.assertEqual(res.status_code, 200)

        #Test to see if it exists, should return a 404
        result = self.client().get('/candidate',headers=dict(Authorization=access_token), data={'enrolement_no':results['enrolement_no']})
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()