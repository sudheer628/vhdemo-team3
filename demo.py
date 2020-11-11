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

@app.route("/list")
def lists ():
	inventory_l = inventory.find()
	a1="active"
	return render_template('index.html',a1=a1,inventory=inventory_l,t=title,h=heading)

@app.route("/")
@app.route("/uncompleted")
def tools():
	inventory_l = inventory.find({"done":"no"})
	a2="active"
	return render_template('index.html',a2=a2,inventory=inventory_l,t=title,h=heading)


@app.route("/completed")
def completed ():
	inventory_l = inventory.find({"done":"yes"})
	a3="active"
	return render_template('index.html',a3=a3,inventory=inventory_l,t=title,h=heading)

@app.route("/done")
def done():
	#Done-or-not ICON
	id=request.values.get("_id")
	task=inventory.find({"_id":ObjectId(id)})
	if(task[0]["done"]=="yes"):
		inventory.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		inventory.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir=redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Tool
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	inventory.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
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
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	id=request.values.get("_id")
	inventory.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "date":date, "pr":pr }})
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
