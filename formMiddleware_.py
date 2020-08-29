from functools import wraps
from flask import Response, request, g
import re

def validate(field, ex):
    x = re.search(ex, field)
    if x:
        return True
    return False

def validate_register(func):
    @wraps((func))
    def decorated_function(*args, **kwargs):

        if request.method == 'POST':

            # TeamName = request.form['teamname']
            name1 = request.form['name1']
            # name2 = request.form['name2']
            # name3 = request.form['name3']
            # name4 = request.form['name4']
            # name5 = request.form['name5']
            # phone1 = request.form['phone1']
            # phone2 = request.form['phone2']
            # phone3 = request.form['phone3']
            # phone4 = request.form['phone4']
            # phone5 = request.form['phone5']
            # inst1 = request.form['inst1']
            # inst2 = request.form['inst2']
            # inst3 = request.form['inst3']
            # inst4 = request.form['inst4']
            # inst5 = request.form['inst5']
            email = request.form['email']
            # Password = request.form['password']
            # RePassword = request.form['re-password']
            test = "The rain in Spain"

            isName1Valid = validate(name1, r"/^[A-Z][a-zA-Z-.:]+\s?[A-Z][a-zA-Z-.:]+$/")
            isEmailValid = validate(email, r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$")
            isTestValid = validate(test, "^The.*Spain$")
            
            
            errorDic = {}
            if not isName1Valid:
                errorDic['name1Error'] = "Name is invalid"
            if not isEmailValid:
                errorDic['emailError'] = "Email is invalid"
            if not isTestValid:
                errorDic['testError'] = "test is invalid"

            if errorDic:
                return Response(errorDic,mimetype='text/plain', status=401)
            
                


        return func(*args, **kwargs)
    return decorated_function

def hello_middleware(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        name = request.form['name']
        if name == "Kuddus":
            return Response(name, mimetype='text/plain', status=401)
        # email = request.form['email']
        NameError = "name error happened"
        emailError = "email error happened"
        g.token = {
            'name': NameError,
            'email': emailError
        }
        return func(*args, **kwargs)
    
    return decorated_function