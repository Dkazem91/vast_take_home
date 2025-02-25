"""
Simulator for the mining truck operations.

This module defines the Simulator class that orchestrates the interaction
between trucks, stations, and locations in the simulation.
"""

from random import randint
from mining_simulation.constants import MINING_MINIMUM_HRS, MINING_MAX_HRS, SIMULATION_TIME_HRS, PASS_TIME_MIN
from mining_simulation.models.truck import MiningTruck, TruckState
from mining_simulation.models.station import UnloadStation, UnloadStationState
from mining_simulation.models.location import Location, UnloadingStations


class Simulator:
    """
    Orchestrates the mining truck simulation.
    
    Creates and manages trucks, stations, and locations, advancing the
    simulation over time and collecting performance metrics.
    """
    
    def __init__(self, trucks_amt, unload_stations_amt, simulation_hrs=SIMULATION_TIME_HRS):
        """
        Initialize a new simulation environment.
        """
        self.simulation_minutes = simulation_hrs * 60
        self.trucks = {MiningTruck(randint(MINING_MINIMUM_HRS, MINING_MAX_HRS)) for _ in range(trucks_amt)}
        self.stations = [UnloadStation() for _ in range(unload_stations_amt)]
        self.locations = {
            TruckState.MINING: Location(TruckState.MINING),
            TruckState.TRAVELING: Location(TruckState.TRAVELING),
            TruckState.UNLOADING: UnloadingStations(TruckState.UNLOADING, self.stations)
        }
        self.performance_data = {
            'trucks': [],
            'stations': []
        }
    
    def start(self, interval=PASS_TIME_MIN):
        """
        Start and run the simulation.
        
        Advances time in intervals and manages the movement of trucks
        between locations until the simulation time is exhausted.
        """
        # Initialize all trucks to mining location
        self.locations[TruckState.MINING].current = self.trucks
        locations = self.locations.values()
        start = 0
        while start < self.simulation_minutes:

            # advance time for all trucks in each location
            for location in locations:
                location.pass_time(interval)

            # update leaving trucks to move to their next location
            for location in locations:
                location.resolve_departures(self.locations)
            
            start += interval

    def end(self):
        """
        Clean up after simulation ends.
        
        Collects all trucks from various locations and stations into a
        single list for final metric gathering.
        """
        self.trucks = [truck for location in self.locations.values() for truck in location.current]
        self.stations = self.locations[TruckState.UNLOADING].stations
        MiningTruck._next_id = 0
        UnloadStation._next_id = 0

        for station in self.stations:
            self.trucks.extend(station.queue)
    
    def gather_performance_metrics(self):
        """
        Collect performance metrics from all trucks and stations.
        
        Organizes the data into a structured format for analysis.
        """
        for truck in self.trucks:
            truck_data = {'id': truck.id}
            for kpi, value in truck.performance.items():
                if isinstance(kpi, TruckState):
                    kpi = kpi.name.lower()

                truck_data[kpi] = value

            self.performance_data['trucks'].append(truck_data)

        for station in self.stations:
            station_data = {'id': station.id}
            for kpi, value in station.performance.items():
                if isinstance(kpi, UnloadStationState):
                    kpi = kpi.name.lower()
                
                station_data[kpi] = value

            self.performance_data['stations'].append(station_data)

        return self.performance_data

    def __enter__(self):
        """
        Context manager entry method.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit method.
        
        Cleans up and gathers metrics when the with block is exited.
        """
        self.end()
        self.gather_performance_metrics()

        return False