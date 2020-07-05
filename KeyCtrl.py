# coding: utf-8
from __future__ import division
from objc_util import *
import ui
from console import hud_alert
import keyboard
import clipboard

#page
pageArray = [['cL','cR','home','end'],['del','tab','copy','paste']]

class CustomView(object):
	def switch_page(self, sender):
	    index = sender.superview['page'].selected_index
	    if index == 0:
	    	for i in range(4):
	    		X = (55+1)*i
	    		v[pageArray[0][i]].frame = \
	    			(X,  00, 55, 30)
	    		v[pageArray[1][i]].frame = \
	    			(X, -50, 55, 30)
	    elif index == 1:
	    	for i in range(4):
	    		X = (55+1)*i
	    		v[pageArray[1][i]].frame = \
	    			(X,  00, 55, 30)
	    		v[pageArray[0][i]].frame = \
	    			(X, -50, 55, 30)

	def move_cL(self, sender):
	    keyboard.play_input_click()
	    keyboard.move_cursor(-1)

	def move_cR(self, sender):
	    keyboard.play_input_click()
	    keyboard.move_cursor(1)

	def move_home(self, sender):
	    keyboard.play_input_click()
	    locale = len(keyboard.get_input_context()[0])
	    keyboard.move_cursor(-locale)

	def move_end(self, sender):
	    keyboard.play_input_click()
	    locale = len(keyboard.get_input_context()[1])
	    keyboard.move_cursor(locale)

	def act_del(self, sender):
	    keyboard.play_input_click()
	    if keyboard.get_input_context()[1]:
	    	keyboard.move_cursor(1)
	    	keyboard.backspace(1)

	def insert_tab(self, sender):
	    keyboard.play_input_click()
	    keyboard.insert_text('	')

	def act_copy(self, sender):
	    keyboard.play_input_click()
	    if keyboard.get_selected_text():
	    	selected = keyboard.get_selected_text()
	    	clipboard.set(selected)
	    	console.hud_alert('Copied','',0.45)

	def act_paste(self, sender):
	    keyboard.play_input_click()
	    if clipboard.get():
	    	keyboard.insert_text(clipboard.get())


#calc -------------------
shows_result = False

def calc_tapped(sender):
	keyboard.play_input_click()
	'@type sender: ui.Button'
	# Get the button's title for the following logic:
	t = sender.title
	global shows_result
	# Get the labels:
	label = sender.superview['label1']
	label2 = sender.superview['label2']
	if t in '0123456789':
		if shows_result or label.text == '0':
			# Replace 0 or last result with number:
			label.text = t
		else:
			# Append number:
			label.text += t
	elif t == '.' and label.text[-1] != '.':
		# Append decimal point (if not already there)
		label.text += t
	elif t in '+-÷×':
		if label.text[-1] in '+-÷×':
			# Replace current operator
			label.text = label.text[:-1] + t
		else:
			# Append operator
			label.text += t
	elif t == 'AC':
		# Clear All
		label.text = '0'
	elif t == 'C':
		# Delete the last character:
		label.text = label.text[:-1]
		if len(label.text) == 0:
			label.text = '0'
	elif t == '=':
		# Evaluate the result:
		try:
			label2.text = label.text + ' ='
			expr = label.text.replace('÷', '/').replace('×', '*')
			label.text = str(eval(expr))
		except (SyntaxError, ZeroDivisionError):
			label.text = 'ERROR'
		shows_result = True
	if t != '=':
		shows_result = False
		label2.text = ''

def calc_copy(sender):
	'@type sender: ui.Button'
	t1 = sender.superview['label1'].text
	t2 = sender.superview['label2'].text
	if t2:
		text = t2 + ' ' + t1
	else:
		text = t1
	clipboard.set(text)
	hud_alert('Copied')

v = ui.load_view()

cv = CustomView()
v['page'].action  = cv.switch_page
v['cL'].action    = cv.move_cL
v['cR'].action    = cv.move_cR
v['home'].action  = cv.move_home
v['end'].action   = cv.move_end
v['del'].action   = cv.act_del
v['tab'].action   = cv.insert_tab
v['copy'].action  = cv.act_copy
v['paste'].action = cv.act_paste

if keyboard.is_keyboard():
	keyboard.set_view(v,'minimized')
	
else:
	v.present('sheet')
