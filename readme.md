# CPU Instance Allocator

The program gives the number of instances that can be allocated based on three scenarios:
1. Given total number of hours and maximum price
2. Given total hours and total number of CPUs required
3. Given total hours, total CPUs and maximum price the user is willing to pay

The result contains the total cost per region and the allocated number of instances and their count

## How to run
``python3 main.py -hours <num_of_hours> -cpu <num_of_cpus> -price <max_price> ``  
The ``-hours`` option is mandatory
Instances can be requested in a combination of hours with cpu, or price or both

Examples:  
``python3 main.py -hours 3 -cpu 10``  
``python3 main.py -hours 5 -cpu 30 -price 40.5``  
``python3 main.py -hours 5 -price 40.5``   

The instances cost is available in ``cost_file.json`` file.

## Running tests
I have included two test files
``test.py`` runs fine with pycharm IDE but unable to via terminal as it is unable to resolve paths  
As a workaround I have included another test file that can be run from terminal
``python3 -m unittest tests/tests_terminal.py``  