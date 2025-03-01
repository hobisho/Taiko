import inspect

def start_wrapper(start, *args, **kwargs):
  def wrapper(func, *args, **kwargs):
    start() # start function

    return func
  
  return wrapper

def main(*args, **kwargs):
  caller_frame = inspect.currentframe().f_back
  caller_globals = caller_frame.f_globals
  caller_module_name = caller_globals['__name__']

  func = args[0]
  
  def wrapper(*args, **kwargs):
    if caller_module_name == '__main__':
      func()

  return wrapper