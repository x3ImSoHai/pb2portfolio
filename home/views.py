from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pymysql
import hashlib
import base64


PRESALT = "sQ(/aekbBmu!"
SUFSALT = "QegzK12Ye2sK"

def saltnhash(password):
    preSalt = PRESALT
    sufSalt = SUFSALT

    saltedPassword = preSalt + password + sufSalt

    m = hashlib.md5()
    m.update(saltedPassword.encode())

    encoded = base64.b64encode(m.digest())
    return encoded.decode()

def connectSQL():
    mydb = pymysql.connect("nyov.mysql.pythonanywhere-services.com","nyov","Power1000","nyov$database")
    #mydb = pymysql.connect("localhost","root","root","pb2")
    return mydb

def loginFunc(login, password):
    mydb = connectSQL()
    mycursor = mydb.cursor()

    sql = "SELECT `username`, `password` FROM `npuser` WHERE `username` = %s AND `password` = %s;"
    insertTuple = (login, saltnhash(password))

    mycursor.execute(sql, insertTuple)
    results = mycursor.fetchall()

    mydb.close()
    return results

def verifyApiKey(request):
    apiKey = request.POST.get("apiKey", "")

    if apiKey == "83388fc7d26bdf4d930ab67bbf4cfbfc":
        return True
    return False
#------------------------------------------------------------------

#/
def index(request):
    mydb = connectSQL()
    mycursor = mydb.cursor()

    sql = "SELECT path FROM `npslideshow`"
    mycursor.execute(sql)
    slideshow = mycursor.fetchall()

    indexJson = {
        'slideshow': slideshow,
    }

    mydb.close()
    return render(request, 'home/index.html', indexJson)

#/login
def login(request):
    submitReq = request.POST.get('req', '')

    if(submitReq == "submit"):
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        results = loginFunc(username, password)

        if not results:
            return render(request, 'home/login.html', {'success': 0})
        else:
            request.session['login'] = 'true'
            return HttpResponseRedirect('admin')
    else:
        return render(request, 'home/login.html')

#/admin
def admin(request):
    try:
        if(request.session['login'] == 'true'):
            mydb = connectSQL()
            mycursor = mydb.cursor()

            sql = "SELECT * FROM npslideshow"
            mycursor.execute(sql)
            slideshow = mycursor.fetchall()

            sql = "SELECT * FROM npbug"
            mycursor.execute(sql)
            bug = mycursor.fetchall()

            adminJson = {
                'slideshow': slideshow,
                'bug': bug
            }

            mydb.close()
            return render(request, 'home/admin.html', adminJson)
        else:
            return HttpResponse('How did you end up here?')
    except KeyError:
        return HttpResponseRedirect('login')

#/logout
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('login')

#/bug
def bug(request):
    mydb = connectSQL()
    mycursor = mydb.cursor()

    sql = "SELECT * FROM `npbug`"
    mycursor.execute(sql)
    bug = mycursor.fetchall()

    bugJson = {
        'bug': bug,
        'total': len(bug)
    }

    mydb.close()
    return render(request, 'home/bug.html', bugJson)

#/admin/img
def changeImg(request):
    try:
        if(request.session['login'] == 'true'):
            id = request.GET.get("id", "")

            if id == "":
                return HttpResponse("Missing ID!", status=400)

            mydb = connectSQL()
            mycursor = mydb.cursor()
            insertTuple = (id)

            sql = "SELECT * FROM `npslideshow` WHERE id=%s;"
            mycursor.execute(sql, insertTuple)

            results = mycursor.fetchall()

            mydb.close()

            if not results:
                return HttpResponse("Invalid ID!", status=400)

            adminJson = {
                "data" : results[0]
            }

            return render(request, "home/changeImg.html", adminJson)
        else:
            return HttpResponse('How did you end up here?')
    except KeyError:
        return HttpResponseRedirect('../login')

#/admin/bug
def changeBug(request):
    try:
        if(request.session['login'] == 'true'):
            id = request.GET.get("id", "")

            if id == "":
                return HttpResponse("Missing ID!", status=400)

            mydb = connectSQL()
            mycursor = mydb.cursor()
            insertTuple = (id)

            sql = "SELECT * FROM `npbug` WHERE id=%s;"
            mycursor.execute(sql, insertTuple)

            results = mycursor.fetchall()

            mydb.close()

            if not results:
                return HttpResponse("Invalid ID!", status=400)

            adminJson = {
                "data" : results[0]
            }

            return render(request, "home/changeBug.html", adminJson)
        else:
            return HttpResponse('How did you end up here?')
    except KeyError:
        return HttpResponseRedirect('../login')

#/----------------------------------------------------------------

#/api/addImg
def addImg(request):
    if request.method == "POST":
        path = request.POST.get("path", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if path == "":
            return HttpResponse("Empty fields detected. Request not processed.", status=400)

        if len(path) > 30:
            return HttpResponse("Path too long. Maximum 30 characters.", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()

        sql = "INSERT INTO `npslideshow` (`path`) VALUES (%s);"
        insertTuple = (path)
        mycursor.execute(sql, insertTuple)
        mydb.commit()

        mydb.close()
        return HttpResponseRedirect('../admin')
    else:
        return HttpResponse("Invalid HTTP request method.", status=405)

#/api/addBug
def addBug(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        description = request.POST.get("description", "")
        severity = request.POST.get("severity", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if (description == "" or name == ""):
            return HttpResponse("Empty fields detected. Request not processed.", status=400)

        if len(name) > 100:
            return HttpResponse("Name too long. Max 100 characters.", status=400)

        if len(description) > 1000:
            return HttpResponse("Description too long. Max 1000 characters.", status=400)

        if(severity != "1" and severity != "2" and severity != "3" ):
            return HttpResponse("Invalid format / number for severity. Only 1, 2 or 3.", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()

        sql = "INSERT INTO `npbug` (`name`, `description`, `severity`) VALUES (%s, %s, %s);"
        insertTuple = (name, description, severity)

        mycursor.execute(sql, insertTuple)
        mydb.commit()

        mydb.close()
        return HttpResponseRedirect('../admin')
    else:
        return HttpResponse("Invalid HTTP request method.", status=405)

#/api/actionImg
def actionImg(request):
    if request.method == "POST":
        req = request.POST.get("req", "")
        id = request.POST.get("id", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if id == "":
            return HttpResponse("Invalid ID!", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()
        insertTuple = (id)

        sql = "SELECT * FROM `npslideshow` WHERE id=%s;"
        mycursor.execute(sql, insertTuple)

        results = mycursor.fetchone()

        if not results:
            mydb.close()
            return HttpResponse("Invalid ID!", status=400)

        if req == "Delete":
            sql = "DELETE FROM `npslideshow` WHERE (`id` = %s);"

            mycursor.execute(sql, insertTuple)
            mydb.commit()

        elif req == "Change":
            return HttpResponseRedirect('/admin/img?id=' + id)
        else:
            mydb.close()
            return HttpResponse("Invalid request type!", status=400)

        mydb.close()
        return HttpResponseRedirect('../admin')
    else:
        return HttpResponse("Invalid HTTP request method.", status=405)

#/api/actionBug
def actionBug(request):
    if request.method == "POST":
        req = request.POST.get("req", "")
        id = request.POST.get("id", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if id == "":
            return HttpResponse("Invalid ID!", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()
        insertTuple = (id)

        sql = "SELECT * FROM `npbug` WHERE id=%s;"
        mycursor.execute(sql, insertTuple)

        results = mycursor.fetchone()

        if not results:
            mydb.close()
            return HttpResponse("Invalid ID!", status=400)

        if req == "Delete":
            sql = "DELETE FROM `npbug` WHERE (`id` = %s);"

            mycursor.execute(sql, insertTuple)
            mydb.commit()

        elif req == "Change":
            return HttpResponseRedirect('/admin/bug?id=' + id)
        else:
            mydb.close()
            return HttpResponse("Invalid request type!", status=400)

        mydb.close()
        return HttpResponseRedirect('../admin')
    else:
        return HttpResponse("Invalid HTTP request method.", status=405)

#/api/changeBug
def changeBugApi(request):
    if request.method == "POST":
        id = request.POST.get("id", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if id == "":
            return HttpResponse("Invalid ID!", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()
        insertTuple = (id)

        sql = "SELECT * FROM `npbug` WHERE id=%s;"
        mycursor.execute(sql, insertTuple)

        results = mycursor.fetchone()

        if not results:
            mydb.close()
            return HttpResponse("Invalid ID!", status=400)

        name = request.POST.get("name", "")
        description = request.POST.get("description", "")
        severity = request.POST.get("severity", "")

        if (description == "" or name == ""):
            return HttpResponse("Empty fields detected. Request not processed.", status=400)

        if len(name) > 100:
            return HttpResponse("Name too long. Max 100 characters.", status=400)

        if len(description) > 1000:
            return HttpResponse("Description too long. Max 1000 characters.", status=400)

        if(severity != "1" and severity != "2" and severity != "3" ):
            return HttpResponse("Invalid format / number for severity. Only 1, 2 or 3.", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()

        sql = "UPDATE `npbug` SET `name` = %s, `description` = %s, `severity` = %s WHERE (`id` = %s);"
        insertTuple = (name, description, severity, id)

        mycursor.execute(sql, insertTuple)
        mydb.commit()

        mydb.close()
        return HttpResponseRedirect('../admin')

#/api/changeImg
def changeImgApi(request):
    if request.method == "POST":
        id = request.POST.get("id", "")

        if(not verifyApiKey(request)):
            return HttpResponse("Unauthorised.", status=401)

        if id == "":
            return HttpResponse("Invalid ID!", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()
        insertTuple = (id)

        sql = "SELECT * FROM `npslideshow` WHERE id=%s;"
        mycursor.execute(sql, insertTuple)

        results = mycursor.fetchone()

        if not results:
            mydb.close()
            return HttpResponse("Invalid ID!", status=400)

        path = request.POST.get("path", "")

        if path == "":
            return HttpResponse("Path is empty!", status=400)

        mydb = connectSQL()
        mycursor = mydb.cursor()

        sql = "UPDATE `npslideshow` SET `path` = %s WHERE (`id` = %s);"
        insertTuple = (path, id)

        mycursor.execute(sql, insertTuple)
        mydb.commit()

        mydb.close()
        return HttpResponseRedirect('../admin')
