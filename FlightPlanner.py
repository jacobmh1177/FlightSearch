from datetime import datetime
import requests
import collections
import multiprocessing
from functools import partial

total = []
class FlightPlanner(object):
	'''Flight Planner Class'''
	def __init__(self):
		self.base_url = 'https://api.skypicker.com/'
		self.path = ''
		self.param_str = ''
		self.graph = collections.defaultdict(list)

	@property
	def full_url(self):
		""" Returns the full URL for requesting the data. """
		return '{}{}{}'.format(self.base_url, self.path, self.param_str)

	def get_request(self):
		""" Requests the API endpoint and returns the response """
		headers = {'content-type': 'application/json'}
		resp = requests.get(self.full_url, headers=headers)
		return resp.json()

	def get_flights(self, destination, start_date, end_date, num_passengers, origin):
		self.path = 'flights'
		if end_date is None:
			end_date = start_date
		if destination is None:
			self.param_str = '?flyFrom=' + \
				'{}&dateFrom={}&dateTo={}&passengers={}&typeFlight={}'.format(
				origin, start_date.strftime('%d/%m/%Y'),
				end_date.strftime('%d/%m/%Y'), num_passengers,'oneway')
		else:
			self.param_str = '?flyFrom=' + \
			'{}&to={}&dateFrom={}&dateTo={}&passengers={}'.format(
			origin, destination, start_date.strftime('%d/%m/%Y'),
			end_date.strftime('%d/%m/%Y'), num_passengers)

		self.param_str += '&flyDaysType=departure&partner=picky&curr=USD&directFlights=1'
		resp = self.get_request()
		flights = []
		for flight in resp.get('data'):
			try:
				flight_info = {
					'departure': datetime.utcfromtimestamp(flight.get('dTimeUTC')),
					'arrival': datetime.utcfromtimestamp(flight.get('aTimeUTC')),
					'price': flight.get('price'),
					'currency': resp.get('currency'),
					'legs': []
				}
				flight_info['duration'] = flight_info['arrival'] - \
					flight_info['departure']
				flight_info['duration_hours'] = (flight_info[
					'duration'].total_seconds() / 60.0) / 60.0
				if destination is None:
					for route in flight['route']:
						flight_info['legs'].append({
							'carrier': route['airline'],
							'departure': datetime.utcfromtimestamp(
								route.get('dTimeUTC')),
							'arrival': datetime.utcfromtimestamp(
								route.get('aTimeUTC')),
							'from': '{} ({})'.format(route['cityFrom'],
								route['flyFrom']),
							'to': '{} ({})'.format(route['cityTo'], route['flyTo']),
						})
				else:
					for route in flight['route']:
						flight_info['legs'].append({
							'carrier': route['airline'],
							'departure': datetime.utcfromtimestamp(
								route.get('dTimeUTC')),
							'arrival': datetime.utcfromtimestamp(
								route.get('aTimeUTC')),
							'from': '{} ({})'.format(route['cityFrom'],
								route['flyFrom']),
							'to': '{} ({})'.format(route['cityTo'], route['flyTo']),
						})
				flight_info['carrier'] = ', '.join(set([c.get('carrier') for c
					in flight_info['legs']]))
				depart = flight_info['legs'][0]['departure']
				if start_date.date() <= depart.date() and len(flight_info['legs']) == 1:
					flights.append(flight_info)
			except:
				continue
				print("error")
		return flights

	def append_to_graph(self, origin, flights):
		cities_visited = set()
		for f in flights:
			self.graph[origin].append((f['legs'], f['price']))
			city = f['legs'][0]['to']
			city = city[city.find("(")+1:city.find(")")]
			cities_visited.add(city)
		return cities_visited, self.graph

def flight_routine(planner, destination, start_date, end_date, num_passengers, visited_cities, origin):
	if origin in visited_cities:
		return set(), collections.defaultdict(list)
	flights = planner.get_flights(destination, start_date, end_date, num_passengers, origin)
	return planner.append_to_graph(origin, flights)

def build_graph(origin, start_date, end_date, num_stops, threads=5):
	planner = FlightPlanner()
	total_graph = collections.defaultdict(list)
	new_cities = set()
	visited_cities = set()
	edges = []
	origin_cities = [origin]
	flightSearch = partial(flight_routine, planner, None, start_date, end_date, 1, visited_cities)
	for stop in range(num_stops):
		pool = multiprocessing.Pool()
		output = pool.map(flightSearch, origin_cities)
		pool.close()
		pool.join()
		for cities, graph in output:
			new_cities.update(cities)
			total_graph.update(graph)
		visited_cities.update(origin_cities)
		origin_cities = list(new_cities)
		print "Visited cities: " + str(visited_cities)
		print "Next cities: " + str(origin_cities)
		print "Total number of vertices: " + str(len(total_graph))
		print "\n\n"

	vertices = 0
	edges = 0
	for k,v in total_graph.items():
		vertices += 1
		edges+=len(v)

	print "Total number of edges: " + str(edges)
	print "Total number of vertices: " + str(vertices)

	

