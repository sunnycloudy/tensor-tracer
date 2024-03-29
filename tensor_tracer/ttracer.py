import sys
import linecache
import os
import inspect
import numpy
import torch
import ntpath
import textwrap 

#def trace_var_wrap_print(k, line):
#  print("\\\n".join(["[var:]" + k + l for l in textwrap.fill(line, 10).split("\n")]))

def print_self(obj):
  #print("------ print self ------")
  #print(len(list(obj.__dict__)))
  for k,v in obj.__dict__.items():
    k = '{:20}'.format(k)
    if type(v) ==  torch.Tensor:
      print("[var:] "+k+" [torch.Tensor#size:"+str(v.size())+"]")
      #trace_var_wrap_print(k, " [torch.Tensor#size:"+str(v.size())+"]")
    elif type(v) ==  numpy.ndarray:
      print("[var:] "+k+" [numpy.ndarray#shape:"+str(v.shape)+"]")
      #trace_var_wrap_print(k, " [numpy.ndarray#shape:"+str(v.shape)+"]")
    elif type(v) == list:
      print("[var:] "+k+" [list#length:"+str(len(v))+"]")
      #trace_var_wrap_print(k, " [list#length:"+str(len(v))+"]")
    elif type(v) == dict:
      print("[var:] "+k+" [dict#length:"+str(len(v))+"]")
      #trace_var_wrap_print(k, " [dict#length:"+str(len(v))+"]")
    elif type(v) == float or type(v) == int:
      print("[var:] "+k+ " [float or int#value:"+str(v)+"]")
      #trace_var_wrap_print(k, " [float or int#value:"+str(v)+"]")
    elif type(v) == str:
      print("[var:] "+k+ " [str#value:\""+str(v)+"\"]")
      #trace_var_wrap_print(k, " [str#value:\""+str(v)+"\"]")
    elif type(v) == bool:
      print("[var:] "+k+ " [bool#value:\""+str(v)+"\"]")
      #trace_var_wrap_print(k, " [bool#value:\""+str(v)+"\"]")
    else:
      print("[var:] "+k+ " [type not included:]" + str(type(v)) + "<id:" + str(id(v)) + ">")
      #trace_var_wrap_print(k, " [type not included:]" + str(type(v)) + "<id:" + str(id(v)) + ">")


def print_items(frame):
#      return frame.f_locals.items() 
  for k,v in frame.f_locals.items():
    k = '{:20}'.format(k)
    if type(v) ==  torch.Tensor:
      print("[arg:] "+k+" [torch.Tensor#size:"+str(v.size())+"]")
    elif type(v) ==  numpy.ndarray:
      print("[arg:] "+k+" [numpy.ndarray#shape:"+str(v.shape)+"]")
#   print xxx
    elif type(v) == list:
      print("[arg:] "+k+" [list#length:"+str(len(v))+"]")
    elif type(v) == dict:
      print("[var:] "+k+" [dict#length:"+str(len(v))+"]")
#   print xxx
    elif type(v) == float or type(v) == int:
      print("[arg:] "+k+ " [float or int#value:"+str(v) + "]")
    elif type(v) == str:
      print("[var:] "+k+ " [str#value:\""+str(v)+"\"]")
#   print (xxx)
#   print xxx
    elif type(v) == bool:
      print("[var:] "+k+ " [bool#value:\""+str(v)+"\"]")
    elif k == "self":
      print_self(v)
    else:
      print("[arg:] "+k+ " [type not included:]" + str(type(v)) + "<id:" + str(id(v)) + ">")
#   print xxx

#还需要一个记录数据的代码.

def _get_func_name(frame):
    module_name = inspect.getmodule(frame).__name__
    func_name = frame.f_code.co_name
    arginfo = inspect.getargvalues(frame)
    if len(arginfo.args) > 0 and arginfo.args[0] == "self":
        func_name = "%s#%s" % (arginfo.locals["self"].__class__.__name__, func_name)
    return func_name

trace_account = 0
trace_account_max = 10000


trace_repeat = {}
def traceit(frame, event, arg, indent=[0]):
    global target_files
    global trace_account
    global trace_account_max
    global trace_repeat
    global trace_width
    if trace_account == trace_account_max:
      exit(0)
    if event == "call":
        f_name = frame.f_code.co_filename
        if f_name in  target_files and frame.f_code.co_name not in trace_ignore_functions:
          print("--"*6+frame.f_code.co_filename+"--"*6)
          trace_repeat[_get_func_name(frame)] = {}
          trace_account += 1
          format_trace_account =  '{:>5d}'.format(trace_account)
          indent[0] += 4
          #print("-" * indent[0] + "> [ call function", frame.f_code.co_name, "]")
          #print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(trace_account)  + "-" * indent[0] + "> [ call function",_get_func_name(frame), "]")
          print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account)  + "  |" + "[ call function",_get_func_name(frame), "]")
          #print(frame.f_code.co_varnames)
          #if len(frame.f_code.co_varnames) > 2:
          #  print(exec(frame.f_code.co_varnames[1]))
          #print(frame.f_code.co_names)
          #print(_get_value(frame))
          print_items(frame)
          #print(frame.f_locals.items())

          lineno = frame.f_lineno
          format_lineno = '{:>4d}'.format(lineno)
          line = linecache.getline(frame.f_code.co_filename, lineno)
          #print(str(trace_account) + " " * indent[0] + "  |line %d|    %s" % (lineno, line.rstrip()))
          #print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) + "  |L %s|    %s" % (format_lineno, line.rstrip()))
          print("\\\n".join(['{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) +  "  |L %s|    %s" % (format_lineno, l.rstrip()) for l in textwrap.fill(line, trace_width).split("\n")]))


    elif event == "return":
        f_name = frame.f_code.co_filename
        if f_name in target_files and frame.f_code.co_name not in trace_ignore_functions:
          #print(target_file)
          #print("--"*6+frame.f_code.co_filename+"--"*6)
          trace_account += 1
          format_trace_account =  '{:>5d}'.format(trace_account)
          #print("-" * indent[0] + "> [ call function",_get_func_name(frame), "]")
          #print("<" + "-" * indent[0], "[ exit function", frame.f_code.co_name, "]")
          #print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) + "<" + "-" * indent[0], "[ exit function", _get_func_name(frame), "]")
          print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) + "  |" + "[ exit function", _get_func_name(frame), "]")

          indent[0] -= 4

    if event == "line":
        f_name = frame.f_code.co_filename
        if f_name in target_files and frame.f_code.co_name not in trace_ignore_functions:
          #print(target_file)

          lineno = frame.f_lineno
          format_lineno = '{:>4d}'.format(lineno)
          if f_name in  trace_ignore_lines and lineno in  trace_ignore_lines[f_name]:
            if lineno in trace_repeat[_get_func_name(frame)]:
              "do nothing"
              trace_repeat[_get_func_name(frame)][lineno] += 1
            else:
              trace_repeat[_get_func_name(frame)][lineno] = 1   #只打印这么一次
              trace_account += 1
              format_trace_account =  '{:>5d}'.format(trace_account)
              line = linecache.getline(f_name, lineno)
              #print('{:20}'.format("[only once:]") + str(format_trace_account) + " " * indent[0] + "  |L %s|    %s" % (format_lineno, line.rstrip()))
              
              print("\\\n".join(['{:20}'.format("[only once]") + ":" + str(format_trace_account) +  "  |L %s|    %s" % (format_lineno, l.rstrip()) for l in textwrap.fill(line, trace_width).split("\n")]))

          else:
            trace_account += 1
            format_trace_account =  '{:>5d}'.format(trace_account)
            line = linecache.getline(f_name, lineno)
            #print(ntpath.basename(f_name) + ":" + str(trace_account) + " " * indent[0] + "  |line %d|    %s" % (lineno, line.rstrip()))
            #print('{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) + "  |L %s|    %s" % (format_lineno, line.rstrip()))
            print("\\\n".join(['{:20}'.format(ntpath.basename(f_name)) + ":" + str(format_trace_account) +  "  |L %s|    %s" % (format_lineno, l.rstrip()) for l in textwrap.fill(line, trace_width).split("\n")]))
          #print(frame.f_code.co_varnames)
          #print(frame.f_locals.items())
          #发生return时清0

    return traceit

sys.settrace(traceit)
target_files = []
trace_ignore_lines = {}
trace_ignore_functions = []

def start(path):
  print(path)

  global target_file
  global target_files
  global trace_account_max
  global trace_ignore_lines
  global trace_ignore_functions
  global trace_width

  pwd = os.getcwd()
  #print(pwd)
   
  import sys
  sys.path.insert(0, pwd)
  #print(sys.path)

  
  target_files.append(os.path.abspath(path))  #"./test4.py"
  print("------------", target_files[0], "------------")


  import sys
  sys.path.insert(0, pwd)
  #print(sys.path)


  config = __import__("tt_config")
  target_files = target_files + [ os.path.abspath(path_in_config) for path_in_config in config.target_files]
  trace_account_max = config.maxline
  trace_ignore_functions = config.ignore_functions
  trace_width = config.trace_width

  #改造key名中的路径,为abspath
  for key in config.ignore_lines:
    trace_ignore_lines[os.path.abspath(key)] = config.ignore_lines[key]
   

  print(target_files)
  module_name = os.path.splitext(os.path.basename(target_files[0]))[0]
  print(module_name)
  module_to_trace = __import__(module_name)  #去掉文件名的路径和后缀
  module_to_trace.main()

  


