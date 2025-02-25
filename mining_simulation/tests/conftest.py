"""
Shared test fixtures for the mining simulation tests.

This module provides pytest fixtures that can be used across multiple test files.
"""

import pytest
from mining_simulation.models.truck import MiningTruck, TruckState
from mining_simulation.models.station import UnloadStation
from mining_simulation.models.location import Location, UnloadingStations

DEFAULT_MINING_TRUCK_HRS=2
DEFAULT_STATIONS=3
DEFAULT_STATE = TruckState.MINING

@pytest.fixture(autouse=True)
def reset_class_values():
    """
    Reset the class values before each test.
    """
    MiningTruck._next_id = 0
    UnloadStation._next_id = 0

@pytest.fixture
def mining_hrs_fix(request):
    """
    Fixture providing the mining hours parameter or default
    """
    if not hasattr(request, "param"):
        return DEFAULT_MINING_TRUCK_HRS

    return request.param

@pytest.fixture
def mining_truck(mining_hrs_fix):
    """
    A truck in mining state
    """
    return MiningTruck(mining_hrs=mining_hrs_fix)

@pytest.fixture
def unloading_truck(mining_hrs_fix):
    """
    A truck that's currently unloading
    """
    truck = MiningTruck(mining_hrs=mining_hrs_fix)
    # Complete mining and traveling
    truck.pass_time(truck.time_left)  # Finish mining
    truck.pass_time(truck.time_left)  # Finish traveling
    return truck

@pytest.fixture
def truck_factory(mining_hrs_fix):
    """
    Factory fixture for creating mining trucks with specified parameters.
    """
    def create_truck(hrs=mining_hrs_fix):

        return MiningTruck(mining_hrs=hrs)
    
    return create_truck

@pytest.fixture
def basic_station():
    """
    Fixture providing a unloading station.
    """
    return UnloadStation()

@pytest.fixture
def stations(request):
    """
    Fixture providing the mining hours parameter or default
    """
    if not hasattr(request, "param"):
        return DEFAULT_STATIONS

    return request.param

@pytest.fixture
def basic_unloading_location(stations):
    """
    Fixture providing a basic unloading location with standard stations.
    """
    station_instances = [UnloadStation() for _ in range(stations)]

    return UnloadingStations(TruckState.UNLOADING, station_instances)


@pytest.fixture
def location_state_fix(request):
    """
    Fixture providing the mining hours parameter or default
    """
    if not hasattr(request, "param"):
        return DEFAULT_STATE

    return request.param

@pytest.fixture
def basic_location(location_state_fix):
    """
    Fixture providing a basic empty mining location.
    """

    return Location(location_state_fix)