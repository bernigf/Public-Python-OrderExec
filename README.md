# Public-Python-OrderExec
Python example OrderExec

Main python script and a .dat file with price tickers recorded from BTCUSDT market back in July 2020 that I used to test this method.

To run the script just type "python script.py" and give an input for each configuration step, but you can also leave empty any of them and the script will use a default value for each variable (the default value is what's written between [ ] in each input step).

Also take into consideration that this function / method is just a simulation and was written as fast as possible without intensive testing nor used over a vast number of possible price trends / scenarios which would be the best practice.

To consider a real world implementation there are many improvements to be made and other strategies that could be tried in order to get better or optimal results.

If you would like to see the script in action at readable speed you should set the following variables when going through input:

>>> Simulated second duration (in real seconds 0.01 = 100x): [0.1] : 1 

this means that 1 simulated second will last a real second at run-time, and

>>> Print simulation output (Y/N) [Y] : Y 

in order to see a verbose output of the orders execution through the selected time frame.
