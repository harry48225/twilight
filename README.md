# ```twlight```

An automated roller blind opener. Using an esp32 runing micropython.

## ```twilight.local```
The esp32 serves a svelte webapp on ``` twilight.local```. See ```firmware/webapp```
![webapp](https://github.com/harry48225/twilight/blob/main/images/webapp.png?raw=true)

## ```hardware```
A NEMA 17 stepper motor is used to move the blinds. It's connected to a 3d-printed gearbox ```cad/``` providing an ~1:5 reduction. It's driven by a DRV8825 stepper motor driver.
![gears](https://github.com/harry48225/twilight/blob/main/images/gears.png?raw=true)
