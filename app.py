# -*- coding: utf-8 -*-
from flask import Flask, jsonify,abort,make_response,request

from firebird import firebird
import json



app = Flask(__name__)


@app.route('/select', methods=['GET'])
def select():
    try:
        content = request.json
        db = content['connect']['db']
        user = content['connect']['user']
        password = content['connect']['password']
        charset = content['connect']['charset']
        sql_dialect = content['connect']['sql_dialect']
        if  ('fb_library_name' in content['connect']):
            fb_library_name = content['connect']['fb_library_name']
        else :
            fb_library_name = None
        query = content['query']

    except  Exception as e:
        return jsonify({'error': 'parameter not found: '+str(e) })

    try:
        if fb_library_name == None:
            fb = firebird(db, user,password,charset,sql_dialect)
        else:
            fb = firebird(db, user,password,charset,sql_dialect,fb_library_name)
    except  Exception as e:

        return jsonify({'error': str(e) })


    try:
        if ( ('query_params' in content) and len(content['query_params'])>0):
            query_params = content['query_params']
            res = fb.select(query,query_params)
        else :
            res = fb.select(query)

    except  Exception as e:

        return jsonify({'error': str(e) })

    return jsonify({'result': res })
    # res = json.dumps({'result': res },ensure_ascii=False, indent=4,default=str)
    # return res,200,{'content-type':'application/json'}





@app.route('/execute', methods=['POST'])
def execute():
    try:
        content = request.json

        db = content['connect']['db']
        user = content['connect']['user']
        password = content['connect']['password']
        charset = content['connect']['charset']
        sql_dialect = content['connect']['sql_dialect']
        fb_library_name = content['connect']['fb_library_name']
        query = content['query']

    except  Exception as e:
        return jsonify({'error': 'parameter not found: '+str(e) })

    try:
        fb = firebird(db, user,password,charset,sql_dialect,fb_library_name)
    except  Exception as e:


        return jsonify({'error': str(e) })


    try:
        if (('query_params' in content)  and len(content['query_params'])>0):
            query_params = content['query_params']
            res = fb.execute(query,query_params)
        else :
            res = fb.execute(query)
    except  Exception as e:

        return jsonify({'error': str(e) })

    return jsonify({'result': res })


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)

