import pytest
import logging
from mining_simulation.simulator import Simulator
from mining_simulation.models.truck import TruckState
from mining_simulation.models.station import UnloadStationState

logger = logging.getLogger("TestSimulator")

# Create test scenarios with their expected outcomes
TEST_SCENARIOS = [
    {
        "name": "Balanced",
        "trucks_amt": 2,
        "stations_amt": 2,
        "sim_hours": 12,
        "expected_metrics": {
            'trucks': [
                {'mining': 480, 'traveling': 220, 'unloading': 20, 'waiting': 0, 'delivered': 4},
                {'mining': 480, 'traveling': 220, 'unloading': 20, 'waiting': 0, 'delivered': 4}
            ],
            'stations': [
                {'free': 700, 'occupied': 20, 'unloaded': 4},
                {'free': 700, 'occupied': 20, 'unloaded': 4}
            ]
        }
    },
    {
        "name": "Too_many_trucks",
        "trucks_amt": 3,
        "stations_amt": 1,
        "sim_hours": 12,
        "expected_metrics": {
            'trucks': [
                {'mining': 480, 'traveling': 220, 'unloading': 20, 'waiting': 0, 'delivered': 4},
                {'mining': 480, 'traveling': 215, 'unloading': 20, 'waiting': 5, 'delivered': 4},
                {'mining': 480, 'traveling': 210, 'unloading': 20, 'waiting': 10, 'delivered': 4}
            ],
            'stations': [
                {'free': 660, 'occupied': 60, 'unloaded': 12}
            ]
        }
    }
]

class TestSimulator:
    
    @pytest.mark.parametrize("scenario", TEST_SCENARIOS, ids=[s["name"] for s in TEST_SCENARIOS])
    def test_simulator(self, scenario, truck_factory):
        """
        Test that simulator initializes, runs, and collects metrics correctly.
        Uses different scenarios defined in TEST_SCENARIOS.
        """
        # Extract scenario parameters
        trucks_amt = scenario["trucks_amt"]
        stations_amt = scenario["stations_amt"]
        sim_hours = scenario["sim_hours"]
        expected_metrics = scenario["expected_metrics"]
        
        # Create fixed mining hours trucks for consistent test runs
        test_trucks = {truck_factory() for _ in range(trucks_amt)}

        # Initialize simulator
        simulator = Simulator(
            trucks_amt=trucks_amt, 
            unload_stations_amt=stations_amt, 
            simulation_hrs=sim_hours
        )
        simulator.trucks = test_trucks
        
        # Verify initial setup
        assert len(simulator.trucks) == trucks_amt
        assert len(simulator.stations) == stations_amt
        assert simulator.simulation_minutes == sim_hours * 60
        assert TruckState.MINING in simulator.locations
        assert TruckState.TRAVELING in simulator.locations
        assert TruckState.UNLOADING in simulator.locations
        
        # Run simulation
        with simulator as sim:
            sim.start()
        
        # Verify metrics against expected metrics, get rid of ids
        metrics = simulator.performance_data
        
        metrics['trucks'] = sorted([{key: value for key, value in entry.items() if key != 'id'} for entry in metrics['trucks']], key=lambda truck: truck['waiting'])
        metrics['stations'] = sorted([{key: value for key, value in entry.items() if key != 'id'} for entry in metrics['stations']], key=lambda station: station['free'])

        assert metrics['trucks'] == expected_metrics['trucks']
        assert metrics['stations'] == expected_metrics['stations']

        assert len(simulator.trucks) == trucks_amt
        assert len(simulator.stations) == stations_amt