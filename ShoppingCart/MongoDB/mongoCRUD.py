"""
This file contains the basic crud operations required for
the shopping cart module

_id -> primary key of the collection (automatically generated by
mongoDB)
userId -> getFromUserSessions
productId -> getFromProductCatalog
productName -> getFromProductCatalog
price -> getFromProductCatalog
quantity -> get from user on GUI of shopping cart or add to cart page
"""

from pymongo import MongoClient
from pprint import pprint
mongo_cluster = "mongodb://haroon:haroon@cluster0-shard-00-00-pjkz1.mongodb.net:27017,cluster0-shard-00-01-pjkz1.mongodb.net:27017,cluster0-shard-00-02-pjkz1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

client = MongoClient(mongo_cluster)

#Database name
db = client["cmpe281"]

#Collection name
myCart = db["shoppingCart"]

#productId = get from frontend
productId = "59ef95771fe8881db48299b8"

#get quantity from frontend
quantity = 3

#API call to user database
userDetails = {
               "userName" : "haroonShareef"
              }

def getUserDetails():
    return userDetails

userId = userDetails["userName"]

"""
addTocart: This method adds a product to the cart
"""
def addToCart(productId, quantity):
    #dummy details
    #APICallToProductCatalog
    #productDetails = "curl http://localhost:5000/books/"+productId

    productDetails = {
    "_id": productId,
    "title": "cracking the coding interview",
    "price": 37.95,
    "productImage": "green book with a clock"
    }

    #document to insert
    item = {}

    #Check the schema for user database
    item['userId'] = userDetails['userName']
    item['productId'] = productDetails['_id']
    item['productName'] = productDetails['title']
    item['price'] = productDetails['price']

    #check the exact attribute name for the image
    item['productImage'] = productDetails['productImage']
    item['quantity'] = quantity
    cartId = myCart.insert_one(item).inserted_id
    #print(cartId)

"""
getCartDetails: display the contents of shopping cart for the given user
    userId: user whose cart content is to be displayed
"""
def getCartDetails(userId):
    items = myCart.find({"userId":userId})
    for item in items:
        pprint(item)

"""
findProduct : returns the details of a product for
              a given user from the database
    userId    : user id for whom product details are needed
    productId : product whose details are required
"""
def findProduct(userId, productId):
    item = {}
    item = myCart.find_one({"userId":userId, "productId" : productId})
    return item

#addToCart(productId,quantity)
#pprint(myCart.find_one())

#getCartDetails(userId)
pprint(findProduct(userId, productId))

#create a method to update
"""
updateCart : This method updates the user cart
    userId:
    productId:
    newQty:

if newQty is 0 : call the delete method and remove this item from cart
"""
def updateCart(userId, productId, newQty):
    if newQty == 0:
        deleteProduct(userId, productId)
    else:

#write a method to delete an item from the cart
"""
deleteProduct: This method removes a product from the cart
    userId:
    productId:
"""
def deleteProduct(userId, productId):
    result = myCart.delete_one({"userId":userId, "productId" : productId})
    pprint(dir(result))
    pprint(result)


#write a method to create after checking the availability in db, if already
#present update the quantity

deleteProduct(userId, productId)
pprint(findProduct(userId, productId))
