import sys
import os
from flask import Flask, request, jsonify
import coffee_rag_hosted
from credential_utilties.environment import setTritonEnvironmentVariablesFromConfig
from credential_utilties.environment import setDataEnvironmentVariablesFromConfig

web_app = Flask(__name__)

def main():
    print("Starting web server for hosted coffee app")
    setDataEnvironmentVariablesFromConfig(sys.argv[1])
    coffee_rag_hosted.init()
    setTritonEnvironmentVariablesFromConfig(sys.argv[1])
    web_app.run(host="0.0.0.0", port=8095, debug=False)

@web_app.route('/',methods = ["GET"])
def processclaim():
    try:
        query = request.args["request"]
        response = coffee_rag_hosted.run(query)
        return response[0]
    except Exception as e:
        print(e)
        return jsonify({"Status":"Failure --- some error occured"})
    
if __name__ == "__main__":
    main()
