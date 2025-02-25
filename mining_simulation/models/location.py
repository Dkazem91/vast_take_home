"""
Location models for the mining simulation.

This module defines the Location class that manage
trucks at different locations in the simulation.
"""

import heapq
from mining_simulation.constants import PASS_TIME_MIN
from mining_simulation.models.truck import TruckState


class Location:
    """
    Base class representing a location where trucks can be present.
    
    Tracks the current trucks at the location and manages their state changes.
    """
    
    def __init__(self, location_state):
        """
        Initialize a new location.
        """
        self.location_state = location_state
        self.current = set()
        self.leaving = set()
    
    def pass_time(self, interval=PASS_TIME_MIN):
        """
        Advance time for all trucks at this location.
        
        Updates time for each truck and identifies trucks that need to leave
        for another location.
        """
        for item in self.current:
            item.pass_time(interval)
            if item.state != self.location_state:
                self.leaving.add(item)
        
        for item in self.leaving:
            self.current.remove(item)
    
    def resolve_departures(self, locations_state_map):
        """
        Move trucks from leaving set to their next locations.
        """
        for item in self.leaving:
            locations_state_map[item.state].current.add(item)
        
        self.leaving = set()

class UnloadingStations(Location):
    """
    location that manages multiple unloading stations.
    
    Distributes trucks among stations and manages the unloading process.
    """
    
    def __init__(self, location_state, stations):
        """
        Initialize a new unloading stations location.
        """
        super().__init__(location_state)
        self.stations = stations
    
    def pass_time(self, interval=PASS_TIME_MIN):
        """
        Advance time for all trucks and stations at this location.
        
        Assigns incoming trucks to stations based on queue length,
        processes unloading at stations, and identifies trucks that
        have completed unloading.
        """
        for item in self.current:
            unloading_station = heapq.heappop(self.stations)
            wait_time = item.state_time_minutes_map[self.location_state]
            unloading_station.add_truck(item, wait_time)

            heapq.heappush(self.stations, unloading_station)

        self.current = set()

        for station in self.stations:
            traveling_truck = station.pass_time(interval)
            if traveling_truck:
                self.leaving.add(traveling_truck)

        heapq.heapify(self.stations)