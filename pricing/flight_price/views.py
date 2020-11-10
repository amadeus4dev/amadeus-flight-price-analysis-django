import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .metrics import Metrics
from django.http import HttpResponse

amadeus = Client()


def flight_offers(request):
    origin = request.POST.get('Origin')
    destination = request.POST.get('Destination')
    departureDate = request.POST.get('Departuredate')
    returnDate = request.POST.get('Returndate')

    kwargs = {'originLocationCode': request.POST.get('Origin'),
              'destinationLocationCode': request.POST.get('Destination'),
              'departureDate': request.POST.get('Departuredate'), 'adults': 1}
    tripPurpose = ''
    if returnDate:
        kwargs['returnDate'] = returnDate
        tripPurpose = get_trip_purpose(request, origin, destination, departureDate, returnDate)

    if origin and destination and departureDate:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
            metrics = get_flight_price_metrics(request, origin, destination, departureDate)

        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'flight_price/home.html', {})
        search_flights_returned = []
        for flight in search_flights.data:
            offer = Flight(flight).construct_flights()
            search_flights_returned.append(offer)
            response = zip(search_flights_returned, search_flights.data)
        cheapest_flight = get_cheapest_flight_price(search_flights_returned)

        return render(request, 'flight_price/results.html', {'response': response,
                                                     'origin': origin,
                                                     'destination': destination,
                                                     'departureDate': departureDate,
                                                     'returnDate': returnDate,
                                                     'tripPurpose': tripPurpose,
                                                     'metrics': metrics,
                                                     'cheapest_flight': cheapest_flight,
                                                            })
    return render(request, 'flight_price/home.html', {})


def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')


def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))

    return json.dumps(result)


def get_flight_price_metrics(request, origin, destination, departure_date):
    try:
        metrics = amadeus.analytics.itinerary_price_metrics.get(originIataCode=origin,
                                                                destinationIataCode=destination,
                                                                departureDate=departure_date)
        metrics_returned = Metrics(metrics.data).construct_metrics()
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error)
    return metrics_returned


def get_trip_purpose(request, origin, destination, departure_date, return_date):
    try:
        trip_purpose = amadeus.travel.predictions.trip_purpose.get(originLocationCode=origin,
                                                                   destinationLocationCode=destination,
                                                                   departureDate=departure_date,
                                                                   returnDate=return_date).data
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'flight_price/home.html', {})
    return trip_purpose['result']


def get_cheapest_flight_price(flight_offers):
    return flight_offers[0].get('price')
