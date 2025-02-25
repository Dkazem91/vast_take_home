"""
Main file for running the mining truck simulation.

Provides functions to run the simulation and display results.
"""

from mining_simulation.simulator import Simulator
import argparse

def parse_args():
    """
    Argument Parser function for user to run custom simulations with command line flags and arguments
    """
    parser = argparse.ArgumentParser(description='Mining Truck Simulation')
    parser.add_argument('--trucks', type=int, default=7, help='Number of trucks')
    parser.add_argument('--stations', type=int, default=3, help='Number of unloading stations')
    parser.add_argument('--hours', type=int, default=72, help='Simulation duration in hours')
    return parser.parse_args()

def display_results(metrics):
    """
    Display the simulation results in a readable format.

    """
    print("\nTruck Performance:")
    for truck in sorted(metrics['trucks'], key=lambda x: x['id']):
        print(f"\nTruck {truck['id']}:")
        print(f"  Deliveries: {truck['delivered']}")
        print(f"  Mining time: {truck['mining']} minutes")
        print(f"  Traveling time: {truck['traveling']} minutes")
        print(f"  Unloading time: {truck['unloading']} minutes")
        print(f"  Waiting time: {truck['waiting']} minutes")

    print("\nStation Performance:")
    for station in sorted(metrics['stations'], key=lambda x: x['id']):
        print(f"\nStation {station['id']}:")
        print(f"  Total unloaded: {station['unloaded']}")
        print(f"  Time occupied: {station['occupied']} minutes")
        print(f"  Time free: {station['free']} minutes")

def main():
    args = parse_args()
    
    with Simulator(trucks_amt=args.trucks, 
                  unload_stations_amt=args.stations, 
                  simulation_hrs=args.hours) as sim:
        sim.start()
        metrics = sim.performance_data
        
    # Print or save results
    display_results(metrics)



if __name__ == '__main__':
    main()