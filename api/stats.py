import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required

from model.users import Post

stats_api = Blueprint('stats_api', __name__,
                   url_prefix='/api/stats')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(stats_api)
class UserAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()     
            ''' Avoid garbage in, error checking '''
            # validate name
            playerName = body.get('playerName')
            if playerName is None or len(playerName) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400
            # look for password and dob
            goals = body.get('goals')
            number = body.get('number')

    

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Post( playerName = playerName, uid=uid, goals=goals, number=number)

            created_post = uo.create()
# success returns json of user
            if created_post:
                return jsonify(created_post.read())
            # failure returns error
            return {'message': f'Processed {playerName}, either a format error or User ID {uid} is duplicate'}, 400
            
            ''' Additional garbage error checking '''
            # set password if provided
            # convert to date type
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            playerName = uo.create()
            # success returns json of user
            if playerName:
                return jsonify(playerName.read())
            # failure returns error
            return {'message': f'Processed {playerName}, either a format error or User ID {uid} is duplicate'}, 400

        def get(self): # Read Method
            users = Post.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps
        
    
  

    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = Post.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    # api.add_resource(_Security, '/')
    