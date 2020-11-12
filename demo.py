import os
from flask import Flask, render_template,request,redirect,url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
title = "Vodafone Group - Hackathon Chalenge"
heading = "DevOps Inventory Manager"

client = MongoClient("mongodb+srv://sudheer:12maialen69@team-3.ascgs.mongodb.net")
db = client.vhdemo
inventory = db.devops

def redirect_url():
    return request.args.get('next') or request.referrer or url_for('index')

@app.route("/")
@app.route("/list")
def lists ():
	inventory_l = inventory.find()
	a1="active"
	return render_template('index.html',a1=a1,inventory=inventory_l,t=title,h=heading)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Tool
	tag=request.values.get("tag")
	contact=request.values.get("contact")
	market=request.values.get("market")
	link=request.values.get("link")
	best_practice=request.values.get("best_practice")
	inventory.insert({ "tag":tag, "contact":contact, "market":market, "link":link, "best_practice":best_practice})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Tool with various references
	key=request.values.get("_id")
	inventory.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=inventory.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
	#Updating a Tool with various references
	tag=request.values.get("tag")
	contact=request.values.get("contact")
	market=request.values.get("market")
	link=request.values.get("link")
	best_practice=request.values.get("best_practice")
	id=request.values.get("_id")
	inventory.update({"_id":ObjectId(id)}, {'$set':{ "tag":tag, "contact":contact, "market":market, "link":link, "best_practice":best_practice }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Tool with various references
	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		inventory_l = inventory.find({refer:ObjectId(key)})
	else:
		inventory_l = inventory.find({refer:key})
	return render_template('searchlist.html',inventory=inventory_l,t=title,h=heading)

if __name__ == "__main__":
    app.run()
