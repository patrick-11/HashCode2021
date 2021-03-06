class Street:
	def __init__(self, start, end, duration):
		self.start = start
		self.end = end
		self.duration = duration
		self.waitingCars = 0
		self.passingCars = 0


class Car:
	def __init__(self, numStreets, path):
		self.numStreets = numStreets
		self.path = path


class Intersection:
	def __init__(self, incomingStreets):
		self.incomingStreets = incomingStreets


def readFile(fileName):
	file = open("input/" + fileName, "r")

	def readNextLine():
		return file.readline().split()

	duration, numIntersection, numStreets, numCars, points = list(map(int, readNextLine()))
	streets, cars = {}, {}

	for i in range(numStreets):
		tokens = readNextLine()
		streets.update({tokens[2]: Street(int(tokens[0]), int(tokens[1]), int(tokens[3]))})
		
	for i in range(numCars):
		tokens = readNextLine()
		temp = tokens.pop(0)
		path = tokens
		cars.update({i: Car(int(temp), path)})
		
	file.close()
	return streets, cars, duration, numIntersection, numStreets, numCars, points


def writeFile(fileName, schedule):
	space = " "
	newline = "\n"

	file = open("output/" + fileName, "w")
	file.write(str(len(schedule)) + newline)

	for intersection, streets in schedule.items():
		file.write(str(intersection) + newline)
		file.write(str(len(streets)) + newline)
		for street, time in streets.items():
			file.write(street + space + str(time[0]) + newline)
	file.close()


def main():
	# Choose file: a, b, c, d, e, f
	fileName = "a.txt"

	# Read Input file
	streets, cars, duration, numIntersection, numStreets, numCars, points = readFile(fileName)

	intersections, schedule = {}, {}

	# Calculate passing and waiting cars on each street (ignoring the last street in car's path)
	for car, values in cars.items():
		for i, street in enumerate(values.path):
			if i == 0:
				streets.get(street).waitingCars += 1
			if i < len(values.path) - 1:
				streets.get(street).passingCars += 1
	
	# Add incoming streets to each intersection (ignoring streets with no passing cars)
	for street, values in streets.items():
		if values.passingCars > 0:
			if values.end in intersections:
				intersection = intersections.get(values.end)
				intersection.incomingStreets.update({street})
			else:
				intersections.update({values.end: Intersection({street})})

	# Calculate schedule of each intersection
	for intersection, values in intersections.items():

		# Calculate total passing cars of the intersection
		totalPassingCars = 0
		for street in values.incomingStreets:
			totalPassingCars += streets.get(street).passingCars

		# Calculate best duration for each traffic light on the intersection
		for street in values.incomingStreets:
			factor = 1 # 1-20
			time = round(streets.get(street).passingCars / totalPassingCars * factor)
			time = max(1, time)

			if intersection in schedule:
				schedule.get(intersection).update({street: [time, streets.get(street).waitingCars]})
			else:
				schedule.update({intersection: {street: [time, streets.get(street).waitingCars]}})
	
	# Sort streets by the amount of waiting cars
	for intersection, streets in schedule.items():
		temp = {key: value for key, value in sorted(streets.items(), key = lambda waitingCars: waitingCars[1][1], reverse = True)}
		schedule.update({intersection: temp})

	# Write Output file
	writeFile(fileName, schedule)


main()