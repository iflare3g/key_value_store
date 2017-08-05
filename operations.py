class Operations():
  
  def __init__(self):
    #SET OF OPERATIONS (set(args),get(args)...)
    self.ops = []
  
  #EVERYTIME NEW COMMAND IS LAUNCHED, IT'S APPENDED TO OPERATION'S SET. IF COMMAND IS ALREADY SAVED, IT'S NOT APPENDED INTO OPS[]
  def add_step(self,command,*args):
    self.ops.append((command,args))
  
  #RELAUNCH EVERY COMMANDS FROM THE LAST ONE LAUNCHED TO THE FIRST ONE.
  def rollback(self):
    for command in reversed(self.ops):
      #THIS IS EQUAL TO set(key,value) FOR EXAMPLE. GENERIC = command(*args)
      command[0](*command[1])