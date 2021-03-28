import flask
from flask import Flask, request, send_from_directory, jsonify, current_app, render_template
import requests
import json


app= Flask(__name__, static_folder="templates")




@app.route("/")
def home():
    return render_template("/index.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")



@app.route("/error-page")
def error_page():
    return render_template("/error.html")


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
