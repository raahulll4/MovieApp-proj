from tkinter import * #import tkinter so the GUI can be made
import os # import OS so the files can be access from the directory
import urllib.request #import urllib so that I can retrieve the information from the URL
import json # import JSON so that i can handle data retrieved
from functools import partial
import hashlib

import sqlite3
con = sqlite3.connect("MovieApp.db")
c = con.cursor()

#creates the table USERS
c.execute("""CREATE TABLE IF NOT EXISTS users
          (username TEXT,
          password TEXT);""")

#creates the table RATING       
c.execute("""CREATE TABLE IF NOT EXISTS rating
          (username TEXT,
          movie TEXT,
          rating INTEGER,
          genre TEXT);""")

#creates the table WATCHLIST        
c.execute("""CREATE TABLE IF NOT EXISTS watchlist
          (username TEXT,
          movie TEXT,
          genre TEXT);""")

#creates the table FRIEND        
c.execute("""CREATE TABLE IF NOT EXISTS friend
          (username TEXT,
          friend TEXT);""")

def destroy11(): #closes errortitle()
    screen26.destroy()
    
def watchlistsuccess():
    global screen26
    screen26 = Toplevel(screen)
    screen26.title("Sucess")
    screen26.geometry("250x100")
    
    Label(screen26, text = "Movie App", bg = "#336699", fg = "white", width = "300", height = "2", font = ("Arial",12)).pack()
    Label(screen26, text = "Watchlist updated successfully").pack()
    Button(screen26, text = "Okay", command = destroy11).pack()


def addwatchlist(film,fgenre): #opens the user list and adds the film they want to the watchlist
    name = user
    title = film
    genre = fgenre

    c.execute("INSERT INTO watchlist(username, movie, genre)     \
            VALUES(?,?,?)",(name, title,genre))
    con.commit()
    
    watchlistsuccess()
    
def destroy10(): #closes errortitle()
    screen25.destroy()
    
def ratingsuccess():
    global screen25
    screen25 = Toplevel(screen)
    screen25.title("Success")
    screen25.geometry("250x100")
    
    Label(screen25, text = "Movie App", bg = "#336699", fg = "white", width = "300", height = "2", font = ("Arial",12)).pack()
    Label(screen25, text = "Rating added successfully").pack()
    Button(screen25, text = "Okay", command = destroy10).pack()
    
    
def addrating(film,fgenre): #opens the user list and adds the movie and the rating to the watchlist
    name = user
    score = rating.get()
    title = film
    glist = fgenre.split()
    genre = glist[0]

    
    c.execute("INSERT INTO rating(username, movie, rating, genre) \
              VALUES (?,?,?,?)",(name,title,score,genre))
    con.commit()
    
    ratingsuccess()
    
def destroy6(): #closes errortitle()
    screen13.destroy()
    
def errortitle(): #tells the user that the title is unknown and to try again
    global screen13
    screen13 = Toplevel(screen)
    screen13.title("Unknown Title")
    screen13.geometry("250x100")
    
    Label(screen13, text = "Movie App", bg = "#336699", fg = "white", width = "300", height = "2", font = ("Arial",12)).pack()
    Label(screen13, text = "Unknown Title, Please enter a new one").pack()
    Button(screen13, text = "Okay", command = destroy6).pack()
    
def searchlist(): # finds the top 10 movies with the keyword entered by the user
    title = query.get() # gets the name of the movie the user enters 
    newtitle = title.replace(" ","+") # if there are any spaces, replace them with +'s so it can be used in the URL
    url = "http://www.omdbapi.com/?apikey=ea685a0e&type=movie&s="+newtitle # this is the URL where data requests will be taken from
    response = urllib.request.urlopen(url).read() # this will read all of the data and store it in response
    json_obj = str(response,"utf-8") # this will convert the data collected into a dictionary which i can work with
    data = json.loads(json_obj) # this will hold the dictionary in the final form

    global screen11 #Makes global
    screen11 = Toplevel(screen) #Pop up window
    screen11.title("List") #Title of window
    screen11.geometry("400x500") #Window size
    
    Label(screen11, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # Header
    Label(screen11, width = "300" ,height = "1").pack() # Blank space between header and the list

    for item in data['Search']: #Looking at all the items in the dictionary
        a = (item['Title'] , item['Year']) #store the title and year of release in a
        Label(screen11, text = a).pack() # print the contents of a 

def check(film):
    title = film
    uname = user

    c.execute("SELECT friend FROM friend WHERE username = ?",(uname,))
    f = c.fetchall()
    c.execute("SELECT username FROM rating WHERE movie = ?",(title,))
    u = c.fetchall()
    Label(screen12, text = "Friends who have seen the movie: ").pack()
    for a in range(0,len(u)):
        if u[a] in f:
            Label(screen12, text = u[a]).pack()

            
def searchtitle(): #this will let the user search for a movie and will bring back information about it
    global rating
    rating = StringVar()

    title = query.get() # gets the title the user searches
    newtitle = title.replace(" ","+") #changes any spaces making them a '+' so it's recognised in the URL
    url = "http://www.omdbapi.com/?apikey=ea685a0e&t="+newtitle
    response = urllib.request.urlopen(url).read()
    json_obj = str(response,"utf-8")
    data = json.loads(json_obj)

    for item in data:
        a = (data['Response'])
    if a == "False":
        errortitle()
    else:
        global screen12 #Makes global
        screen12 = Toplevel(screen) #Pop up window
        screen12.title("Title") #Title of window
        screen12.geometry("600x500") #Window size
    
        Label(screen12, text = "Movie App", bg = "#336699",fg = "white", width = "600", height = "2", font = ("Arial",12)).pack() # Header
        Label(screen12, width = "600" ,height = "1").pack() # Blank space between header and the list

        #gets the correct movie information from data and stores them in variables so they can be accessed again
        a,b,c,d,e,h = ("Title: ",data['Title']),("Year: ",data['Year']),("Rating: ",data['Rated']),("Date Released: ",data['Released']),("Plot: ",data['Plot']),("Genre: ",data['Genre'])                                                                                                                                                                                                                          
                                                                                                                     
        Label(screen12, text = a).pack()
        Label(screen12, text = b).pack()
        Label(screen12, text = c).pack()
        Label(screen12, text = d).pack()
        Label(screen12, text = e).pack()

        global film
        global genre
        
        film = str(a[1])
        genre = str(h[1])

        
        #to get all the values for different reviews from various sites: IMDB, Metacritic, RT
        for item in data['Ratings']:
            f = (item['Source'])
            Label(screen12, text = f).pack()
            g = (item['Value'])
            Label(screen12, text = g).pack()
        Label(screen12, text = "Enter Your Own Rating: ").pack()
        rate = Entry(screen12, textvariable = rating)
        rate.pack()
        
        #Creates buttons to allow users to add a rating or add the movie to their watchlist
        Button(screen12, text = "Add to ratings", command = partial(addrating,film,genre)).pack()
        Button(screen12, text = "Add to watchlist", command = partial(addwatchlist,film,genre)).pack()

        check(film) #checks if any friends have seen the movie 
                
        
    
def destroy8(): #closes ferror()
    screen20.destroy()

def ferror(): #tells the user that the username doesnt exist
    global screen20
    screen20 = Toplevel(screen) #Create window pop up
    screen20.title("Error") # Window title
    screen20.geometry("250x100")  # Window size

    Label(screen20, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen20, text = "Username doesn't exist, please try again").pack() #Text
    Button(screen20, text = "Okay", command = destroy8).pack() # Button linked to destroy8()

def destroy7(): #closes the blank field message
    screen19.destroy()
    
def fempty(): #Tells the user that the field is blank
    global screen19
    screen19 = Toplevel(screen) #Create window pop up
    screen19.title("Empty") # Window title
    screen19.geometry("250x100")  # Window size

    Label(screen19, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen19, text = "Do not leave any fields empty").pack() #Text
    Button(screen19, text = "Okay", command = destroy7).pack() # Button linked to destroy7()

def destroy9():
    screen18.destroy()
    
def fcheck(): #checks to see if user file exists in directory
    uname = user
    name = fname.get()
    
    c.execute("SELECT username FROM users WHERE username = ?",(name,))
    valid = c.fetchall()
    if valid == []:
        ferror()
    else:
        c.execute("INSERT INTO friend(username,friend)    \
                  VALUES(?,?)",(uname,name))

    con.commit()
        

def addfriend(): #creates screen to add friend
    global fname    
    fname = StringVar()

    global screen18
    screen18 = Toplevel(screen)
    screen18.title("Add Friend")
    screen18.geometry("300x500")
    
    Label(screen18, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen18, width = "300" ,height = "1").pack() # blank space
    Label(screen18, text = "Enter Username to Add:").pack()
    name = Entry(screen18, textvariable = fname)
    name.pack()
    Button(screen18, text = "Go", command = fcheck).pack()
    
def viewlist():
    friend = fname.get()
    screen22.destroy()

    global screen23
    screen23 = Toplevel(screen)
    screen23.title("Ratings")
    screen23.geometry("300x500")
    
    Label(screen23, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen23, width = "300" ,height = "1").pack() # blank space
    
    c.execute("SELECT movie, rating FROM rating WHERE username = ?",(friend,))
    rows = c.fetchall()
    for row in rows:
        Label(screen23, text = row).pack()
    con.commit()
    

def listname():
    global fname   
    fname = StringVar()

    global screen22
    screen22 = Toplevel(screen)
    screen22.title("Choose who")
    screen22.geometry("300x500")
    
    Label(screen22, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen22, width = "300" ,height = "1").pack() # blank space
    Label(screen22, text = "Enter name of friend to view their list:").pack()
    name = Entry(screen22, textvariable = fname)
    name.pack()
    Button(screen22, text = "Go", command = viewlist).pack()


def rfind(qry,f):
    gen = qry
    friend = f
    glist = ''.join(gen)
    global screen27
    screen27 = Toplevel(screen)
    screen27.title("Recomendations")
    screen27.geometry("300x500")
    
    Label(screen27, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen27, width = "300" ,height = "1").pack() # blank space


    c.execute("SELECT movie FROM rating WHERE username = ?",(friend,))
    movies = c.fetchall()
    length = len(movies)

    for i in range(0,length):
        temp = movies[i]
        title = temp[0]
        c.execute("SELECT genre FROM rating WHERE movie = ?",(title,))
        genre = c.fetchone()
        if str(genre) == str(glist):
            Label(screen27, text = "A movie you may like is: ").pack()
            Label(screen27, text = title).pack()
    con.commit()
    

def rcheck():
    username = user
    friend = fname.get()
    screen24.destroy()

    global screen25
    screen25 = Toplevel(screen)
    screen25.title("Recomendations")
    screen25.geometry("300x500")
    
    Label(screen25, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen25, width = "300" ,height = "1").pack() # blank space

    c.execute("SELECT genre FROM rating WHERE username = ?",(friend,))
    genres = c.fetchall()
    master = screen25
    variable = StringVar(master)
    variable.set(genres[0])
    w = OptionMenu(master, variable, *genres)
    w.pack()

    def ok(f):
        friend = f
        answer = variable.get()
        rfind(answer,f)
    con.commit()
    button = Button(screen25, text = "Okay", command = partial(ok,friend)).pack()
            
def recname():
    global fname
    fname = StringVar()

    global screen24
    screen24 = Toplevel(screen)
    screen24.title("Choose Friend")
    screen24.geometry("300x500")
    
    Label(screen24, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen24, width = "300" ,height = "1").pack() # blank space
    Label(screen24, text = "Enter Friends Username:").pack()
    name = Entry(screen24, textvariable = fname)
    name.pack()
    Button(screen24, text = "Go", command = rcheck).pack()
    
def close():
    screen28.destroy()
    
def avgcalc():
    name = fname.get()
    total = 0
    
    c.execute("SELECT rating FROM rating WHERE username =?",(name,))
    rows = c.fetchall()
    length = len(rows)

    for x in range(0,length):
        val = rows[x]
        a = str(val)
        b = a.split(",")
        qlist = b[0]
        newlist = qlist.split("(")
        value = int(newlist[1])
        total = total + value

    avg = total / length

    global screen28
    screen28 = Toplevel(screen)
    screen28.title("Average")
    screen28.geometry("300x500")
    
    Label(screen28, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen28, width = "300" ,height = "1").pack() # blank space
    Label(screen28, text = "The users' average rating is:").pack()
    Label(screen28, text = avg).pack()
    Button(text = "okay", command = close).pack()
  
def avgname():
    global fname
    fname = StringVar()

    global screen27
    screen27 = Toplevel(screen)
    screen27.title("Choose Friend")
    screen27.geometry("300x500")
    
    Label(screen27, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen27, width = "300" ,height = "1").pack() # blank space
    Label(screen27, text = "Enter Friends Username:").pack()
    name = Entry(screen27, textvariable = fname)
    name.pack()
    Button(screen27, text = "Go", command = avgcalc).pack()

def gen():
    rater = score.get()
    rate = int(rater)
    friend = fname.get()

    global screen30 
    screen30 = Toplevel(screen)
    screen30.title("Movies")
    screen30.geometry("300x500")

    Label(screen30, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen30, width = "300" ,height = "1").pack() # blank space
    Label(screen30, text = "Here are some movies that you may like: ").pack()
    
    c.execute("SELECT movie FROM rating WHERE username = ?",(friend,))
    movielist = c.fetchall()
    length = len(movielist)

    for x in range(0,length):
        film = movielist[x]
        sfilm = film[0]

        c.execute("SELECT rating FROM rating WHERE movie = ?",(sfilm,))
        rating = c.fetchone()
        ratesplit = str(rating).split(',')
        rate2 = ratesplit[0]
        newrate = rate2.split("(")
        val = int(newrate[1])

        if val > rate or val == rate:
            Label(screen30, text = sfilm).pack() 


def genscore():
    global score
    global fname
    score = StringVar()
    fname = StringVar()

    global screen29
    screen29 = Toplevel(screen)
    screen29.title("Enter a Score")
    screen29.geometry("300x500")
    
    Label(screen29, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen29, width = "300" ,height = "1").pack() # blank space
    Label(screen29, text = "Enter a Score:").pack()
    val = Entry(screen29, textvariable = score)
    val.pack()
    Label(screen29, text = "Enter Friends Username:").pack()
    name = Entry(screen29, textvariable = fname)
    name.pack()
    Button(screen29, text = "Go", command = gen).pack()
    
def friends():
    name = user
    
    global screen10 #makes global
    screen10 = Toplevel(screen) #Pop up window
    screen10.title("Friends") #Title of window
    screen10.geometry("300x500") #Window size
    
    Label(screen10, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # Header
    Label(screen10, width = "300" ,height = "1").pack() # Blank space between title
    Label(screen10, text = "Friends", bg = "#336699",fg = "white", width = "300", height = "1", font = ("Arial",12)).pack() # title
    Button(screen10, text = "Add Friends", command = addfriend).pack()
    Label(screen10, width = "300" ,height = "1").pack()
    Button(screen10, text = "View Ratings", command = listname).pack()
    Label(screen10, width = "300" ,height = "1").pack()
    Button(screen10, text = "Get Recomendation", command = recname).pack()
    Label(screen10, width = "300" ,height = "1").pack()
    Button(screen10, text = "Average", command = avgname).pack()
    Label(screen10, width = "300" ,height = "1").pack()
    Button(screen10, text = "General", command = genscore).pack()
    Label(screen10, width = "300" ,height = "1").pack()
    Label(screen10, text = "Your Friends: ",width = "300" ,height = "1").pack()

    c.execute("SELECT friend FROM friend WHERE username = ?",(name,))
    rows = c.fetchall()
    for row in rows:
        Label(screen10, text = row).pack()
    con.commit()
    
def rating():
    name = user
    
    global screen9 # makes global
    screen9 = Toplevel(screen) # pop up window
    screen9.title("Rating") # window title
    screen9.geometry("300x500") # window size
    
    Label(screen9, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # header
    Label(screen9, width = "300" ,height = "1").pack() # blank space
    Label(screen9, text = "Ratings", bg = "#336699",fg = "white", width = "300", height = "1", font = ("Arial",12)).pack() # title

    c.execute("SELECT movie, rating FROM rating WHERE username = ?",(name,))
    rows = c.fetchall()
    for row in rows:
        Label(screen9, text = row).pack()
    con.commit()
    
def watchlist():
    name = user

    global screen8 # makes global
    screen8 = Toplevel(screen) # pop up window
    screen8.title("Watchlist") # window title
    screen8.geometry("300x500") # window size
    
    Label(screen8, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() # title
    Label(screen8, width = "300" ,height = "1").pack() # blank space
    Label(screen8, text = "Watchlist", bg = "#336699",fg = "white", width = "300", height = "1", font = ("Arial",12)).pack() # title

    c.execute("SELECT movie FROM watchlist WHERE username = ?",(name,))
    rows = c.fetchall()
    for row in rows:
        Label(screen8, text = row).pack()
    con.commit()
    
def destroy5():
    screen7.destroy() #close empty()
    
def destroy4():
    screen6.destroy() #close user_exists()
    
def destroy3():
    screen5.destroy() # close user_fail()
    
def destroy2():
    screen4.destroy() # close password_fail()
    
def destroy1():
    screen3.destroy() # close login_success()

def fail():
    global screen5
    screen5 = Toplevel(screen) #Pop up window
    screen5.title("Error") # Window title
    screen5.geometry("250x100") # Window Size
    
    Label(screen5, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen5, text = "Username or Password incorrect").pack() # Text
    Button(screen5, text = "Okay", command = destroy3).pack() # Button linked to destroy3()
    
def main(name):
    screen2.destroy()
    global user
    user = str(name)
    #print(user)

    global query
    global screen3

    query = StringVar()
        
    screen3 = Toplevel(screen) # Pop up Window
    screen3.title("Main Page") #Window Title
    screen3.geometry("300x500") # Window Size
    
    Label(screen3, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen3, text = "Search: ").pack()
    moviesearch = Entry(screen3, textvariable = query)
    moviesearch.pack()
    Label(screen3, width = "300", height = "1").pack()
    Button(screen3, text = "Search by title",bg = "grey", fg = "white", command = searchtitle).pack()
    Button(screen3, text = "Search for list", bg = "grey", fg = "white", command = searchlist).pack()
    Label(screen3, width = "300", height = "3").pack()
    Button(screen3, text = "Watchlist",bg = "grey", fg = "white",command = watchlist).pack()
    Label(screen3, width = "300", height = "1").pack()
    Button(screen3, text = "Ratings",bg = "grey", fg = "white", command = rating).pack()
    Label(screen3, width = "300", height = "1").pack()
    Button(screen3, text = "Friends",bg = "grey", fg = "white", command = friends).pack()
    
def login_verify(): #Verifies what the user has entered to make sure it is all correct
    global usern
    usern = StringVar()
    
    #Takes the username and password they entered in login() and stores in these variables
    username1 = user_verify.get()
    password1 = pass_verify.get()
    passh = hasher(password1)
    usern = str(username1)

    if username1 == "" or password1 == "":
        empty()
    else:
        c.execute("SELECT password FROM users WHERE username = ?",(username1,))
        password = c.fetchall()
        passw = password[0][0]
        if passw == passh:
            main(usern)
        else:
            fail()
    con.commit()

            
def empty(): #Tells the user that the field is blank
    global screen7
    screen7 = Toplevel(screen) #Create window pop up
    screen7.title("Empty") # Window title
    screen7.geometry("250x100")  # Window size

    Label(screen7, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen7, text = "Do not leave any fields empty").pack() #Text
    Button(screen7, text = "Okay", command = destroy5).pack() # Button linked to destroy5()
    
def user_exists(): # Tells the user that the username exists
    global screen6
    screen6 = Toplevel(screen) #Create window pop up
    screen6.title("Username Exists") # Window title
    screen6.geometry("250x100")  # Window size

    Label(screen6, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen6, text = "Username exists, please enter a new one").pack() #Text
    Button(screen6, text = "Okay", command = destroy4).pack() # Button linked to destroy4()

def hasher(password):
    hash1 = hashlib.md5(password.encode('utf-8')).hexdigest()
    return hash1

def sign_up_user(): #Stores the users data onto a file in a directory
    #Gathers the info entered by the user in sign_up() and stores in these varaibles
    user_info = username.get()
    pass_info = password.get()
    passw = hasher(pass_info)

    if user_info == "" or pass_info == "":
        empty()
    else:
        c.execute("SELECT username FROM users WHERE username = ?",(user_info,))
        if c.fetchall() == []:
            c.execute("INSERT INTO users(username,password) \
                      VALUES(?,?)",(user_info,passw))
            Label(screen1, text = "You have successfully signed up!").pack()
            Label(screen1, text = "Please close and login").pack()
        else:
            user_exists()
    con.commit()

    #Deletes what was entered in the textbox in sign_up()
    user_entry.delete(0,END)
    pass_entry.delete(0,END)

    

def sign_up(): #Takes in the details of the user
    global screen1
    screen1 = Toplevel(screen) #Pop up window
    screen1.title("Sign Up") # Title of Window
    screen1.geometry("300x500") # Size of Window

    #Makes these variables global
    global username
    global password
    global user_entry
    global pass_entry

    #Makes these variables have a string data type
    username = StringVar()
    password = StringVar()

    Label(screen1, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Header
    Label(screen1, text = "Please enter your details :").pack() #Text
    Label(text = "").pack()
    Label(text = "").pack()
    Label(screen1, text = "Username ").pack() #Text
    user_entry = Entry(screen1, textvariable = username)#Textbox so user can enter details
    user_entry.pack()
    Label(screen1, text = "Password ").pack()#Text
    pass_entry = Entry(screen1, textvariable = password)#Textbox so user can enter details
    pass_entry.pack()
    Button(screen1, text = "Sign Up", width = "10", height = "1", bg = "grey", fg = "white", command = sign_up_user).pack()#Button linked to sign_up_user()

def login(): #Allows the user to login taking in their details
    global screen2
    screen2 = Toplevel(screen) #Pop up Window
    screen2.title("Login")  #Title of Window
    screen2.geometry("300x500") #Size of Window

    #Makes all of these variables global
    global user_verify
    global pass_verify
    global user_entry1
    global pass_entry1

    #Makes these variables have a string data type
    user_verify = StringVar()
    pass_verify = StringVar()
 
    Label(screen2, text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Creates a header on the GUI
    Label(screen2, text = "Welcome, Please enter your details to log in:").pack()#Text
    Label(screen2, text = "Username: ").pack()#Name fot textbox
    user_entry1 = Entry(screen2, textvariable = user_verify) #Textbox so the user can enter details
    user_entry1.pack()
    Label(screen2, text = "Password ").pack()#Name for textbox
    pass_entry1 = Entry(screen2, textvariable = pass_verify) #Textbox so the user can enter details
    pass_entry1.pack()
    Label(screen2, text = "").pack()
    Button(screen2, text = "Login", width = "10", height = "1", bg = "grey", fg = "white", command = login_verify).pack() #Creates a button linked to login_verify()
        
def main_screen(): #Main menu for the app which lets the user either login or sign up
    global screen #Makes 'screen' a global variable
    screen = Tk()#Links to interpreter
    screen.geometry("300x500")#Defines the size
    screen.title("Movie App")#Title of the window
    Label(text = "Movie App", bg = "#336699",fg = "white", width = "300", height = "2", font = ("Arial",12)).pack() #Creates a header on the GUI
    Label(text = "").pack()
    Button(text = "Login", width = "10", height = "1", bg = "grey", fg = "white", command = login).pack() #Creates a button linked to login()
    Label(text = "").pack()
    Button(text = "Sign Up", width = "10", height = "1", bg = "grey", fg = "white", command = sign_up).pack() #Creates a button linked to sign_up()

    screen.mainloop()

#Main Program
main_screen() #Calls the function main_screen() which will open the GUI


