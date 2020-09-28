from flask import *
from threading import Thread, Lock
import queue
from time import sleep, ctime



app = Flask(__name__)

a = 0
b = 0
c = ctime()

a_lock = Lock()
b_lock = Lock()
c_lock = Lock()


# MAIN STREAM (generator that gets used in template)
def stream():
	global a, b, c
	while True:
		yield [a,b,c]
		sleep(1)

# SUB STREAMS (all get fed into the main stream)
def stream_source_1():
	global a, b
	while True:
		sleep(1)
		
		a_lock.acquire()
		a += 1
		a_lock.release()
				
def stream_source_2():
	global a, b
	while True:
		sleep(3)
		
		b_lock.acquire()
		b += 1
		b_lock.release()
		
def stream_source_3():
	global c
	while True:
		sleep(1)
		c_lock.acquire()
		c = ctime()
		c_lock.release()

def stream_template(template_name, **context):
	app.update_template_context(context)
	t = app.jinja_env.get_template(template_name)
	rv = t.stream(context)
	rv.disable_buffering()
	return rv
		
		
		
@app.route("/", methods=['GET', 'POST'])
def index():
	
	return Response(stream_with_context(stream_template('index.html', stream=stream())))
	




if __name__ == "__main__":
	try:
	
		main_thread = Thread(target=app.run)
		#main_thread = Thread(target=stream)
		thread1 = Thread(target=stream_source_1)
		thread2 = Thread(target=stream_source_2)
		thread3 = Thread(target=stream_source_3)

		main_thread.start()
		thread1.start()
		thread2.start()
		thread3.start()
		
	except KeyboardInterrupt:
		pass