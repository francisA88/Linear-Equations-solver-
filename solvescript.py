#Make sure TextInput class is imported in a kv file
'''This file is not meant to be run separately and is used somewhere in mainlayout.kv'''
def solve():
	n=0
	noOfTextChildren = len(ef.children)-1
	for children in ef.children:
		for child in children.children:
			if issubclass(child.__class__, TextInput):
				if child.text != "":
					app.eqns.append(child.text)
	
	result = app.solve()
	disp = Factory.ResultDisplay(
			title="Results",
			text_button_ok="close",
			text=f"[color=#0000ee][size=34][i]{result}[/i][/size][/color]"
			)
	disp.events_callback = lambda x,y: disp.dismiss()
	disp.size_hint = .8, .7
	disp.open()
solve()