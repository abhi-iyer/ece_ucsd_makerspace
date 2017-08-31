from kiosk.sensors import main_handler
'''
Usage:
1) Sets up benchmark readings(idle_distance with no obstruction/intrusion)
2) Activate sensor alarm system which will run in background
'''
main_handler.sensor_benchmark_setup()
main_handler.start_reading()
