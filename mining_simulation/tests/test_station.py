from mining_simulation.models.truck import TruckState
from mining_simulation.models.station import UnloadStationState

DEFAULT_WAIT_TIME = 5

class TestStation():

    def test_station(self, basic_station, truck_factory):
        """
        Tests unload station init, state change, and performance functions
        """
        # build out test arguments
        truck_1 = truck_factory()
        truck_2 = truck_factory()
        wait_time = truck_1.state_time_minutes_map[TruckState.WAITING]
        truck_1.time_left = wait_time
        truck_2.time_left = wait_time

        truck_1.state = TruckState.UNLOADING
        truck_2.state = TruckState.UNLOADING
        
        # check that station initializes correctly
        assert basic_station.state == UnloadStationState.FREE
        assert len(basic_station.queue) == 0
        assert basic_station.queue_time == 0
        assert basic_station.performance["unloaded"] == 0
        
        basic_station.pass_time(DEFAULT_WAIT_TIME)

        assert basic_station.performance[UnloadStationState.FREE] == DEFAULT_WAIT_TIME

        # check that we correctly change states after adding a truck
        basic_station.add_truck(truck_1, DEFAULT_WAIT_TIME)

        assert truck_1.state == TruckState.UNLOADING
        assert basic_station.queue_time == wait_time

        # check that adding a second truck puts it into waiting
        # and values get updated 
        basic_station.add_truck(truck_2, DEFAULT_WAIT_TIME)

        assert truck_2.state == TruckState.WAITING
        
        assert basic_station.state == UnloadStationState.OCCUPIED
        assert len(basic_station.queue) == 2
        assert basic_station.queue_time == wait_time * 2

        # check that after passing time, we get our first truck back
        # and performance metrics reflect that
        traveling_truck = basic_station.pass_time(wait_time)

        assert traveling_truck == truck_1
        assert basic_station.performance['unloaded'] == 1
        assert basic_station.performance[UnloadStationState.OCCUPIED] == DEFAULT_WAIT_TIME
        # check that the next truck has been updated states from waiting to unloading
        assert basic_station.queue[0] == truck_2

        assert basic_station.queue[0].state == TruckState.UNLOADING
