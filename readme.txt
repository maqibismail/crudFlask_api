flask (create, read, update and delete ) api.
=> api is based on candidate's
	+ name
	+ enrolement_no 
	+ address 
	+ degree_name
	+ admission_status
=> urls:
	+ 127.0.0.1:5000/candidate_list     ## GET all candidate list
	+ 127.0.0.1:5000/candidate          ## GET PUT DELETE and UPDATE candidates against their enrolement no. 
	+ 127.0.0.1:5000/auth/register      ## Register the user
	+ 127.0.0.1:5000/auth/login         ## Login to authenticate


User has to login first to authenticate if user is not registered then it has to register first and then login to access the api. After successful login user has given a token which the user uses in access-token to access the api.

Tests file are places in separate test folder.
 + python manage.py test 