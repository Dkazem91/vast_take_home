"""
Truck model for the mining simulation.

This module defines the MiningTruck class and TruckState enum which track
the state and behavior of mining trucks in the simulation.
"""

from enum import Enum
from mining_simulation.constants import TRAVELING_TIME_MIN, HELIUM_UNLOAD_TIME_MIN, PASS_TIME_MIN


class TruckState(Enum):
    """
    Enum representing the possible states of a mining truck.
    
    States:
        MINING: Truck is at a mining site collecting resources
        TRAVELING: Truck is in transit between locations
        UNLOADING: Truck is unloading resources at a station
        WAITING: Truck is waiting in queue at an unloading station
    """
    MINING = 0
    TRAVELING = 1
    UNLOADING = 2
    WAITING = 3


class MiningTruck:
    """
    Represents a mining truck that collects and transports resources.
    
    The truck cycles through different states (mining, traveling, unloading, waiting)
    and tracks time spent in each state.
    """
    _next_id = 0
    
    def __init__(self, 
                 mining_hrs,
                 traveling_min=TRAVELING_TIME_MIN,
                 unloading_time_min=HELIUM_UNLOAD_TIME_MIN):
        """
        Initialize a new mining truck.
        """
        self.state_time_minutes_map = {
            TruckState.MINING: mining_hrs * 60,
            TruckState.TRAVELING: traveling_min,
            TruckState.UNLOADING: unloading_time_min,
            TruckState.WAITING: unloading_time_min
        }
        self.id = MiningTruck._next_id
        # assume all trucks are empty at a mining site
        self.empty = True
        self.state = TruckState.MINING
        self.time_left = self.state_time_minutes_map[self.state]
        # track minutes spent in each state
        self.performance = {state: 0 for state in TruckState}
        self.performance["delivered"] = 0

        MiningTruck._next_id += 1
    
    def state_change(self):
        """
        Handle state transitions for the truck.
        
        Changes the truck's state based on its current state and cargo status.
        Also updates the empty/full status when appropriate.
        """
        match self.state:
            case TruckState.MINING:
                self.state = TruckState.TRAVELING
                self.empty = False
            case TruckState.TRAVELING:
                if self.empty:
                    self.state = TruckState.MINING
                else:
                    self.state = TruckState.UNLOADING
            case TruckState.UNLOADING:
                self.state = TruckState.TRAVELING
                self.performance["delivered"] += 1
                self.empty = True
            case TruckState.WAITING:
                self.state = TruckState.UNLOADING

    def pass_time(self, interval=PASS_TIME_MIN):
        """
        Advance time for the truck by the specified interval.
        
        Updates time counters and transitions to the next state when appropriate.
        """
        self.performance[self.state] += interval

        if self.state != TruckState.WAITING:
            self.time_left -= interval

            if self.time_left <= 0:
                self.state_change()
                self.time_left = self.state_time_minutes_map[self.state]
        else:
            self.time_left = self.state_time_minutes_map[self.state]