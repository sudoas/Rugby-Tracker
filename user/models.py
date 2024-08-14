from flask import Flask, jsonify

class User:

    def register(self):

        user = {
            "_id": "",
            "username": "",
            "password": "",
            "email": "",
        }

        return jsonify(user), 200