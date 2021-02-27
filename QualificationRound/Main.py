class Street:
	def __init__(self, id, start, end, name, duration):
		self.id = id
		self.start = start
		self.end = end
		self.name = name
		self.duration = duration


class Intersection:
	def __init__(self, id, incoming):
		self.id = id
		self.incoming = incoming


def readFile(fileName):
	file = open("input/" + fileName, "r")

	def readNextLine():
		return file.readline().split()

	duration, numIntersection, numStreets, numCars, points = list(map(int, readNextLine()))
	streets = []

	for i in range(numStreets):
		tokens = readNextLine()
		streets.append(Street(i, int(tokens[0]), int(tokens[1]), tokens[2], int(tokens[3])))
		
	file.close()

	return streets, duration, numIntersection, numStreets, numCars, points


def writeFile(fileName, intersections):
	space = " "
	newline = "\n"

	file = open("output/" + fileName, "w")

	file.write(str(len(intersections)) + newline)
	for intersection in intersections:
		file.write(str(intersection.id) + newline)
		file.write(str(len(intersection.incoming)) + newline)
		for street in intersection.incoming:
			file.write(street + space + "1" + newline)
	
	file.close()
	
def main():
	#a, b, c, d, e, f
	fileName = "f" + ".txt"
	streets, duration, numIntersection, numStreets, numCars, points = readFile(fileName)

	intersections = []
	for i in range(numIntersection):
		intersections.append(Intersection(i, []))

	for i in range(numStreets):
		intersection = streets[i].end
		street = streets[i].name
		intersections[intersection].incoming = intersections[intersection].incoming + [street]

	writeFile(fileName, intersections)


main()