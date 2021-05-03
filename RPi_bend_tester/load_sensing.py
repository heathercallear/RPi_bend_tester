from time import sleep, time
import sys

import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

from hk711 import HK711

from graphs import formal_plot

REFERENCE_UNIT = 1
SPACING = 5

# allow for clean exit (through keyboard interrupt) from long measurement readings
def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

# initialize HK711:
# pin for dout (input pin) -> 5
# pin for pd_sck (output pin) -> 6
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(REFERENCE_UNIT)
hx.reset()
sleep(1)
# tare the balance
print('Now doing tare...')
# find average value, and readings during and after pause
try:
    tare_value, tare_pause_values, tare_values = hx.tare()
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print("Tare done! Add weight now...")

# wait for user to have added weight before proceeding
input('Press enter once weight added')

try:
    # measure weight
    # find average value, and readings during and after pause
    cal_value, cal_pause_values, cal_values = hx.read_pulse_average(times=15,
                                                                    duration=120,
                                                                    spacing=SPACING,
                                                                    pause=60
                                                                    )
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()

print('Value for tare:', tare_value)
print('Value for measurement:', cal_value)

# plot results for tare
# plot values taken during initial pause (not used for value)
formal_plot(tuple(range(0, len(tare_pause_values), SPACING)),
            tare_pause_values,
            )
# plot vertical red line to seperate pause and value reading sections of graph
plt.plot((len(tare_pause_values)-0.5,)*2,
         (0, max(tare_pause_values)),
         'r-'
)
# plot values taken during averaging for given value
(gradient, intercept), r_squared = formal_plot(tuple(range(0, len(tare_values), SPACING)),
                                               tare_values,
                                               title='',
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
print('r squared =', r_squared)

plt.show()

# plot results for measurement
# plot values taken during initial pause (not used for value)
formal_plot(tuple(range(0, len(cal_pause_values), SPACING)),
            cal_pause_values,
            )
# plot vertical red line to seperate pause and value reading sections of graph
plt.plot((len(cal_pause_values)-0.5,)*2,
         (0, max(cal_pause_values)),
         'r-'
)
# plot values taken during averaging for given value
(gradient, intercept), r_squared = formal_plot(tuple(range(0, len(cal_values), SPACING)),
                                               cal_values,
                                               )

# Hopefully values are somewhat random, so r squared is close to zero
print('Gradient = ', gradient)
print('Intercept =', intercept)
print('r squared =', r_squared)