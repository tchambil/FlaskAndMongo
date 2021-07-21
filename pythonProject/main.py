from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
import os

app = Flask(__name__)
title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mitienda    #Select the database
todos = db.tweets #Select the collection name

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/list")
def lists ():
	#Display the all tweets
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/")
def tweets ():
	todos_l = todos.find({"user_id":64496036})
	a2="active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/action", methods=['POST'])
def action ():
	#Adding a Tweet
	text=request.values.get("text")
	user_id=request.values.get("user_id")
	date=request.values.get("date")
	user_name=request.values.get("user_name")
	todos.insert({ "user_name":user_name, "text":text, "date":date, "user_id":user_id, "retweeted":False})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	tweet=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tweets=tweet,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Task with various references
	text=request.values.get("text")
	user_name=request.values.get("user_name")
	id=request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "text":text, "user_name":user_name}})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a tweets with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
