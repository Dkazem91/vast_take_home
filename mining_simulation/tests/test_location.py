from mining_simulation.models.location import Location
from mining_simulation.models.truck import TruckState
from mining_simulation.models.station import UnloadStationState

class TestLocation():

    def test_location(self, mining_truck, basic_location):
        # test location initialized correctly at mining state
        traveling_location = Location(TruckState.TRAVELING)
        locations_map = {TruckState.TRAVELING: traveling_location}

        basic_location.current == set()
        basic_location.leaving == set()
        state_time = mining_truck.state_time_minutes_map[mining_truck.state]

        basic_location.location_state == mining_truck.state

        basic_location.current.add(mining_truck)

        # check that location passes time and correctly moves truck around
        basic_location.pass_time(state_time)

        assert mining_truck in basic_location.leaving
        assert mining_truck not in basic_location.current

        # test that mining location moves truck to traveling location
        basic_location.resolve_departures(locations_map)

        assert basic_location.leaving == set()
        assert mining_truck.state == TruckState.TRAVELING
        assert mining_truck in traveling_location.current
        
    def test_unloading_stations(self, truck_factory, unloading_truck, basic_unloading_location):
        """
        Tests unloading station location properly takes in a truck, allocates to correct queues
        and truck is put into waiting state
        """
        # occupy all stations
        for station in basic_unloading_location.stations:

            dummy_truck = truck_factory()
            dummy_truck.state = TruckState.UNLOADING
            station.queue.append(dummy_truck)
            station.state = UnloadStationState.OCCUPIED

        # all stations should be occupied
        for station in basic_unloading_location.stations:
            assert station.state == UnloadStationState.OCCUPIED

        # add test truck to the location
        basic_unloading_location.current.add(unloading_truck)

        # Pass time to process the truck
        basic_unloading_location.pass_time()

        # The truck should now be waiting
        for station in basic_unloading_location.stations:
            for truck in station.queue:
                if truck is unloading_truck:
                    assert truck.state == TruckState.WAITING
                    return

        # we didn't find our truck, test should fail
        assert False, "Test truck not found in any station queue"





