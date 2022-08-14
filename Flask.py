from flask import *
app = Flask(__name__)


class Model:
    
    def collection(): # return The Table
        import pymongo
        return pymongo.MongoClient("mongodb+srv://AhmedWaheed:345678901@cluster0.yw7b3uu.mongodb.net/?retryWrites=true&w=majority") ["mydatabase"] ["URL"]
    
    def search(dic):
        return Model.collection().count_documents(dic)
    
    def write(dic):
        Model.collection().insert_one(dic)
        
    def read(dic):
        return Model.collection().find_one(dic)
    
    def readAll():
        return Model.collection().find()
        
    
    
class Controller:
    
    def shorten(): # convert long link to short : may using Hashing , Random or Counter
        long = request.args.get('long')
        
        if Model.search({ "long":long }) != 0 :
            message = "Already shorten before"
        
        else:
            from random import randint
            while True :
                short = str( randint(1000000,9999999) ) #inclusive : len=7
                if Model.search({ "short":short }) == 0 : # unique short link 
                    break
            Model.write({ "long":long , "short":short })
            message = "Shorten successfully"
            
        short = str (  Model.read({ "long":long }) ['short']  )
        return json.dumps({ "message":message , "short":short })
    
    
    def long(): # return main long link for specific short one
        short = request.args.get('short')
            
        if Model.search({ "short":short }) == 0 :
            long = "not found"
        else:
            long = str(  Model.read({ "short":short }) ['long']  )
        
        return json.dumps({ "long":long })
    
    
    def getLinks(): # print Table
        return json.dumps( str( ( list( Model.readAll() ) ) ) )



@app.route('/') 
def home():
    try:
        return Controller.shorten()
    except:
        return 'catch'

@app.route('/getMainLink') 
def getMainLink():
    try:
        return Controller.long()
    except:
        return 'catch'
        
@app.route('/getAll') 
def getAll():
    try:
        return Controller.getLinks()
    except:
        return 'catch'


if __name__ == '__main__':
    app.run(debug=True)