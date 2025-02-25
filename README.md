# Vast Take-Home Coding Challenge

## Getting started

Grab the code and install it:

```bash
git clone git@github.com:Dkazem91/vast_take_home.git
cd vast_take_home
pip install -e .
```

Run a simulation:

```bash
python -m mining_simulation.main --trucks 7 --stations 3 --hours 72
```

Example output:

```bash
Truck Performance:

Truck 0:
  Deliveries: 23
  Mining time: 2825 minutes
  Traveling time: 1380 minutes
  Unloading time: 115 minutes
  Waiting time: 0 minutes

Truck 1:
  Deliveries: 11
  Mining time: 3600 minutes
  Traveling time: 665 minutes
  Unloading time: 55 minutes
  Waiting time: 0 minutes

Truck 2:
  Deliveries: 23
  Mining time: 2825 minutes
  Traveling time: 1380 minutes
  Unloading time: 115 minutes
  Waiting time: 0 minutes

Truck 3:
  Deliveries: 11
  Mining time: 3600 minutes
  Traveling time: 665 minutes
  Unloading time: 55 minutes
  Waiting time: 0 minutes

Truck 4:
  Deliveries: 11
  Mining time: 3600 minutes
  Traveling time: 660 minutes
  Unloading time: 55 minutes
  Waiting time: 5 minutes

Truck 5:
  Deliveries: 34
  Mining time: 2100 minutes
  Traveling time: 2050 minutes
  Unloading time: 170 minutes
  Waiting time: 0 minutes

Truck 6:
  Deliveries: 11
  Mining time: 3600 minutes
  Traveling time: 665 minutes
  Unloading time: 55 minutes
  Waiting time: 0 minutes

Station Performance:

Station 0:
  Total unloaded: 56
  Time occupied: 280 minutes
  Time free: 4040 minutes

Station 1:
  Total unloaded: 34
  Time occupied: 170 minutes
  Time free: 4150 minutes

Station 2:
  Total unloaded: 34
  Time occupied: 170 minutes
  Time free: 4150 minutes
```

## Design & Architecture

Objected Oriented Programming and event driven actions:

### Core Classes & Responsibilities

- **MiningTruck**: A state machine that transitions between MINING, TRAVELING, UNLOADING, and WAITING states. Each truck tracks its own performance metrics and changes states where applicable.

- **UnloadStation**: Manages a truck queue and processes trucks sequentially. 

- **Location**: Locations representing the different states the truck can be in. Trucks changing states will change location.

- **Simulator**: Orchestrates the entire simulation using a step pattern, advancing time in intervals and coordinating interactions between locations, trucks, and stations.

### Data Flow

1. The simulator initializes all objects and places trucks at mining locations
2. For each time step:
   - Locations advance time for all contained trucks
   - Trucks update their internal state and may signal they need to move
   - The simulator handles truck transitions between locations
   - UnloadingStations location handles truck queues and waiting states
   - Performance metrics are continuously collected

3. At simulation end, metrics are aggregated and presented

### Other Design Decisions

- **Deque for station queue**: stations use deque for fast pops after a truck has changed states
- **Min-heap for station selection**: added station queue comparison operator to enable efficient selection of stations with shortest queue time
- **Set-based truck tracking**: Used sets for tracking trucks to avoid duplicate handling, non deterministic time checks, O(1) membership checks
- **Performance metrics collection**: Built metrics directly into entity classes for simplicity

## Testing

The test suite uses pytest with parameterized tests to verify correctness across multiple scenarios:

```bash
pytest
```

## Future improvements

With more time, I would:

- Add more diverse test cases, negative tests, functional testing, modular tests, test runner class that assembles tests given a config file
- Exception handling(bad arguments, bad states, bad metrics)
- true step functions: 
    - scrap the while loop and pass time intervals because, given hours of mining time and minutes of unload and travel time, a majority of the time nothing is happening.
    - Have a priority queue where trucks are ordered by the earliest state change time
- Create a proper metric collection 'observer' class that centralizes all the metric gathering
- Refactor all the state management code into one class that holds all the state changing rules