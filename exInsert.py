def insert_example():
	while len(ef.children) > self.var+1:
		ef.remove_widget(ef.children[0])
	while len(ef.children) < self.var+1:
		ef.add_widget(Factory.Group())
	ch =[]
	for children in ef.children:
		for child in children.children:
			if issubclass(child.__class__, Factory.TextInput):
				ch.append(child)
	print(ch)
	ex2 = ["x + y = 3", "2x - y = 3"]
	ex3 = [
		"x + y + z = 12",
		"2x - 2y +3z =10",
		"8x - y - z = 14"
	]
	if self.var == 2:
		ex = ex2
	elif self.var==3:
		ex = ex3
	for i in range(len(ex)):
		ch[i].text = ex[i]

insert_example()

