"""
Station model for the mining simulation.

This module defines the UnloadStation class and UnloadStationState enum which manage
the unloading of resources from mining trucks.
"""

from enum import Enum
from collections import deque
from mining_simulation.constants import PASS_TIME_MIN
from mining_simulation.models.truck import TruckState


class UnloadStationState(Enum):
    """
    Enum representing the possible states of an unloading station.
    
    States:
        FREE: Station has no trucks and is available
        OCCUPIED: Station is currently processing one or more trucks
    """
    FREE = 0
    OCCUPIED = 1


class UnloadStation:
    """
    Represents a station where trucks unload their collected resources.
    
    Manages a queue of trucks and processes them according to simulation rules.
    """
    _next_id = 0
    def __init__(self):
        """
        Initialize a new unloading station.
        """
        self.id = UnloadStation._next_id
        self.state = UnloadStationState.FREE
        self.queue = deque()
        self.queue_time = 0

        self.performance = {state: 0 for state in UnloadStationState}
        self.performance["unloaded"] = 0
        UnloadStation._next_id += 1
        
    def __lt__(self, other):
        """
        Comparison operator for station priority.
        """
        return self.queue_time < other.queue_time

    def state_change(self):
        """
        Update the station's state based on its queue.
        
        If the queue contains trucks, station is OCCUPIED, otherwise FREE.
        """
        if self.queue:
            self.state = UnloadStationState.OCCUPIED
        else:
            self.state = UnloadStationState.FREE
            self.queue_time = 0

    def pass_time(self, interval=PASS_TIME_MIN):
        """
        Advance time for the station by the specified interval.
        
        Updates time counters, processes trucks in the queue, and
        returns any truck that has completed unloading.
        """
        self.performance[self.state] += interval
        unloaded_truck = None

        if self.state == UnloadStationState.OCCUPIED:
            self.queue_time -= interval

            for truck in self.queue:
                truck.pass_time(interval)
            
            unloaded_truck = self.unload_check()

        self.state_change()
        
        return unloaded_truck
    
    def unload_check(self):
        """
        Check if the front truck in the queue has completed unloading.
        
        If the front truck is in TRAVELING state, it means it has completed
        unloading and is ready to leave the station.
        """
        # check front of queue if truck is ready to travel
        Truck = None
        if self.queue and self.queue[0].state == TruckState.TRAVELING:
            self.performance["unloaded"] += 1
            Truck = self.queue.popleft()

            if self.queue:
                self.queue[0].state_change()
        
        return Truck
    
    def add_truck(self, truck, wait_time):
        if self.queue:
            truck.state = TruckState.WAITING

        self.queue.append(truck)
        self.queue_time += wait_time

        self.state_change()