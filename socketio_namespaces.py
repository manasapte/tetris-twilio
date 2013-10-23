from socketio.namespace import BaseNamespace
import redis
import signal
import json
import time

r = redis.StrictRedis(host='localhost', port=6379, db=0)

class PlayersNamespace(BaseNamespace):
  def recv_connect(self):
    self.ps = r.pubsub()


  def on_move(self):
    move = r.rpop('move_'+str(self.id))
    if move is not None:
      self.emit('move',move)
    
  def on_start(self):
    self.ps.subscribe([self.id])
    for item in self.ps.listen():
      print 'got an item from listen'+str(item)
      if(item.get('type') == 'message'):
        print "item data: "+str(item.get)
        if item.get('data') == self.id:
          self.emit('start')
          break
  
  def on_login(self, packet):
    try:
      self.id = r.get('sessionid')
      r.incr('sessionid')
      print "logged in with id: "+str(self.id)
      self.emit('login',self.id)
    except:
      print "some exception"
      raise


  def disconnect(self, *args, **kwargs):
    print "Got a socket disconnection" # debug
    self.ps.unsubscribe()
    if self.id is not None:
        r.delete(self.id)
    super(PlayersNamespace, self).disconnect(*args, **kwargs)

