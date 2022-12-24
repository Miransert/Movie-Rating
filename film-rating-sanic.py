# Importing Sanic Library 
from sanic import Sanic as Sanic
import sanic.response as resp

app = Sanic("Movie")

# Dictionary
movies = {"Star Wars": [4.3], "Harry Potter": [3.9], "The Pianist": [4.0], "Straight Outta Compton": [3.7]}

htmlHeader = "<!DOCTYPE html></html><body>"
htmlFooter = "</body></html>"

def htmlWrap(html):
    return htmlHeader + html + htmlFooter

userName = "<form action='/start' method='post'> <input type='text' id='Name' name='Name'/> <input type='submit' value='Submit'/> </form>"

# Function to print the code and create the logic
def printing(request, search, sortParam, sortRate, errorMsg):
    global addMovieName
    global addMovieRating
    global searchFunction
    html = ""
    # Error Message
    if errorMsg != None:
        tryAgain = "<form action='/' method='route'><input type='submit' value='Try Again'></form>"
        return resp.html(htmlWrap("<h1>Error, please try again with a number between 0-10</h1>" + tryAgain))
    averageRating = 0
    
    # Sort in alphabetic order
    x = movies.keys()
    if sortParam == "title":
        x = sorted(movies)

    # Sort in rating order
    elif sortRate == "rating":
        x = []
        for (title, rating) in sorted(movies.items(), key=lambda x: x[1], reverse=True):
            x.append(title)
    
    # Search code
    if search != None:
        y = movies.keys()
        x = []
        for movieTitle in y:
            if (movieTitle.find(search) != -1):
                x.append(movieTitle)
    # Print list in order with its elements
    for movieTitle in x:
        rating = sum(movies[movieTitle])/len(movies[movieTitle])
        averageRating += rating 
        html += "<p>" + movieTitle + ": " + str("%.2f" % rating) + "</p>"
        rateNum = "<form action='/userRates' method='post'> <input type='hidden' name='title' value='" + movieTitle + "'/> <input type='text' placeholder='Rating Number' name='ratingNum'> <input type='submit' value='Rate'/></form>"
        deleteMovie = "<form action='/deletes' method='post'><input type='hidden' name='title' value='" + movieTitle + "'/><input type='submit' id='deleteButton' value='Delete'/></form>"
        userRateDelete = rateNum + deleteMovie
        html += userRateDelete
    
    averageRating = averageRating/len(x)
    
    # User adding movie and rating
    addMovieName = "<input type='text' placeholder='Movie name' id='AddMovie' name='AddMovie'/>"
    addMovieRating = "<input type='text' placeholder='Movie rating number' id='AddRating' name='AddRating'/>"
    addMovieSubmit = "<input type='submit' value='Add'/>"
    addMovieNameRating = addMovieName + addMovieRating + addMovieSubmit

    # Search and sort functions
    searchFunction = "<form action='/search' method='post'><input type='text' placeholder='Search after the movie name' size='28' id='search' name='search'/> <input type='submit' value='Search'/></form>"
    sortAlphabeticFunction = "<form action='/sortAlphabetic' method='post'> <input name='sortAlphabetic' type='submit' value='Sort in alphabetic order'/></form>"
    sortRatingFunction = "<form action='/sortRating' method='post'> <input name='sortRating' type='submit' value='Sort in rating order'/></form>"
    
    # Print all code in to the webapplication
    return resp.html(htmlWrap("<h1>Movie Ratings</h1>" + "<h3>Welcome " +
        userName1 + "</h3><p>This is a site where you can rate movies, add movies, </p>" +
        "<p>delete movies, sort them in order and search after a</p><p> specific movie. " +
        "The ratings are between 0-10. Remember, big and small letters matter</p>" + searchFunction +
        "<p>Press button to sort movie names in alfabetic order or in rating order:" +
        sortAlphabeticFunction + sortRatingFunction + "</p>" + html + "<h3>Average Rating of Movies</h3>" +
        str("%.2f" % averageRating) + "<h3>Add Movie and Rating</h3>" +
        "<form action='/adds' method='post'>" + addMovieNameRating + "</form>"))

# User enter name
@app.route("/")
async def welcome(request):
    return resp.html(htmlWrap("Hello, please write your name: " + userName))

# Start site
@app.post("/start")
async def start(request):
    global userName1
    userName1 = request.form.get("Name")
    return printing(request, None, None, None, None)

# User add movie and rating
@app.post("/adds")
async def adds(request):
    rating = float((request.form.get("AddRating")))
    if rating > 10 or rating < 0:
        return printing(request, None, None, None, "Error")
    movies[request.form.get("AddMovie")] = [float(request.form.get("AddRating"))]
    return printing(request, None, None, None, None)

# User delete a movie and rating
@app.post("/deletes")
async def deletes(request):
    movies.pop(request.form.get("title"))
    return printing(request, None, None, None, None)

# User rate a specific movie
@app.post("/userRates")
async def userRates(request):
    print(request.form)
    movieTitle = (request.form.get("title"))
    oldRating = movies[movieTitle]
    rating = float((request.form.get("ratingNum")))
    if rating > 10 or rating < 0:
        print("error?")
        return printing(request, None, None, None, "Error")
    oldRating.append(rating)
    return printing(request, None, None, None, None)

# User search function
@app.post("/search")  
async def search(request):
    search = request.form.get("search")
    return printing(request, search, None, None, None)

# Sort in alphabetic order
@app.post("/sortAlphabetic")  
async def sortAlphabetic(request):
    return printing(request, None, "title", None, None)

# Sort in rating order
@app.post("/sortRating")
async def sortRating(request):
    return printing(request, None, None, "rating", None)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)