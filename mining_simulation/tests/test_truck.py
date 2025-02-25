import logging

import pytest
from mining_simulation.models.truck import TruckState, MiningTruck
from mining_simulation.models.station import UnloadStationState
from mining_simulation.constants import MINING_MAX_HRS, MINING_MINIMUM_HRS



class TestTruck():

    @pytest.mark.parametrize(
        "mining_hrs_fix", 
        [hour for hour in range(MINING_MINIMUM_HRS, MINING_MAX_HRS + 1)],
        indirect=["mining_hrs_fix"] 
    )
    def test_truck(self, mining_hrs_fix, mining_truck):
        """
        Tests the truck state changing, intitializing, pass time and metric capturing
        """

        # make sure they all go by assignment assumptions of empty and already at mining site
        assert mining_truck.state == TruckState.MINING
        assert mining_truck.empty == True
        assert mining_truck.performance[TruckState.MINING] == 0
        assert mining_truck.performance['delivered'] == 0

        # Verify the mining time was set correctly using the exact hours from the parameter
        mining_time = mining_truck.state_time_minutes_map[TruckState.MINING]
        assert mining_time == mining_hrs_fix * 60

        # test that truck has mining time and it goes to traveling after that mining time has passed
        mining_truck.pass_time(mining_time)
        assert mining_truck.performance[TruckState.MINING] == mining_time

        assert mining_truck.state == TruckState.TRAVELING
        assert mining_truck.empty == False
        assert mining_truck.performance[TruckState.TRAVELING] == 0

    
        # test that truck has travel time and it goes to unloading after travel time has passed
        travel_time = mining_truck.state_time_minutes_map[TruckState.TRAVELING]
        mining_truck.pass_time(travel_time)
        assert mining_truck.performance[TruckState.TRAVELING] == travel_time

        
        assert mining_truck.state == TruckState.UNLOADING
        assert mining_truck.empty == False
        assert mining_truck.performance[TruckState.UNLOADING] == 0

        # test that truck has unload time and it goes back to traveling and empty after unload time has passed
        # and we've made our delivery
        unload_time = mining_truck.state_time_minutes_map[TruckState.UNLOADING]
        mining_truck.pass_time(unload_time)
        assert mining_truck.performance[TruckState.UNLOADING] == unload_time

        assert mining_truck.state == TruckState.TRAVELING
        assert mining_truck.empty == True
        assert mining_truck.performance['delivered'] == 1

