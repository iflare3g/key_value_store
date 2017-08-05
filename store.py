import sys
from operations import Operations

class Store:
  #ALL OF THE COMMANDS ALLOWED
  _commands = ['SET','GET','EQUALTO','UNSET','BEGIN','COMMIT','ROLLBACK','END']
  
  def __init__(self):
    # _store_ is the key/value database
    # _nest_ops is a set of transaction
    self._store_ = {}
    self._nest_ops = []
    
  def run(self,query):
    #SPLIT INPUT ON WHITESPACE, SO WORDS[0] IS THE COMMAND and WORDS[1:] ALL OF THE ARGS.
    words = query.split(' ')
    command,args = words[0],words[1:]
    try:
        if command in Store._commands:
            return Store.__dict__[command.lower()](self,*args) #Store.__dict__ ALLOWS MYSELF TO RUN METHODS BASED ON ITS KEY/VALUE PAIR.
        else:
            return 'Error on typing the command, please choose one in {}'.format(self._commands)
    except TypeError as err:
        print 'ERROR Traceback -> {}'.format(str(err))
        
  #WHAT USER SEES ON THE SCREEN.
  def shell_to_display(self):
    store = Store()
    while 1:
        operation = sys.stdin.readline().strip() #READ YOUR INPUT
        if operation is not None:
            result = store.run(operation)
            if result is not None:
                print result
    
    
  #METHOD USED TO CHECK IF LIST OF OPERATIONS IS EMPTY OR NOT
  def is_empty(self):
    return len(self._nest_ops) == 0


  #METHOD TO SET KEY,VALUE INTO YOUR STORE - USAGE: SET key value
  def set(self,key,value,to_save=True):
    if not self.is_empty() and to_save:
      operations = self._nest_ops[-1]
      if self._store_.has_key(key):
        operations.add_step(self.set,key,self.get(key),False)
      else:
        operations.add_step(self.unset,key,False)
    
    self._store_[key] = value
    
  #METHOD USED TO GET VALUE BY KEY, IF KEY DOESN'T EXIST, SHOW NULL. USAGE: GET key
  def get(self,key):
    return self._store_.get(key,None) or 'NULL'
   
  #METHOD USED TO GET HOW MANY VALUES ARE EQUALS INTO THE STORE - USAGE: EQUALTO value
  def equalto(self,value):
    _count = 0
    try:
        #I'VE CHOOSEN TO ACCEPT INTEGERS NUMBER ONLY.
        value = int(value)
        for key in self._store_.keys():
            if int(self._store_.get(key,None)) == value:
                _count +=1
        return _count or 0
    except ValueError as err:
        print 'ERROR Only integers number are allowed! Traceback ->' + str(err)
        
        
  #METHOD USED TO DELETE VALUE BY KEY. USAGE: UNSET key
  def unset(self,key,to_save=True):
    if not self.is_empty() and to_save:
      operations = self._nest_ops[-1]
      if self._store_.has_key(key):
        operations.add_step(self.set,key,self.get(key),False)
        
    if self._store_.has_key(key):
        del self._store_[key]
    else:
        return 'KEY NOT EXISTS'
      
  #BEGIN NEW TRANSACTION BLOCK. USAGE: BEGIN with no args
  def begin(self):
    self._nest_ops.append(Operations())
   
  #METHOD USED TO APPLY ALL CHANGES. IF NO TRANSACTION IS OPEN, RETURN MESSAGE
  def commit(self):
    if not self.is_empty():
      self._nest_ops = []
    else:
      return 'NO TRANSACTION'

  #METHOD USED TO REDO LAST SET OF OPERATIONS. USAGE: ROLLBACK with no args
  def rollback(self):
    if not self.is_empty():
      self._nest_ops.pop().rollback()
    else:
      return 'NO TRANSACTION'
    
  

  #METHOD USED TO END THE PROGRAM. USAGE: END with no args
  def end(self):
    return sys.exit()
      


if __name__ == '__main__':
   Store().shell_to_display()