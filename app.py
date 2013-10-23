from flask import Flask, render_template, request, Response, session, abort, jsonify
from socketio_namespaces import PlayersNamespace
from socketio import socketio_manage
import json
import redis

app = Flask(__name__)
app.config['DEBUG'] = True
r = redis.StrictRedis(host='localhost',port=6379,db=0)

@app.route('/tetris')
def index():
    return render_template('tetris.html') 

@app.route('/socket.io/<path:rest>')
def push_stream(rest):
    try:
        socketio_manage(request.environ, {'/players' : PlayersNamespace}, request)
    except:
        app.logger.error("Exception while handling socketio connection",
                     exc_info=True)

@app.route('/game',methods=['GET'])
def game():
  print('hello called')
  return Response(render_template('login.xml',mimetype='text/xml'))

@app.route('/start',methods=['GET'])
def start():
  fr = request.args.get('From')
  num = int(request.args.get('Digits'))
  print("fr is: "+str(fr)+" and num is: "+str(num))
  r.set(fr,num)
  clients = r.publish(num,num) 
  if clients != 0:
    return Response(render_template('move.xml',mimetype='text/xml'))

@app.route('/move',methods=['GET'])
def move():
  move = int(request.args.get('Digits'))
  fr = request.args.get('From') 
  print('move called with: '+str(move) + " and from: "+str(fr))
  num = r.get(fr)
  r.lpush('move_'+num,int(move))
  return Response(render_template('move.xml',mimetype='text/xml'))

