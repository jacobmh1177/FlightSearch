from FlightPlanner import *
from datetime import datetime
import time

# planner = FlightPlanner()
# start = datetime.strptime('07/10/2017', '%m/%d/%Y')
# end = datetime.strptime('07/11/2017', '%m/%d/%Y')
# depart_time = datetime.strptime('00:00', '%H:%M')
# flights = planner.get_flights(None, start, None, 1, 'SFO')
# #flights = planner.get_flights('SFO', 'DEN', start, 1)
# planner.append_to_graph('SFO', flights)

# for route, cost in planner.graph['SFO']:
# 	route = route[0]
# 	print "From: " + route['from']
# 	print "To: " + route['to']
# 	print "Date: " + datetime.strftime(route['departure'], '%m/%d/%Y')
# 	print "Departing at: " + datetime.strftime(route['departure'], '%H:%M')
# 	print "Arriving at: " + datetime.strftime(route['arrival'], '%H:%M')
# 	print "Cost: " + str(cost)
# 	print "\n\n"


# example = planner.graph['SFO'][0]
# print example
# print len(planner.graph['SFO'])

# build_graph('SFO', start, end, 1)


#([{'arrival': datetime.datetime(2017, 7, 10, 22, 29), 'to': 'Denver (DEN)', 'carrier': u'UA', 'from': 'San Jose (SJC)', 'departure': datetime.datetime(2017, 7, 10, 20, 0)}, {'arrival': datetime.datetime(2017, 7, 11, 6, 48), 'to': 'Houston (IAH)', 'carrier': u'UA', 'from': 'Denver (DEN)', 'departure': datetime.datetime(2017, 7, 11, 4, 30)}, {'arrival': datetime.datetime(2017, 7, 11, 16, 36), 'to': 'Puerto Vallarta (PVR)', 'carrier': u'UA', 'from': 'Houston (IAH)', 'departure': datetime.datetime(2017, 7, 11, 14, 7)}], 163)


if __name__ == '__main__':
	start = datetime.strptime('07/10/2017', '%m/%d/%Y')
	end = datetime.strptime('07/13/2017', '%m/%d/%Y')
	start_time = time.time()
	build_graph('SFO', start, None, 1)
	end_time = time.time()

	print "Total time: " + str(end_time - start_time)