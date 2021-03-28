import flask
from flask import Flask, request, send_from_directory, jsonify, current_app
import requests
import json


app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return current_app.send_static_file("index.html")


@app.route("/privacy", methods=["GET"])
def privacy():
    return current_app.send_static_file("privacy.html")



@app.route("/error-page", methods=["GET"])
def error_page():
    return current_app.send_static_file("error.html")


@app.route("/api/ipo-results", methods=["POST"])
def get_ipo_results():
    print(request.json["boids"])

    headers = {"content-type": "application/json"}

    companies_response = requests.request(
        "GET",
        "https://iporesult.cdsc.com.np/result/companyShares/fileUploaded",
        headers=headers,
    )
    company = json.loads(companies_response.text)["body"][-1]
    results = []
    for boid in request.json["boids"]:
        print(boid)
        payload = json.dumps({"companyShareId": company["id"], "boid": boid})
        response = requests.request(
            "POST",
            "https://iporesult.cdsc.com.np/result/result/check",
            data=payload,
            headers=headers,
        )
        results.append(json.loads(response.text)["success"])
        print(json.loads(response.text)["success"])
    return jsonify({"company_name": company["name"], "results": results})


app.run()