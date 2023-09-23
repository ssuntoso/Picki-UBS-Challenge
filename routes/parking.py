import json
import logging
import heapq
import math

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def calculate_profit(data):
    bus_slots = data['BusParkingSlots']
    car_slots = data['CarParkingSlots']
    charges = data['ParkingCharges']
    buses = data['Buses']
    cars = data['Cars']
    bikes = data['Bikes']

    profit = 0
    bus_rejections = max(buses - bus_slots, 0)
    buses = min(buses, bus_slots)

    available_slots = bus_slots - buses
    car_in_bus_slots = min(cars, available_slots * 2)
    cars -= car_in_bus_slots

    car_rejections = max(cars - car_slots, 0)
    cars = min(cars, car_slots)

    available_slots = available_slots - car_in_bus_slots // 2 + car_slots - cars
    bike_in_car_and_bus_slots = min(bikes, available_slots * 5)
    bikes -= bike_in_car_and_bus_slots

    bike_rejections = max(bikes, 0)

    profit = buses * charges['Bus'] + (car_in_bus_slots + cars) * charges['Car'] + bike_in_car_and_bus_slots * charges['Bike']

    return {
        "Profit": profit,
        "BusRejections": bus_rejections,
        "CarRejections": car_rejections,
        "BikeRejections": bike_rejections
    }


@app.route('/parking-lot', methods=['POST'])
def parking():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = calculate_profit(data)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
