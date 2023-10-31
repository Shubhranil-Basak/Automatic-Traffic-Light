# AUTOMATIC TRAFFIC LIGHT
This repository contains RISC-V based traffic light automation.
### OVERVIEW
Traffic lights usually consists of three signals through the usage of colors, arrows, and other images to convey various messages. Traffic lights are in sets of red, yellow, and green lights at intersection of roads. Traffic is then controlled as vehicles receive signals/messages of when to stop and when to go.
### AIM
The project's goal is to design an automatic machine utilizing a specialized RISC-V processor for controlling traffic by releasing a specific number of cars and pedestrians depending on whoever comes first. The objective of this program is to minimize traffic problems, energy consumption, and overall expenses. 
### BLOCK DIAGRAM 
<img width="810" alt="Block Diagram" src="https://github.com/AryanAAB/Automatic-Traffic-Light/assets/142584708/0538173c-416c-49be-acfe-d18c96bad4db">

### MATERIALS REQUIRED
LED : https://tinyurl.com/yc5w423x : ₹125

IR Sensors : https://tinyurl.com/8dybpmhn : ₹510
### HOW DOES AN IR SENSOR WORK?
An IR Sensor consists of an IR LED trasmitter that emits infrared radition. It has the same appearance as a standard LED, but the radiation it emits is not visible to the human eye. If an object blocks the pathway of the infrared waves, then the reflected radiations are detected by the infrared receivers. The sensor output can be decided by the IR receiver depending on the intensity of the response. These infrared receivers are available in photodiode form. IR photodiode are different from regular photodiodes in that they only detect IR radiation. Different types of infrared receivers exist based on voltage, wavelength, package, and other factors.

When using an IR transmitter and receiver, the wavelength of the receiver must match that of the transmitter because the infrared photodiode is activated by the infrared light produced by the infrared LED. The photodiode’s resistance and the change in output voltage are proportional to the amount of infrared light obtained.

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/144095577/dd21f4aa-b0f3-4a6a-9c71-0b6cb3cbec00)


### REGISTER ARCHITECTURE FOR x30 FOR GPIOs

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/148491110/c6fd4ddc-8b65-4447-9a75-fb0c106bfc71)

x30[0] is an input pin from an IR Sensor from Side 1 for going straight.

x30[1] is an input pin from an IR Sensor from Side 2 for going straight.

x30[2] is an input pin from an IR Sensor form Side 3 for going straight.

x30[3] is an input pin from an IR Sensor from Side 4 for going straight.

x30[4] is an input pin from an IR Sensor from Side 1 for going right.

x30[5] is an input pin from an IR Sensor from Side 2 for going right.

x30[6] is an input pin from an IR Sensor form Side 3 for going right.

x30[7] is an input pin from an IR Sensor from Side 4 for going right.

x30[8] is an output pin for a Red LED for Side 1 for going straight.

x30[9] is an output pin for a Red LED for Side 2 for going straight.

x30[10] is an output pin for a Red LED for Side 3 for going straight.

x30[11] is an output pin for a Red LED for Side 4 for going straight.

x30[12] is an output pin for a Red LED for Side 1 for going right.

x30[13] is an output pin for a Red LED for Side 2 for going right.

x30[14] is an output pin for a Red LED for Side 3 for going right.

x30[15] is an output pin for a Red LED for Side 4 for going right.

x30[16] is an output pin for a Yellow LED for Side 1 for going straight.

x30[17] is an output pin for a Yellow LED for Side 2 for going straight.

x30[18] is an output pin for a Yellow LED for Side 3 for going straight.

x30[19] is an output pin for a Yellow LED for Side 4 for going straight.

x30[20] is an output pin for a Yellow LED for Side 1 for going right.

x30[21] is an output pin for a Yellow LED for Side 2 for going right.

x30[22] is an output pin for a Yellow LED for Side 3 for going right.

x30[23] is an output pin for a Yellow LED for Side 4 for going right.

x30[24] is an output pin for a Green LED for Side 1 for going straight.

x30[25] is an output pin for a Green LED for Side 2 for going straight.

x30[26] is an output pin for a Green LED for Side 3 for going straight.

x30[27] is an output pin for a Green LED for Side 4 for going straight.

x30[28] is an output pin for a Green LED for Side 1 for going right.

x30[29] is an output pin for a Green LED for Side 2 for going right.

x30[30] is an output pin for a Green LED for Side 3 for going right.

x30[31] is an output pin for a Green LED for Side 4 for going right.

### ASSEMBLY CODE USING C

```C
/* 
 * In this code to simulate time, we assume that one iteration of any while loop is 1ms
 * Therefore, 1s = 1000 ms = 1000 iterations.
 */
 
int priority();
void turnOn(int);
void turnOff(int);
int getValue(int);
void turnOnYellow(int *, int, int, int *);
void turnOffLight(int *, int, int, int *);
void turnOffPriorityLight(int, int, int);
void ONLimit(int[], int[], int[], int[], int[]);
void perform(int[], int[], int[], int[], int[], const int, int, int[]);
void call(int[], int[], int[], int[], int[], int[], int[], int[], int);

/*
 * This returns the lane which has priority. That is, it represents the lane that should be green when there is no traffic.
 */
int priority()
{
	return 0; //We are giving side 1 has priority
}

/*
 * Turns on the LED at port "port"
 * @param port : The port of the LED light to turn on (from x30)
 */
void turnOn(int port)
{
	int pin_mask = 1 << port;
	asm volatile(
		"or x30, x30, %0\n\t"
		:
		: "r"(pin_mask)
		: "x30"
	);
}

/*
 * Turns off the LED at port "port"
 * @param port : The port of the LED light to turn off (from x30)
 */
void turnOff(int port)
{
	int pin_mask = ~(1 << port);
	asm volatile(
		"and x30, x30, %0\n\t"
		:
		: "r"(pin_mask)
		: "x30"
	);
}

/*
 * Returns the value of the sensor at port "port"
 * @param port : The port of the sensor (from x30)
 * @return : The value reported by the sensor
 */
int getValue(int port)
{
	int result = 0;
	asm volatile(
		"lw %0, x30\n\t"
		:"=r"(result)
		:
		:"x30"
	);
	return (result >> port) & 1;
}

/*
 * Turns off the green light and turns on the yellow light
 * @param green : pointer to the number that says that green is on/off
 * @param greenLED : port of the green LED
 * @param yellowLED : port of the yellow LED
 * @param yellow : pointer to the number that says that yellow is on/off
 */
void turnOnYellow(int * green, int greenLED, int yellowLED, int * yellow)
{
	*green = 0;
	turnOff(greenLED);
	turnOn(yellowLED);
	*yellow = 1;
}

/*
 * Turns off the given light and turns on the next light
 * @param lightOff : pointer to the number that says that light is on/off
 * @param lightOffLED : port of the LED that is to be turned off
 * @param lightOnLED : port of the LED that is to be turned on
 * @param lightOn : pointer to the number that says that light is on/off
 */
void turnOffLight(int * lightOff, int lightOffLED, int lightOnLED, int * lightOn)
{
	*lightOff = 0;
	turnOff(lightOffLED);
	turnOn(lightOnLED);
	*lightOn = 1;
}

/* 
 * Turns off the priority light that is used when there is no traffic.
 * @param red: the port of the red light
 * @param yellow: the port of the yellow light
 * @param green: the port of the green light
 */
void turnOffPriorityLight(int red, int yellow, int green)
{
	int counter = 0;
	
	turnOff(green);
	turnOn(yellow);
	while(counter != 1000)
		counter++;
	
	turnOff(yellow);
	turnOn(red);
}

/*
 * First turns on right light and the straight light
 * @param sensor1 : Ports of Straight Sensor 1 and Right Sensor 1
 * @param sensor2 : Ports of Straight Sensor 2 and Right Sensor 2
 * @param red : Ports of red Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param yellow : Ports of yellow Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param green : Ports of green Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 */
void ONLimit(int sensor1[], int sensor2[], int red[], int yellow[], int green[])
{
	const int RIGHT_TIME_LIMIT = 15;
	const int STRAIGHT_TIME_LIMIT = 45;
	
	int greenOn[2] = {0, 0};
	
	perform(sensor1, sensor2, red, yellow, green, RIGHT_TIME_LIMIT, 0, greenOn);
	perform(sensor1, sensor2, red, yellow, green, STRAIGHT_TIME_LIMIT, 1, greenOn);
}

/*
 * Turns on the lights specified. 
 * @param sensor1 : Ports of Straight Sensor 1 and Right Sensor 1
 * @param sensor2 : Ports of Straight Sensor 2 and Right Sensor 2
 * @param red : Ports of red Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param yellow : Ports of yellow Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param green : Ports of green Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param Limit : The time limit
 * @param goStraight : If you want to go straight = 1; otherwise = 0
 * @param greenOn : If you want to go straight then greenOn would store if the green signals are already on
 */
void perform(int sensor1[], int sensor2[], int red[], int yellow[], int green[], const int LIMIT, int goStraight, int greenOn[])
{
	int counter = 0;
		
	//If going right, then pos = 1; otherwise = 0
	int pos = 1;
	if(goStraight)
		pos = 0; 		
		
	//For turning on green signals for going straight if this function is for going right
	int done1 = 0, done2 = 0;

	//If red light is on then value is 1; otherwise it is 0
	int red1 = 1, red2 = 1;
	//If green light is on then value is 1; otherwise it is 0
	int green1 = 0, green2 = 0;
	//If yellow light is on then value is 1; otherwise it is 0
	int yellow1 = 0, yellow2 = 0;
	//We need to store the time when yellow light was turned on
	int yellowCounter1 = 0, yellowCounter2 = 0;
		
	if(goStraight && greenOn[0])
	{
		red1 = 0;
		green1 = 1;
	}
	if(goStraight && greenOn[1])
	{
		red2 = 0;
		green2 = 1;
	}

	if(getValue(sensor1[pos]))
		turnOffLight(&red1, red[pos], green[pos], &green1);
	if(getValue(sensor2[pos]))
		turnOffLight(&red2, red[pos + 2], green[pos + 2], &green2);
		
	//After this loop, only red light would be turned on if you want to go straight.
	//If you want to go right, it is possible that the going straight light would be on.
	//However, going right light would be off.
	while(!red1 || !red2)
	{
		if(green1 && (getValue(sensor1[pos]) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green[pos], yellow[pos], &yellow1);
		if(green2 && (getValue(sensor2[pos]) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green[pos + 2], yellow[pos + 2], &yellow2);

		if(yellow1 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow[pos], red[pos], &red1);
		if(yellow2 && yellowCounter2 >= 1 * 1000)
			turnOffLight(&yellow2, yellow[pos + 2], red[pos + 2], &red2);
			
		//If this function performs for going right and the opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red2 && !done1 && getValue(sensor1[0]))
		{
			done1 = 1;
			turnOff(red[0]);
			turnOn(green[0]);
		}
			
		//If this function performs for going right and opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red1 && !done2 && getValue(sensor1[2]))
		{
			done2 = 1;
			turnOff(red[2]);
			turnOn(green[2]);
		}
		counter++;
		
		if(yellow1)
			yellowCounter1++;
		if(yellow2)
			yellowCounter2++;
	}
		
	greenOn[0] = done1;
	greenOn[1] = done2;
}

/* 
 * Used by main to call the OnLimit function. 
 * @param sensors : list of ports of all the sensors
 * @param red : list of ports of red lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param red_right : list of ports of red lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param yello : list of ports of yellow lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param yellow_right : list of ports of yellow lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param green : list of ports of green lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param green_right : list of ports of green lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param open : Which side to turn on
 */
void call(int sensors[], int sensors_right[], int red[], int red_right[], int yellow[], int yellow_right[], int green[], int green_right[], int open)
{
		//Parameters of ONLimit
		int inp_sensor1[2] = { sensors[open], sensors_right[open] };
		int inp_sensor2[2] = { sensors[open + 1], sensors_right[open + 1] };
		int inp_Red[4]     = { red[open], red_right[open], red[open + 1], red_right[open + 1] };
		int inp_Yellow[4]  = { yellow[open], yellow_right[open], yellow[open + 1], yellow_right[open + 1] };
		int inp_Green[4]   = { green[open], green_right[open], green[open + 1], green_right[open + 1] };
		ONLimit(inp_sensor1, inp_sensor2, inp_Red, inp_Yellow, inp_Green);
}

int main(void)
{
		//Format: Side1, Side2, Side3, Side4
		
		//These are on x30
		int sensors[4] = {0, 1, 2, 3};
		int sensors_right[4] = {4, 5, 6, 7};
		
		//These are on x30
		int red[4] = {8, 9, 10, 11};
		int red_right[4] = {12, 13, 14, 15};
		int yellow[4] = {16, 17, 18, 19};
		int yellow_right[4] = {20, 21, 22, 23};
		int green[4] = {24, 25, 26, 27};
		int green_right[4] = {28, 29, 30, 31};
		
		//open == 0 means open sides 1 and 2 (opposite paths)
		//open == 2 means open sides 3 and 4 (opposite paths)
		int open = 0;

		//Reset all bits on x30
		asm volatile(
			"andi x30, x30, 0x0\n\t" //x30 & 0 and store in x30
			:
			:
			: "x30" //This specifies that x30 is being changed after this instruction
		);
		
		//Masked value to turn on all red lights		
		int pin_mask = 0;
		for(int i = 0; i < 4; i++)
			pin_mask |= 1 << red[i] | 1 << red_right[i];

		//Turn on all red lights
		asm volatile(
			"or x30, x30, %0\n\t" //x30 or pin_mask and store in x30 (%0 means go to first input that is given)
			:
			: "r"(pin_mask)
			: "x30"
		);

		int priorityLane = priority();
		int on = 0;
		
		while(1)
		{
			int count = 0;
			for(int i = 0; i < 4; i++)
				if(getValue(sensors[i]) || getValue(sensors_right[i]))
					count++;
			
			if(count != 0)
			{
				if(on)
				{
					turnOffPriorityLight(red[priorityLane], yellow[priorityLane], green[priorityLane]);
					on = 0;
				}
				if(count == 4 || count == 3)
				{
					call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
					open = (open + 2) % 4;	
					call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);				
					open = (open + 2) % 4;
				}
				else if(count == 2 || count == 1)
				{
					if(getValue(sensors[open]) || getValue(sensors_right[open]) || getValue(sensors[open + 1]) || getValue(sensors_right[open + 1]))
						call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
					open = (open + 2) % 4;
					if(getValue(sensors[open]) || getValue(sensors_right[open]) || getValue(sensors[open + 1]) || getValue(sensors_right[open + 1]))
					{
						call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
						open = (open + 2) % 4;
					}
				}
			}
			else
			{
				if(!on)
				{
					turnOff(red[priorityLane]);
					turnOn(green[priorityLane]);
					on = 1;
				}
			}
		}
    return 0;
}
```

### NON-ASSEMBLY CODE USING C

```C
//This code is not a assembly structure
//This code can be run to check whether the code is providing
//the required outputs according to the given inputs.

#include <time.h>
#include <stdio.h>
#include <stdlib.h>

int randomNumber(int, int);
void turnOn(int);
void turnOff(int);
int getValue(int);
void turnOnYellow(int *, int, int, int *, time_t *);
void turnOffLight(int *, int, int, int *);
void turnOffRandomLight(int, int, int);
void ONLimit(int[], int[], int[], int[], int[]);
void perform(int[], int[], int[], int[], int[], const int, int, int[]);
void call(int[], int[], int[], int[], int[], int[], int[], int[], int);
int hardware[32];
for(int i = 0; i < 32; i++){
	hardware[i] = 0;
}

//This function will print the Side/Lane number along with the direction i.e. Straight or Right if the LED for those Sideis are on.
void print(){
    for(int i = 8, j = 1; i <= 11; i++, j++){
	    if(hardware[i]){
		    printf("Red light straight at side %d is on\n", j);
		}
    }
    for(int i = 12, j = 1; i <= 15; i++, j++){
	    if(hardware[i]){
		    printf("%d Red light right at side %d is on\n", hardware[i], j);
	    }
    }
    for(int i = 16, j = 1; i <= 19; i++, j++){
	    if(hardware[i]){
		    printf("%d Yellow light straight at side %d is on\n", hardware[i], j);
	    }
    }
    for(int i = 20, j = 1; i <= 23; i++, j++){
	    if(hardware[i]){
		    printf("%d Yellow light right at side %d is on\n", hardware[i], j);
	    }
    }
    for(int i = 24, j = 1; i <= 27; i++, j++){
	    if(hardware[i]){
		    printf("%d Green light straight at side %d is on\n", hardware[i], j);
	    }
    }
    for(int i = 28, j = 1; i <= 31; i++, j++){
	    if(hardware[i]){
		    printf("%d Green light right at side %d\n", hardware[i], j);
	    }
    }

	printf("\n\n");
}

/*
 * Outputs a random number between lower and upper.
 * @param lower : lower bound
 * @param upper : upper bound
 */

int randomNumber(int lower, int upper)
{
    srand(time(NULL));
    return (rand() % (upper - lower + 1));
}

/*
 * Turns on the LED at port "port"
 * @param port : The port of the LED light to turn on (from x30)
 */
void turnOn(int port)
{
	int pin_mask = 1 << port;
	hardware[port] = 1;
}

/*
 * Turns off the LED at port "port"
 * @param port : The port of the LED light to turn off (from x30)
 */
void turnOff(int port)
{
	int pin_mask = ~(1 << port);
	hardware[port] = 0;
}

/*
 * Returns the value of the sensor at port "port"
 * @param port : The port of the sensor (from x30)
 * @return : The value reported by the sensor
 */
int getValue(int port)
{
	return hardware[port];
}

/*
 * Turns off the green light and turns on the yellow light
 * @param green : pointer to the number that says that green is on/off
 * @param greenLED : port of the green LED
 * @param yellowLED : port of the yellow LED
 * @param yellow : pointer to the number that says that yellow is on/off
 * @param yellowStart : pointer to a time object that will start the time of yellow
 */
void turnOnYellow(int * green, int greenLED, int yellowLED, int * yellow, time_t * yellowStart)
{
	*green = 0;
	turnOff(greenLED);
	turnOn(yellowLED);
	*yellow = 1;
	*yellowStart = time(NULL);
}

/*
 * Turns off the given light and turns on the next light
 * @param lightOff : pointer to the number that says that light is on/off
 * @param lightOffLED : port of the LED that is to be turned off
 * @param lightOnLED : port of the LED that is to be turned on
 * @param lightOn : pointer to the number that says that light is on/off
 */
void turnOffLight(int * lightOff, int lightOffLED, int lightOnLED, int * lightOn)
{
	*lightOff = 0;
	turnOff(lightOffLED);
	turnOn(lightOnLED);
	*lightOn = 1;
}

/* 
 * Turns off the random light that is used when there is no traffic.
 * @param red: the port of the red light
 * @param yellow: the port of the yellow light
 * @param green: the port of the green light
 */
void turnOffRandomLight(int red, int yellow, int green)
{
	time_t startTime, currTime;
	
	startTime = time(NULL);
	currTime = time(NULL);
	
	turnOff(green);
	turnOn(yellow);
    print();
	while(difftime(currTime, startTime) <= 1){
		currTime = time(NULL);
    }
	turnOff(yellow);
	turnOn(red);
    print();
}

/*
 * First turns on right light and the straight light
 * @param sensor1 : Ports of Straight Sensor 1 and Right Sensor 1
 * @param sensor2 : Ports of Straight Sensor 2 and Right Sensor 2
 * @param red : Ports of red Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param yellow : Ports of yellow Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param green : Ports of green Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 */
void ONLimit(int sensor1[], int sensor2[], int red[], int yellow[], int green[])
{
	const int RIGHT_TIME_LIMIT = 5; //Standard RIGHT_TIME_LIMIT is 15 sec
	const int STRAIGHT_TIME_LIMIT = 5; //Standard STRAIGHT_TIME_LIMIT is 45 sec
	
	int greenOn[2] = {0, 0};
	
	perform(sensor1, sensor2, red, yellow, green, RIGHT_TIME_LIMIT, 0, greenOn);
	perform(sensor1, sensor2, red, yellow, green, STRAIGHT_TIME_LIMIT, 1, greenOn);
}

/*
 * Turns on the lights specified. 
 * @param sensor1 : Ports of Straight Sensor 1 and Right Sensor 1
 * @param sensor2 : Ports of Straight Sensor 2 and Right Sensor 2
 * @param red : Ports of red Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param yellow : Ports of yellow Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param green : Ports of green Light: Straight Lane 1, Right Lane 1, Straight Lane 2, Right Lane 2
 * @param Limit : The time limit
 * @param goStraight : If you want to go straight = 1; otherwise = 0
 * @param greenOn : If you want to go straight then greenOn would store if the green signals are already on
 */
void perform(int sensor1[], int sensor2[], int red[], int yellow[], int green[], const int LIMIT, int goStraight, int greenOn[])
{
	time_t startTime, currentTime;
	startTime = time(NULL);
		
	//If going right, then pos = 1; otherwise = 0
	int pos = 1;
	if(goStraight){
		pos = 0;
    }
	//For turning on green signals for going straight if this function is for going right
	int done1 = 0, done2 = 0;

	//If red light is on then value is 1; otherwise it is 0
	int red1 = 1, red2 = 1;
	//If green light is on then value is 1; otherwise it is 0
	int green1 = 0, green2 = 0;
	//If yellow light is on then value is 1; otherwise it is 0
	int yellow1 = 0, yellow2 = 0;
	//We need to store the time when yellow light was turned on
	time_t yellow1Start, yellow2Start;
		
	if(goStraight && greenOn[0])
	{
		red1 = 0;
		green1 = 1;
	}
	if(goStraight && greenOn[1])
	{
		red2 = 0;
		green2 = 1;
	}

	if(getValue(sensor1[pos]))
		turnOffLight(&red1, red[pos], green[pos], &green1);
	if(getValue(sensor2[pos]))
		turnOffLight(&red2, red[pos + 2], green[pos + 2], &green2);
		
	currentTime = time(NULL);
    print();
		
	//After this loop, only red light would be turned on if you want to go straight.
	//If you want to go right, it is possible that the going straight light would be on.
	//However, going right light would be off.
	while(!red1 || !red2)
	{
		if(green1 && (getValue(sensor1[pos]) == 0 || difftime(currentTime, startTime) >= LIMIT))
			turnOnYellow(&green1, green[pos], yellow[pos], &yellow1, &yellow1Start);
		if(green2 && (getValue(sensor2[pos]) == 0 || difftime(currentTime, startTime) >= LIMIT))
			turnOnYellow(&green2, green[pos + 2], yellow[pos + 2], &yellow2, &yellow2Start);

		currentTime = time(NULL);

		if(yellow1 && difftime(currentTime, yellow1Start) >= 1)
			turnOffLight(&yellow1, yellow[pos], red[pos], &red1);
		if(yellow2 && difftime(currentTime, yellow2Start) >= 1)
			turnOffLight(&yellow2, yellow[pos + 2], red[pos + 2], &red2);
			
		//If this function performs for going right and the opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red2 && !done1 && getValue(sensor1[0]))
		{
			done1 = 1;
			turnOff(red[0]);
			turnOn(green[0]);
		}
			
		//If this function performs for going right and opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red1 && !done2 && getValue(sensor1[2]))
		{
			done2 = 1;
			turnOff(red[2]);
			turnOn(green[2]);
		}
        print();
	}
		
	greenOn[0] = done1;
	greenOn[1] = done2;
}

/* 
 * Used by main to call the OnLimit function. 
 * @param sensors : list of ports of all the sensors
 * @param red : list of ports of red lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param red_right : list of ports of red lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param yello : list of ports of yellow lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param yellow_right : list of ports of yellow lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param green : list of ports of green lights StraightLED1, StraightLED2, StraightLED3, StraightLED4
 * @param green_right : list of ports of green lights RightLED1, RightLED2, RightLED3, RightLED4
 * @param open : Which side to turn on
 */
void call(int sensors[], int sensors_right[], int red[], int red_right[], int yellow[], int yellow_right[], int green[], int green_right[], int open)
{
		//Parameters of ONLimit
		int inp_sensor1[2] = { sensors[open], sensors_right[open] };
		int inp_sensor2[2] = { sensors[open + 1], sensors_right[open + 1] };
		int inp_Red[4]     = { red[open], red_right[open], red[open + 1], red_right[open + 1] };
		int inp_Yellow[4]  = { yellow[open], yellow_right[open], yellow[open + 1], yellow_right[open + 1] };
		int inp_Green[4]   = { green[open], green_right[open], green[open + 1], green_right[open + 1] };
		ONLimit(inp_sensor1, inp_sensor2, inp_Red, inp_Yellow, inp_Green);
}

int main(void)
{
		//Format: Side1, Side2, Side3, Side4
		
		//These are on x30
		int sensors[4] = {0, 1, 2, 3};
		int sensors_right[4] = {4, 5, 6, 7};
		
		//These are on x30
		int red[4] = {8, 9, 10, 11};
		int red_right[4] = {12, 13, 14, 15};
		int yellow[4] = {16, 17, 18, 19};
		int yellow_right[4] = {20, 21, 22, 23};
		int green[4] = {24, 25, 26, 27};
		int green_right[4] = {28, 29, 30, 31};
		// This part of the hardware function is hardcoded
		// This is to check wether the code is working properly or not
		hardware[0] = 0;
		hardware[1] = 0;
		hardware[2] = 0;
		hardware[3] = 1;
		// Above code will set all LEDs of all lanes to red except for Lane4 straight road.

		// hardware[4] = 0;
		// hardware[5] = 1;
		// hardware[6] = 0;
		// hardware[7] = 0;
		// The above code will make the lane2 right turn LED green and all other LEDs to red
		
		
		

		//open == 0 means open sides 1 and 2 (opposite paths)
		//open == 2 means open sides 3 and 4 (opposite paths)
		int open = 0;
		
		//Masked value to turn on all red lights		
		int pin_mask = 0;
		for(int i = 8; i <= 15; i++)
            hardware[i] = 1;

		int rand = randomNumber(0, 3);
		int on = 0;
		print();
		while(1)
		{
			int count = 0;
			for(int i = 0; i < 4; i++)
				if(getValue(sensors[i]) || getValue(sensors_right[i]))
					count++;
			if(count != 0)
			{
				if(on)
				{
					turnOffRandomLight(red[rand], yellow[rand], green[rand]);
					on = 0;
					rand = randomNumber(0, 3);
				}
				if(count == 4 || count == 3)
				{
					call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
					open = (open + 2) % 4;	
					call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);				
					open = (open + 2) % 4;
				}
				else if(count == 2 || count == 1)
				{
					if(getValue(sensors[open]) || getValue(sensors_right[open]) || getValue(sensors[open + 1]) || getValue(sensors_right[open + 1]))
						call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
					open = (open + 2) % 4;
					if(getValue(sensors[open]) || getValue(sensors_right[open]) || getValue(sensors[open + 1]) || getValue(sensors_right[open + 1]))
					{
						call(sensors, sensors_right, red, red_right, yellow, yellow_right, green, green_right, open);
						open = (open + 2) % 4;
					}
				}
			}
			else
			{
				if(!on)
				{
					turnOff(red[rand]);
					turnOn(green[rand]);
					on = 1;
					print();
				}
			}
			break;
		}
    return 0;
}

```

### COMPILE AND RUN THE C CODE

gcc Traffic.c

./a.out

### SCREENSHOTS

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/144095577/99e03b2b-898a-4eab-94e5-ef1cac09c7cb)

* In the first 4 line we can see that right turn red is on for all the lanes
* In line 5 we can see that yellow light is on for lane 4 straight
* This is because as Green light for lane 4 was on at the beginning
* And the sensor did not return any response as it did not detect any car
* Thus it instantly changes to yellow.
* In the next 3 line red light for the straight road is on for lane 1, 2 and 3 but not for lane 4
* All the other lines in set of 8 are the same thing and it will be the same.
* This code will run for 5 seconds.

### ASSEMBLY CODE CONVERSION

riscv64-unknown-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -nostdlib -o ./out TrafficSignalController.c

riscv64-unknown-elf-objdump -d -r out > TrafficSignalControllerAssembly.txt

### ASSEMBLY CODE

```

out:     file format elf32-littleriscv


Disassembly of section .text:

00010054 <priority>:
   10054:	ff010113          	addi	sp,sp,-16
   10058:	00812623          	sw	s0,12(sp)
   1005c:	01010413          	addi	s0,sp,16
   10060:	00000793          	li	a5,0
   10064:	00078513          	mv	a0,a5
   10068:	00c12403          	lw	s0,12(sp)
   1006c:	01010113          	addi	sp,sp,16
   10070:	00008067          	ret

00010074 <turnOn>:
   10074:	fd010113          	addi	sp,sp,-48
   10078:	02812623          	sw	s0,44(sp)
   1007c:	03010413          	addi	s0,sp,48
   10080:	fca42e23          	sw	a0,-36(s0)
   10084:	fdc42783          	lw	a5,-36(s0)
   10088:	00100713          	li	a4,1
   1008c:	00f717b3          	sll	a5,a4,a5
   10090:	fef42623          	sw	a5,-20(s0)
   10094:	fec42783          	lw	a5,-20(s0)
   10098:	00ff6f33          	or	t5,t5,a5
   1009c:	00000013          	nop
   100a0:	02c12403          	lw	s0,44(sp)
   100a4:	03010113          	addi	sp,sp,48
   100a8:	00008067          	ret

000100ac <turnOff>:
   100ac:	fd010113          	addi	sp,sp,-48
   100b0:	02812623          	sw	s0,44(sp)
   100b4:	03010413          	addi	s0,sp,48
   100b8:	fca42e23          	sw	a0,-36(s0)
   100bc:	fdc42783          	lw	a5,-36(s0)
   100c0:	00100713          	li	a4,1
   100c4:	00f717b3          	sll	a5,a4,a5
   100c8:	fff7c793          	not	a5,a5
   100cc:	fef42623          	sw	a5,-20(s0)
   100d0:	fec42783          	lw	a5,-20(s0)
   100d4:	00ff7f33          	and	t5,t5,a5
   100d8:	00000013          	nop
   100dc:	02c12403          	lw	s0,44(sp)
   100e0:	03010113          	addi	sp,sp,48
   100e4:	00008067          	ret

000100e8 <getValue>:
   100e8:	fd010113          	addi	sp,sp,-48
   100ec:	02812623          	sw	s0,44(sp)
   100f0:	03010413          	addi	s0,sp,48
   100f4:	fca42e23          	sw	a0,-36(s0)
   100f8:	fe042623          	sw	zero,-20(s0)
   100fc:	000f0793          	mv	a5,t5
   10100:	fef42623          	sw	a5,-20(s0)
   10104:	fdc42783          	lw	a5,-36(s0)
   10108:	fec42703          	lw	a4,-20(s0)
   1010c:	40f757b3          	sra	a5,a4,a5
   10110:	0017f793          	andi	a5,a5,1
   10114:	00078513          	mv	a0,a5
   10118:	02c12403          	lw	s0,44(sp)
   1011c:	03010113          	addi	sp,sp,48
   10120:	00008067          	ret

00010124 <turnOnYellow>:
   10124:	fe010113          	addi	sp,sp,-32
   10128:	00112e23          	sw	ra,28(sp)
   1012c:	00812c23          	sw	s0,24(sp)
   10130:	02010413          	addi	s0,sp,32
   10134:	fea42623          	sw	a0,-20(s0)
   10138:	feb42423          	sw	a1,-24(s0)
   1013c:	fec42223          	sw	a2,-28(s0)
   10140:	fed42023          	sw	a3,-32(s0)
   10144:	fec42783          	lw	a5,-20(s0)
   10148:	0007a023          	sw	zero,0(a5)
   1014c:	fe842503          	lw	a0,-24(s0)
   10150:	f5dff0ef          	jal	ra,100ac <turnOff>
   10154:	fe442503          	lw	a0,-28(s0)
   10158:	f1dff0ef          	jal	ra,10074 <turnOn>
   1015c:	fe042783          	lw	a5,-32(s0)
   10160:	00100713          	li	a4,1
   10164:	00e7a023          	sw	a4,0(a5)
   10168:	00000013          	nop
   1016c:	01c12083          	lw	ra,28(sp)
   10170:	01812403          	lw	s0,24(sp)
   10174:	02010113          	addi	sp,sp,32
   10178:	00008067          	ret

0001017c <turnOffLight>:
   1017c:	fe010113          	addi	sp,sp,-32
   10180:	00112e23          	sw	ra,28(sp)
   10184:	00812c23          	sw	s0,24(sp)
   10188:	02010413          	addi	s0,sp,32
   1018c:	fea42623          	sw	a0,-20(s0)
   10190:	feb42423          	sw	a1,-24(s0)
   10194:	fec42223          	sw	a2,-28(s0)
   10198:	fed42023          	sw	a3,-32(s0)
   1019c:	fec42783          	lw	a5,-20(s0)
   101a0:	0007a023          	sw	zero,0(a5)
   101a4:	fe842503          	lw	a0,-24(s0)
   101a8:	f05ff0ef          	jal	ra,100ac <turnOff>
   101ac:	fe442503          	lw	a0,-28(s0)
   101b0:	ec5ff0ef          	jal	ra,10074 <turnOn>
   101b4:	fe042783          	lw	a5,-32(s0)
   101b8:	00100713          	li	a4,1
   101bc:	00e7a023          	sw	a4,0(a5)
   101c0:	00000013          	nop
   101c4:	01c12083          	lw	ra,28(sp)
   101c8:	01812403          	lw	s0,24(sp)
   101cc:	02010113          	addi	sp,sp,32
   101d0:	00008067          	ret

000101d4 <turnOffPriorityLight>:
   101d4:	fd010113          	addi	sp,sp,-48
   101d8:	02112623          	sw	ra,44(sp)
   101dc:	02812423          	sw	s0,40(sp)
   101e0:	03010413          	addi	s0,sp,48
   101e4:	fca42e23          	sw	a0,-36(s0)
   101e8:	fcb42c23          	sw	a1,-40(s0)
   101ec:	fcc42a23          	sw	a2,-44(s0)
   101f0:	fe042623          	sw	zero,-20(s0)
   101f4:	fd442503          	lw	a0,-44(s0)
   101f8:	eb5ff0ef          	jal	ra,100ac <turnOff>
   101fc:	fd842503          	lw	a0,-40(s0)
   10200:	e75ff0ef          	jal	ra,10074 <turnOn>
   10204:	0100006f          	j	10214 <turnOffPriorityLight+0x40>
   10208:	fec42783          	lw	a5,-20(s0)
   1020c:	00178793          	addi	a5,a5,1
   10210:	fef42623          	sw	a5,-20(s0)
   10214:	fec42703          	lw	a4,-20(s0)
   10218:	3e800793          	li	a5,1000
   1021c:	fef716e3          	bne	a4,a5,10208 <turnOffPriorityLight+0x34>
   10220:	fd842503          	lw	a0,-40(s0)
   10224:	e89ff0ef          	jal	ra,100ac <turnOff>
   10228:	fdc42503          	lw	a0,-36(s0)
   1022c:	e49ff0ef          	jal	ra,10074 <turnOn>
   10230:	00000013          	nop
   10234:	02c12083          	lw	ra,44(sp)
   10238:	02812403          	lw	s0,40(sp)
   1023c:	03010113          	addi	sp,sp,48
   10240:	00008067          	ret

00010244 <ONLimit>:
   10244:	fc010113          	addi	sp,sp,-64
   10248:	02112e23          	sw	ra,60(sp)
   1024c:	02812c23          	sw	s0,56(sp)
   10250:	04010413          	addi	s0,sp,64
   10254:	fca42e23          	sw	a0,-36(s0)
   10258:	fcb42c23          	sw	a1,-40(s0)
   1025c:	fcc42a23          	sw	a2,-44(s0)
   10260:	fcd42823          	sw	a3,-48(s0)
   10264:	fce42623          	sw	a4,-52(s0)
   10268:	00f00793          	li	a5,15
   1026c:	fef42623          	sw	a5,-20(s0)
   10270:	02d00793          	li	a5,45
   10274:	fef42423          	sw	a5,-24(s0)
   10278:	fe042023          	sw	zero,-32(s0)
   1027c:	fe042223          	sw	zero,-28(s0)
   10280:	fe040793          	addi	a5,s0,-32
   10284:	00078893          	mv	a7,a5
   10288:	00000813          	li	a6,0
   1028c:	fec42783          	lw	a5,-20(s0)
   10290:	fcc42703          	lw	a4,-52(s0)
   10294:	fd042683          	lw	a3,-48(s0)
   10298:	fd442603          	lw	a2,-44(s0)
   1029c:	fd842583          	lw	a1,-40(s0)
   102a0:	fdc42503          	lw	a0,-36(s0)
   102a4:	040000ef          	jal	ra,102e4 <perform>
   102a8:	fe040793          	addi	a5,s0,-32
   102ac:	00078893          	mv	a7,a5
   102b0:	00100813          	li	a6,1
   102b4:	fe842783          	lw	a5,-24(s0)
   102b8:	fcc42703          	lw	a4,-52(s0)
   102bc:	fd042683          	lw	a3,-48(s0)
   102c0:	fd442603          	lw	a2,-44(s0)
   102c4:	fd842583          	lw	a1,-40(s0)
   102c8:	fdc42503          	lw	a0,-36(s0)
   102cc:	018000ef          	jal	ra,102e4 <perform>
   102d0:	00000013          	nop
   102d4:	03c12083          	lw	ra,60(sp)
   102d8:	03812403          	lw	s0,56(sp)
   102dc:	04010113          	addi	sp,sp,64
   102e0:	00008067          	ret

000102e4 <perform>:
   102e4:	fa010113          	addi	sp,sp,-96
   102e8:	04112e23          	sw	ra,92(sp)
   102ec:	04812c23          	sw	s0,88(sp)
   102f0:	06010413          	addi	s0,sp,96
   102f4:	faa42e23          	sw	a0,-68(s0)
   102f8:	fab42c23          	sw	a1,-72(s0)
   102fc:	fac42a23          	sw	a2,-76(s0)
   10300:	fad42823          	sw	a3,-80(s0)
   10304:	fae42623          	sw	a4,-84(s0)
   10308:	faf42423          	sw	a5,-88(s0)
   1030c:	fb042223          	sw	a6,-92(s0)
   10310:	fb142023          	sw	a7,-96(s0)
   10314:	fe042623          	sw	zero,-20(s0)
   10318:	00100793          	li	a5,1
   1031c:	fef42423          	sw	a5,-24(s0)
   10320:	fa442783          	lw	a5,-92(s0)
   10324:	00078463          	beqz	a5,1032c <perform+0x48>
   10328:	fe042423          	sw	zero,-24(s0)
   1032c:	fe042223          	sw	zero,-28(s0)
   10330:	fe042023          	sw	zero,-32(s0)
   10334:	00100793          	li	a5,1
   10338:	fcf42a23          	sw	a5,-44(s0)
   1033c:	00100793          	li	a5,1
   10340:	fcf42823          	sw	a5,-48(s0)
   10344:	fc042623          	sw	zero,-52(s0)
   10348:	fc042423          	sw	zero,-56(s0)
   1034c:	fc042223          	sw	zero,-60(s0)
   10350:	fc042023          	sw	zero,-64(s0)
   10354:	fc042e23          	sw	zero,-36(s0)
   10358:	fc042c23          	sw	zero,-40(s0)
   1035c:	fa442783          	lw	a5,-92(s0)
   10360:	00078e63          	beqz	a5,1037c <perform+0x98>
   10364:	fa042783          	lw	a5,-96(s0)
   10368:	0007a783          	lw	a5,0(a5)
   1036c:	00078863          	beqz	a5,1037c <perform+0x98>
   10370:	fc042a23          	sw	zero,-44(s0)
   10374:	00100793          	li	a5,1
   10378:	fcf42623          	sw	a5,-52(s0)
   1037c:	fa442783          	lw	a5,-92(s0)
   10380:	02078063          	beqz	a5,103a0 <perform+0xbc>
   10384:	fa042783          	lw	a5,-96(s0)
   10388:	00478793          	addi	a5,a5,4
   1038c:	0007a783          	lw	a5,0(a5)
   10390:	00078863          	beqz	a5,103a0 <perform+0xbc>
   10394:	fc042823          	sw	zero,-48(s0)
   10398:	00100793          	li	a5,1
   1039c:	fcf42423          	sw	a5,-56(s0)
   103a0:	fe842783          	lw	a5,-24(s0)
   103a4:	00279793          	slli	a5,a5,0x2
   103a8:	fbc42703          	lw	a4,-68(s0)
   103ac:	00f707b3          	add	a5,a4,a5
   103b0:	0007a783          	lw	a5,0(a5)
   103b4:	00078513          	mv	a0,a5
   103b8:	d31ff0ef          	jal	ra,100e8 <getValue>
   103bc:	00050793          	mv	a5,a0
   103c0:	04078063          	beqz	a5,10400 <perform+0x11c>
   103c4:	fe842783          	lw	a5,-24(s0)
   103c8:	00279793          	slli	a5,a5,0x2
   103cc:	fb442703          	lw	a4,-76(s0)
   103d0:	00f707b3          	add	a5,a4,a5
   103d4:	0007a583          	lw	a1,0(a5)
   103d8:	fe842783          	lw	a5,-24(s0)
   103dc:	00279793          	slli	a5,a5,0x2
   103e0:	fac42703          	lw	a4,-84(s0)
   103e4:	00f707b3          	add	a5,a4,a5
   103e8:	0007a703          	lw	a4,0(a5)
   103ec:	fcc40693          	addi	a3,s0,-52
   103f0:	fd440793          	addi	a5,s0,-44
   103f4:	00070613          	mv	a2,a4
   103f8:	00078513          	mv	a0,a5
   103fc:	d81ff0ef          	jal	ra,1017c <turnOffLight>
   10400:	fe842783          	lw	a5,-24(s0)
   10404:	00279793          	slli	a5,a5,0x2
   10408:	fb842703          	lw	a4,-72(s0)
   1040c:	00f707b3          	add	a5,a4,a5
   10410:	0007a783          	lw	a5,0(a5)
   10414:	00078513          	mv	a0,a5
   10418:	cd1ff0ef          	jal	ra,100e8 <getValue>
   1041c:	00050793          	mv	a5,a0
   10420:	30078663          	beqz	a5,1072c <perform+0x448>
   10424:	fe842783          	lw	a5,-24(s0)
   10428:	00278793          	addi	a5,a5,2
   1042c:	00279793          	slli	a5,a5,0x2
   10430:	fb442703          	lw	a4,-76(s0)
   10434:	00f707b3          	add	a5,a4,a5
   10438:	0007a583          	lw	a1,0(a5)
   1043c:	fe842783          	lw	a5,-24(s0)
   10440:	00278793          	addi	a5,a5,2
   10444:	00279793          	slli	a5,a5,0x2
   10448:	fac42703          	lw	a4,-84(s0)
   1044c:	00f707b3          	add	a5,a4,a5
   10450:	0007a703          	lw	a4,0(a5)
   10454:	fc840693          	addi	a3,s0,-56
   10458:	fd040793          	addi	a5,s0,-48
   1045c:	00070613          	mv	a2,a4
   10460:	00078513          	mv	a0,a5
   10464:	d19ff0ef          	jal	ra,1017c <turnOffLight>
   10468:	2c40006f          	j	1072c <perform+0x448>
   1046c:	fcc42783          	lw	a5,-52(s0)
   10470:	08078663          	beqz	a5,104fc <perform+0x218>
   10474:	fe842783          	lw	a5,-24(s0)
   10478:	00279793          	slli	a5,a5,0x2
   1047c:	fbc42703          	lw	a4,-68(s0)
   10480:	00f707b3          	add	a5,a4,a5
   10484:	0007a783          	lw	a5,0(a5)
   10488:	00078513          	mv	a0,a5
   1048c:	c5dff0ef          	jal	ra,100e8 <getValue>
   10490:	00050793          	mv	a5,a0
   10494:	02078663          	beqz	a5,104c0 <perform+0x1dc>
   10498:	fa842703          	lw	a4,-88(s0)
   1049c:	00070793          	mv	a5,a4
   104a0:	00579793          	slli	a5,a5,0x5
   104a4:	40e787b3          	sub	a5,a5,a4
   104a8:	00279793          	slli	a5,a5,0x2
   104ac:	00e787b3          	add	a5,a5,a4
   104b0:	00379793          	slli	a5,a5,0x3
   104b4:	00078713          	mv	a4,a5
   104b8:	fec42783          	lw	a5,-20(s0)
   104bc:	04e7c063          	blt	a5,a4,104fc <perform+0x218>
   104c0:	fe842783          	lw	a5,-24(s0)
   104c4:	00279793          	slli	a5,a5,0x2
   104c8:	fac42703          	lw	a4,-84(s0)
   104cc:	00f707b3          	add	a5,a4,a5
   104d0:	0007a583          	lw	a1,0(a5)
   104d4:	fe842783          	lw	a5,-24(s0)
   104d8:	00279793          	slli	a5,a5,0x2
   104dc:	fb042703          	lw	a4,-80(s0)
   104e0:	00f707b3          	add	a5,a4,a5
   104e4:	0007a703          	lw	a4,0(a5)
   104e8:	fc440693          	addi	a3,s0,-60
   104ec:	fcc40793          	addi	a5,s0,-52
   104f0:	00070613          	mv	a2,a4
   104f4:	00078513          	mv	a0,a5
   104f8:	c2dff0ef          	jal	ra,10124 <turnOnYellow>
   104fc:	fc842783          	lw	a5,-56(s0)
   10500:	08078a63          	beqz	a5,10594 <perform+0x2b0>
   10504:	fe842783          	lw	a5,-24(s0)
   10508:	00279793          	slli	a5,a5,0x2
   1050c:	fb842703          	lw	a4,-72(s0)
   10510:	00f707b3          	add	a5,a4,a5
   10514:	0007a783          	lw	a5,0(a5)
   10518:	00078513          	mv	a0,a5
   1051c:	bcdff0ef          	jal	ra,100e8 <getValue>
   10520:	00050793          	mv	a5,a0
   10524:	02078663          	beqz	a5,10550 <perform+0x26c>
   10528:	fa842703          	lw	a4,-88(s0)
   1052c:	00070793          	mv	a5,a4
   10530:	00579793          	slli	a5,a5,0x5
   10534:	40e787b3          	sub	a5,a5,a4
   10538:	00279793          	slli	a5,a5,0x2
   1053c:	00e787b3          	add	a5,a5,a4
   10540:	00379793          	slli	a5,a5,0x3
   10544:	00078713          	mv	a4,a5
   10548:	fec42783          	lw	a5,-20(s0)
   1054c:	04e7c463          	blt	a5,a4,10594 <perform+0x2b0>
   10550:	fe842783          	lw	a5,-24(s0)
   10554:	00278793          	addi	a5,a5,2
   10558:	00279793          	slli	a5,a5,0x2
   1055c:	fac42703          	lw	a4,-84(s0)
   10560:	00f707b3          	add	a5,a4,a5
   10564:	0007a583          	lw	a1,0(a5)
   10568:	fe842783          	lw	a5,-24(s0)
   1056c:	00278793          	addi	a5,a5,2
   10570:	00279793          	slli	a5,a5,0x2
   10574:	fb042703          	lw	a4,-80(s0)
   10578:	00f707b3          	add	a5,a4,a5
   1057c:	0007a703          	lw	a4,0(a5)
   10580:	fc040693          	addi	a3,s0,-64
   10584:	fc840793          	addi	a5,s0,-56
   10588:	00070613          	mv	a2,a4
   1058c:	00078513          	mv	a0,a5
   10590:	b95ff0ef          	jal	ra,10124 <turnOnYellow>
   10594:	fc442783          	lw	a5,-60(s0)
   10598:	04078663          	beqz	a5,105e4 <perform+0x300>
   1059c:	fdc42703          	lw	a4,-36(s0)
   105a0:	3e700793          	li	a5,999
   105a4:	04e7d063          	bge	a5,a4,105e4 <perform+0x300>
   105a8:	fe842783          	lw	a5,-24(s0)
   105ac:	00279793          	slli	a5,a5,0x2
   105b0:	fb042703          	lw	a4,-80(s0)
   105b4:	00f707b3          	add	a5,a4,a5
   105b8:	0007a583          	lw	a1,0(a5)
   105bc:	fe842783          	lw	a5,-24(s0)
   105c0:	00279793          	slli	a5,a5,0x2
   105c4:	fb442703          	lw	a4,-76(s0)
   105c8:	00f707b3          	add	a5,a4,a5
   105cc:	0007a703          	lw	a4,0(a5)
   105d0:	fd440693          	addi	a3,s0,-44
   105d4:	fc440793          	addi	a5,s0,-60
   105d8:	00070613          	mv	a2,a4
   105dc:	00078513          	mv	a0,a5
   105e0:	b9dff0ef          	jal	ra,1017c <turnOffLight>
   105e4:	fc042783          	lw	a5,-64(s0)
   105e8:	04078a63          	beqz	a5,1063c <perform+0x358>
   105ec:	fd842703          	lw	a4,-40(s0)
   105f0:	3e700793          	li	a5,999
   105f4:	04e7d463          	bge	a5,a4,1063c <perform+0x358>
   105f8:	fe842783          	lw	a5,-24(s0)
   105fc:	00278793          	addi	a5,a5,2
   10600:	00279793          	slli	a5,a5,0x2
   10604:	fb042703          	lw	a4,-80(s0)
   10608:	00f707b3          	add	a5,a4,a5
   1060c:	0007a583          	lw	a1,0(a5)
   10610:	fe842783          	lw	a5,-24(s0)
   10614:	00278793          	addi	a5,a5,2
   10618:	00279793          	slli	a5,a5,0x2
   1061c:	fb442703          	lw	a4,-76(s0)
   10620:	00f707b3          	add	a5,a4,a5
   10624:	0007a703          	lw	a4,0(a5)
   10628:	fd040693          	addi	a3,s0,-48
   1062c:	fc040793          	addi	a5,s0,-64
   10630:	00070613          	mv	a2,a4
   10634:	00078513          	mv	a0,a5
   10638:	b45ff0ef          	jal	ra,1017c <turnOffLight>
   1063c:	fa442783          	lw	a5,-92(s0)
   10640:	04079a63          	bnez	a5,10694 <perform+0x3b0>
   10644:	fd042783          	lw	a5,-48(s0)
   10648:	04078663          	beqz	a5,10694 <perform+0x3b0>
   1064c:	fe442783          	lw	a5,-28(s0)
   10650:	04079263          	bnez	a5,10694 <perform+0x3b0>
   10654:	fbc42783          	lw	a5,-68(s0)
   10658:	0007a783          	lw	a5,0(a5)
   1065c:	00078513          	mv	a0,a5
   10660:	a89ff0ef          	jal	ra,100e8 <getValue>
   10664:	00050793          	mv	a5,a0
   10668:	02078663          	beqz	a5,10694 <perform+0x3b0>
   1066c:	00100793          	li	a5,1
   10670:	fef42223          	sw	a5,-28(s0)
   10674:	fb442783          	lw	a5,-76(s0)
   10678:	0007a783          	lw	a5,0(a5)
   1067c:	00078513          	mv	a0,a5
   10680:	a2dff0ef          	jal	ra,100ac <turnOff>
   10684:	fac42783          	lw	a5,-84(s0)
   10688:	0007a783          	lw	a5,0(a5)
   1068c:	00078513          	mv	a0,a5
   10690:	9e5ff0ef          	jal	ra,10074 <turnOn>
   10694:	fa442783          	lw	a5,-92(s0)
   10698:	06079063          	bnez	a5,106f8 <perform+0x414>
   1069c:	fd442783          	lw	a5,-44(s0)
   106a0:	04078c63          	beqz	a5,106f8 <perform+0x414>
   106a4:	fe042783          	lw	a5,-32(s0)
   106a8:	04079863          	bnez	a5,106f8 <perform+0x414>
   106ac:	fbc42783          	lw	a5,-68(s0)
   106b0:	00878793          	addi	a5,a5,8
   106b4:	0007a783          	lw	a5,0(a5)
   106b8:	00078513          	mv	a0,a5
   106bc:	a2dff0ef          	jal	ra,100e8 <getValue>
   106c0:	00050793          	mv	a5,a0
   106c4:	02078a63          	beqz	a5,106f8 <perform+0x414>
   106c8:	00100793          	li	a5,1
   106cc:	fef42023          	sw	a5,-32(s0)
   106d0:	fb442783          	lw	a5,-76(s0)
   106d4:	00878793          	addi	a5,a5,8
   106d8:	0007a783          	lw	a5,0(a5)
   106dc:	00078513          	mv	a0,a5
   106e0:	9cdff0ef          	jal	ra,100ac <turnOff>
   106e4:	fac42783          	lw	a5,-84(s0)
   106e8:	00878793          	addi	a5,a5,8
   106ec:	0007a783          	lw	a5,0(a5)
   106f0:	00078513          	mv	a0,a5
   106f4:	981ff0ef          	jal	ra,10074 <turnOn>
   106f8:	fec42783          	lw	a5,-20(s0)
   106fc:	00178793          	addi	a5,a5,1
   10700:	fef42623          	sw	a5,-20(s0)
   10704:	fc442783          	lw	a5,-60(s0)
   10708:	00078863          	beqz	a5,10718 <perform+0x434>
   1070c:	fdc42783          	lw	a5,-36(s0)
   10710:	00178793          	addi	a5,a5,1
   10714:	fcf42e23          	sw	a5,-36(s0)
   10718:	fc042783          	lw	a5,-64(s0)
   1071c:	00078863          	beqz	a5,1072c <perform+0x448>
   10720:	fd842783          	lw	a5,-40(s0)
   10724:	00178793          	addi	a5,a5,1
   10728:	fcf42c23          	sw	a5,-40(s0)
   1072c:	fd442783          	lw	a5,-44(s0)
   10730:	d2078ee3          	beqz	a5,1046c <perform+0x188>
   10734:	fd042783          	lw	a5,-48(s0)
   10738:	d2078ae3          	beqz	a5,1046c <perform+0x188>
   1073c:	fa042783          	lw	a5,-96(s0)
   10740:	fe442703          	lw	a4,-28(s0)
   10744:	00e7a023          	sw	a4,0(a5)
   10748:	fa042783          	lw	a5,-96(s0)
   1074c:	00478793          	addi	a5,a5,4
   10750:	fe042703          	lw	a4,-32(s0)
   10754:	00e7a023          	sw	a4,0(a5)
   10758:	00000013          	nop
   1075c:	05c12083          	lw	ra,92(sp)
   10760:	05812403          	lw	s0,88(sp)
   10764:	06010113          	addi	sp,sp,96
   10768:	00008067          	ret

0001076c <call>:
   1076c:	f9010113          	addi	sp,sp,-112
   10770:	06112623          	sw	ra,108(sp)
   10774:	06812423          	sw	s0,104(sp)
   10778:	07010413          	addi	s0,sp,112
   1077c:	faa42623          	sw	a0,-84(s0)
   10780:	fab42423          	sw	a1,-88(s0)
   10784:	fac42223          	sw	a2,-92(s0)
   10788:	fad42023          	sw	a3,-96(s0)
   1078c:	f8e42e23          	sw	a4,-100(s0)
   10790:	f8f42c23          	sw	a5,-104(s0)
   10794:	f9042a23          	sw	a6,-108(s0)
   10798:	f9142823          	sw	a7,-112(s0)
   1079c:	00042783          	lw	a5,0(s0)
   107a0:	00279793          	slli	a5,a5,0x2
   107a4:	fac42703          	lw	a4,-84(s0)
   107a8:	00f707b3          	add	a5,a4,a5
   107ac:	0007a783          	lw	a5,0(a5)
   107b0:	fef42423          	sw	a5,-24(s0)
   107b4:	00042783          	lw	a5,0(s0)
   107b8:	00279793          	slli	a5,a5,0x2
   107bc:	fa842703          	lw	a4,-88(s0)
   107c0:	00f707b3          	add	a5,a4,a5
   107c4:	0007a783          	lw	a5,0(a5)
   107c8:	fef42623          	sw	a5,-20(s0)
   107cc:	00042783          	lw	a5,0(s0)
   107d0:	00178793          	addi	a5,a5,1
   107d4:	00279793          	slli	a5,a5,0x2
   107d8:	fac42703          	lw	a4,-84(s0)
   107dc:	00f707b3          	add	a5,a4,a5
   107e0:	0007a783          	lw	a5,0(a5)
   107e4:	fef42023          	sw	a5,-32(s0)
   107e8:	00042783          	lw	a5,0(s0)
   107ec:	00178793          	addi	a5,a5,1
   107f0:	00279793          	slli	a5,a5,0x2
   107f4:	fa842703          	lw	a4,-88(s0)
   107f8:	00f707b3          	add	a5,a4,a5
   107fc:	0007a783          	lw	a5,0(a5)
   10800:	fef42223          	sw	a5,-28(s0)
   10804:	00042783          	lw	a5,0(s0)
   10808:	00279793          	slli	a5,a5,0x2
   1080c:	fa442703          	lw	a4,-92(s0)
   10810:	00f707b3          	add	a5,a4,a5
   10814:	0007a783          	lw	a5,0(a5)
   10818:	fcf42823          	sw	a5,-48(s0)
   1081c:	00042783          	lw	a5,0(s0)
   10820:	00279793          	slli	a5,a5,0x2
   10824:	fa042703          	lw	a4,-96(s0)
   10828:	00f707b3          	add	a5,a4,a5
   1082c:	0007a783          	lw	a5,0(a5)
   10830:	fcf42a23          	sw	a5,-44(s0)
   10834:	00042783          	lw	a5,0(s0)
   10838:	00178793          	addi	a5,a5,1
   1083c:	00279793          	slli	a5,a5,0x2
   10840:	fa442703          	lw	a4,-92(s0)
   10844:	00f707b3          	add	a5,a4,a5
   10848:	0007a783          	lw	a5,0(a5)
   1084c:	fcf42c23          	sw	a5,-40(s0)
   10850:	00042783          	lw	a5,0(s0)
   10854:	00178793          	addi	a5,a5,1
   10858:	00279793          	slli	a5,a5,0x2
   1085c:	fa042703          	lw	a4,-96(s0)
   10860:	00f707b3          	add	a5,a4,a5
   10864:	0007a783          	lw	a5,0(a5)
   10868:	fcf42e23          	sw	a5,-36(s0)
   1086c:	00042783          	lw	a5,0(s0)
   10870:	00279793          	slli	a5,a5,0x2
   10874:	f9c42703          	lw	a4,-100(s0)
   10878:	00f707b3          	add	a5,a4,a5
   1087c:	0007a783          	lw	a5,0(a5)
   10880:	fcf42023          	sw	a5,-64(s0)
   10884:	00042783          	lw	a5,0(s0)
   10888:	00279793          	slli	a5,a5,0x2
   1088c:	f9842703          	lw	a4,-104(s0)
   10890:	00f707b3          	add	a5,a4,a5
   10894:	0007a783          	lw	a5,0(a5)
   10898:	fcf42223          	sw	a5,-60(s0)
   1089c:	00042783          	lw	a5,0(s0)
   108a0:	00178793          	addi	a5,a5,1
   108a4:	00279793          	slli	a5,a5,0x2
   108a8:	f9c42703          	lw	a4,-100(s0)
   108ac:	00f707b3          	add	a5,a4,a5
   108b0:	0007a783          	lw	a5,0(a5)
   108b4:	fcf42423          	sw	a5,-56(s0)
   108b8:	00042783          	lw	a5,0(s0)
   108bc:	00178793          	addi	a5,a5,1
   108c0:	00279793          	slli	a5,a5,0x2
   108c4:	f9842703          	lw	a4,-104(s0)
   108c8:	00f707b3          	add	a5,a4,a5
   108cc:	0007a783          	lw	a5,0(a5)
   108d0:	fcf42623          	sw	a5,-52(s0)
   108d4:	00042783          	lw	a5,0(s0)
   108d8:	00279793          	slli	a5,a5,0x2
   108dc:	f9442703          	lw	a4,-108(s0)
   108e0:	00f707b3          	add	a5,a4,a5
   108e4:	0007a783          	lw	a5,0(a5)
   108e8:	faf42823          	sw	a5,-80(s0)
   108ec:	00042783          	lw	a5,0(s0)
   108f0:	00279793          	slli	a5,a5,0x2
   108f4:	f9042703          	lw	a4,-112(s0)
   108f8:	00f707b3          	add	a5,a4,a5
   108fc:	0007a783          	lw	a5,0(a5)
   10900:	faf42a23          	sw	a5,-76(s0)
   10904:	00042783          	lw	a5,0(s0)
   10908:	00178793          	addi	a5,a5,1
   1090c:	00279793          	slli	a5,a5,0x2
   10910:	f9442703          	lw	a4,-108(s0)
   10914:	00f707b3          	add	a5,a4,a5
   10918:	0007a783          	lw	a5,0(a5)
   1091c:	faf42c23          	sw	a5,-72(s0)
   10920:	00042783          	lw	a5,0(s0)
   10924:	00178793          	addi	a5,a5,1
   10928:	00279793          	slli	a5,a5,0x2
   1092c:	f9042703          	lw	a4,-112(s0)
   10930:	00f707b3          	add	a5,a4,a5
   10934:	0007a783          	lw	a5,0(a5)
   10938:	faf42e23          	sw	a5,-68(s0)
   1093c:	fb040713          	addi	a4,s0,-80
   10940:	fc040693          	addi	a3,s0,-64
   10944:	fd040613          	addi	a2,s0,-48
   10948:	fe040593          	addi	a1,s0,-32
   1094c:	fe840793          	addi	a5,s0,-24
   10950:	00078513          	mv	a0,a5
   10954:	8f1ff0ef          	jal	ra,10244 <ONLimit>
   10958:	00000013          	nop
   1095c:	06c12083          	lw	ra,108(sp)
   10960:	06812403          	lw	s0,104(sp)
   10964:	07010113          	addi	sp,sp,112
   10968:	00008067          	ret

0001096c <main>:
   1096c:	f4010113          	addi	sp,sp,-192
   10970:	0a112e23          	sw	ra,188(sp)
   10974:	0a812c23          	sw	s0,184(sp)
   10978:	0c010413          	addi	s0,sp,192
   1097c:	000117b7          	lui	a5,0x11
   10980:	f1078793          	addi	a5,a5,-240 # 10f10 <main+0x5a4>
   10984:	0007a603          	lw	a2,0(a5)
   10988:	0047a683          	lw	a3,4(a5)
   1098c:	0087a703          	lw	a4,8(a5)
   10990:	00c7a783          	lw	a5,12(a5)
   10994:	fcc42223          	sw	a2,-60(s0)
   10998:	fcd42423          	sw	a3,-56(s0)
   1099c:	fce42623          	sw	a4,-52(s0)
   109a0:	fcf42823          	sw	a5,-48(s0)
   109a4:	000117b7          	lui	a5,0x11
   109a8:	f2078793          	addi	a5,a5,-224 # 10f20 <main+0x5b4>
   109ac:	0007a603          	lw	a2,0(a5)
   109b0:	0047a683          	lw	a3,4(a5)
   109b4:	0087a703          	lw	a4,8(a5)
   109b8:	00c7a783          	lw	a5,12(a5)
   109bc:	fac42a23          	sw	a2,-76(s0)
   109c0:	fad42c23          	sw	a3,-72(s0)
   109c4:	fae42e23          	sw	a4,-68(s0)
   109c8:	fcf42023          	sw	a5,-64(s0)
   109cc:	000117b7          	lui	a5,0x11
   109d0:	f3078793          	addi	a5,a5,-208 # 10f30 <main+0x5c4>
   109d4:	0007a603          	lw	a2,0(a5)
   109d8:	0047a683          	lw	a3,4(a5)
   109dc:	0087a703          	lw	a4,8(a5)
   109e0:	00c7a783          	lw	a5,12(a5)
   109e4:	fac42223          	sw	a2,-92(s0)
   109e8:	fad42423          	sw	a3,-88(s0)
   109ec:	fae42623          	sw	a4,-84(s0)
   109f0:	faf42823          	sw	a5,-80(s0)
   109f4:	000117b7          	lui	a5,0x11
   109f8:	f4078793          	addi	a5,a5,-192 # 10f40 <main+0x5d4>
   109fc:	0007a603          	lw	a2,0(a5)
   10a00:	0047a683          	lw	a3,4(a5)
   10a04:	0087a703          	lw	a4,8(a5)
   10a08:	00c7a783          	lw	a5,12(a5)
   10a0c:	f8c42a23          	sw	a2,-108(s0)
   10a10:	f8d42c23          	sw	a3,-104(s0)
   10a14:	f8e42e23          	sw	a4,-100(s0)
   10a18:	faf42023          	sw	a5,-96(s0)
   10a1c:	000117b7          	lui	a5,0x11
   10a20:	f5078793          	addi	a5,a5,-176 # 10f50 <main+0x5e4>
   10a24:	0007a603          	lw	a2,0(a5)
   10a28:	0047a683          	lw	a3,4(a5)
   10a2c:	0087a703          	lw	a4,8(a5)
   10a30:	00c7a783          	lw	a5,12(a5)
   10a34:	f8c42223          	sw	a2,-124(s0)
   10a38:	f8d42423          	sw	a3,-120(s0)
   10a3c:	f8e42623          	sw	a4,-116(s0)
   10a40:	f8f42823          	sw	a5,-112(s0)
   10a44:	000117b7          	lui	a5,0x11
   10a48:	f6078793          	addi	a5,a5,-160 # 10f60 <main+0x5f4>
   10a4c:	0007a603          	lw	a2,0(a5)
   10a50:	0047a683          	lw	a3,4(a5)
   10a54:	0087a703          	lw	a4,8(a5)
   10a58:	00c7a783          	lw	a5,12(a5)
   10a5c:	f6c42a23          	sw	a2,-140(s0)
   10a60:	f6d42c23          	sw	a3,-136(s0)
   10a64:	f6e42e23          	sw	a4,-132(s0)
   10a68:	f8f42023          	sw	a5,-128(s0)
   10a6c:	000117b7          	lui	a5,0x11
   10a70:	f7078793          	addi	a5,a5,-144 # 10f70 <main+0x604>
   10a74:	0007a603          	lw	a2,0(a5)
   10a78:	0047a683          	lw	a3,4(a5)
   10a7c:	0087a703          	lw	a4,8(a5)
   10a80:	00c7a783          	lw	a5,12(a5)
   10a84:	f6c42223          	sw	a2,-156(s0)
   10a88:	f6d42423          	sw	a3,-152(s0)
   10a8c:	f6e42623          	sw	a4,-148(s0)
   10a90:	f6f42823          	sw	a5,-144(s0)
   10a94:	000117b7          	lui	a5,0x11
   10a98:	f8078793          	addi	a5,a5,-128 # 10f80 <main+0x614>
   10a9c:	0007a603          	lw	a2,0(a5)
   10aa0:	0047a683          	lw	a3,4(a5)
   10aa4:	0087a703          	lw	a4,8(a5)
   10aa8:	00c7a783          	lw	a5,12(a5)
   10aac:	f4c42a23          	sw	a2,-172(s0)
   10ab0:	f4d42c23          	sw	a3,-168(s0)
   10ab4:	f4e42e23          	sw	a4,-164(s0)
   10ab8:	f6f42023          	sw	a5,-160(s0)
   10abc:	fe042623          	sw	zero,-20(s0)
   10ac0:	000f7f13          	andi	t5,t5,0
   10ac4:	fe042423          	sw	zero,-24(s0)
   10ac8:	fe042223          	sw	zero,-28(s0)
   10acc:	0580006f          	j	10b24 <main+0x1b8>
   10ad0:	fe442783          	lw	a5,-28(s0)
   10ad4:	00279793          	slli	a5,a5,0x2
   10ad8:	ff040713          	addi	a4,s0,-16
   10adc:	00f707b3          	add	a5,a4,a5
   10ae0:	fb47a783          	lw	a5,-76(a5)
   10ae4:	00100713          	li	a4,1
   10ae8:	00f71733          	sll	a4,a4,a5
   10aec:	fe442783          	lw	a5,-28(s0)
   10af0:	00279793          	slli	a5,a5,0x2
   10af4:	ff040693          	addi	a3,s0,-16
   10af8:	00f687b3          	add	a5,a3,a5
   10afc:	fa47a783          	lw	a5,-92(a5)
   10b00:	00100693          	li	a3,1
   10b04:	00f697b3          	sll	a5,a3,a5
   10b08:	00f767b3          	or	a5,a4,a5
   10b0c:	fe842703          	lw	a4,-24(s0)
   10b10:	00f767b3          	or	a5,a4,a5
   10b14:	fef42423          	sw	a5,-24(s0)
   10b18:	fe442783          	lw	a5,-28(s0)
   10b1c:	00178793          	addi	a5,a5,1
   10b20:	fef42223          	sw	a5,-28(s0)
   10b24:	fe442703          	lw	a4,-28(s0)
   10b28:	00300793          	li	a5,3
   10b2c:	fae7d2e3          	bge	a5,a4,10ad0 <main+0x164>
   10b30:	fe842783          	lw	a5,-24(s0)
   10b34:	00ff6f33          	or	t5,t5,a5
   10b38:	d1cff0ef          	jal	ra,10054 <priority>
   10b3c:	fca42a23          	sw	a0,-44(s0)
   10b40:	fe042023          	sw	zero,-32(s0)
   10b44:	fc042e23          	sw	zero,-36(s0)
   10b48:	fc042c23          	sw	zero,-40(s0)
   10b4c:	0640006f          	j	10bb0 <main+0x244>
   10b50:	fd842783          	lw	a5,-40(s0)
   10b54:	00279793          	slli	a5,a5,0x2
   10b58:	ff040713          	addi	a4,s0,-16
   10b5c:	00f707b3          	add	a5,a4,a5
   10b60:	fd47a783          	lw	a5,-44(a5)
   10b64:	00078513          	mv	a0,a5
   10b68:	d80ff0ef          	jal	ra,100e8 <getValue>
   10b6c:	00050793          	mv	a5,a0
   10b70:	02079463          	bnez	a5,10b98 <main+0x22c>
   10b74:	fd842783          	lw	a5,-40(s0)
   10b78:	00279793          	slli	a5,a5,0x2
   10b7c:	ff040713          	addi	a4,s0,-16
   10b80:	00f707b3          	add	a5,a4,a5
   10b84:	fc47a783          	lw	a5,-60(a5)
   10b88:	00078513          	mv	a0,a5
   10b8c:	d5cff0ef          	jal	ra,100e8 <getValue>
   10b90:	00050793          	mv	a5,a0
   10b94:	00078863          	beqz	a5,10ba4 <main+0x238>
   10b98:	fdc42783          	lw	a5,-36(s0)
   10b9c:	00178793          	addi	a5,a5,1
   10ba0:	fcf42e23          	sw	a5,-36(s0)
   10ba4:	fd842783          	lw	a5,-40(s0)
   10ba8:	00178793          	addi	a5,a5,1
   10bac:	fcf42c23          	sw	a5,-40(s0)
   10bb0:	fd842703          	lw	a4,-40(s0)
   10bb4:	00300793          	li	a5,3
   10bb8:	f8e7dce3          	bge	a5,a4,10b50 <main+0x1e4>
   10bbc:	fdc42783          	lw	a5,-36(s0)
   10bc0:	30078263          	beqz	a5,10ec4 <main+0x558>
   10bc4:	fe042783          	lw	a5,-32(s0)
   10bc8:	04078a63          	beqz	a5,10c1c <main+0x2b0>
   10bcc:	fd442783          	lw	a5,-44(s0)
   10bd0:	00279793          	slli	a5,a5,0x2
   10bd4:	ff040713          	addi	a4,s0,-16
   10bd8:	00f707b3          	add	a5,a4,a5
   10bdc:	fb47a703          	lw	a4,-76(a5)
   10be0:	fd442783          	lw	a5,-44(s0)
   10be4:	00279793          	slli	a5,a5,0x2
   10be8:	ff040693          	addi	a3,s0,-16
   10bec:	00f687b3          	add	a5,a3,a5
   10bf0:	f947a683          	lw	a3,-108(a5)
   10bf4:	fd442783          	lw	a5,-44(s0)
   10bf8:	00279793          	slli	a5,a5,0x2
   10bfc:	ff040613          	addi	a2,s0,-16
   10c00:	00f607b3          	add	a5,a2,a5
   10c04:	f747a783          	lw	a5,-140(a5)
   10c08:	00078613          	mv	a2,a5
   10c0c:	00068593          	mv	a1,a3
   10c10:	00070513          	mv	a0,a4
   10c14:	dc0ff0ef          	jal	ra,101d4 <turnOffPriorityLight>
   10c18:	fe042023          	sw	zero,-32(s0)
   10c1c:	fdc42703          	lw	a4,-36(s0)
   10c20:	00400793          	li	a5,4
   10c24:	00f70863          	beq	a4,a5,10c34 <main+0x2c8>
   10c28:	fdc42703          	lw	a4,-36(s0)
   10c2c:	00300793          	li	a5,3
   10c30:	0af71463          	bne	a4,a5,10cd8 <main+0x36c>
   10c34:	f5440893          	addi	a7,s0,-172
   10c38:	f6440813          	addi	a6,s0,-156
   10c3c:	f7440313          	addi	t1,s0,-140
   10c40:	f8440713          	addi	a4,s0,-124
   10c44:	f9440693          	addi	a3,s0,-108
   10c48:	fa440613          	addi	a2,s0,-92
   10c4c:	fb440593          	addi	a1,s0,-76
   10c50:	fc440513          	addi	a0,s0,-60
   10c54:	fec42783          	lw	a5,-20(s0)
   10c58:	00f12023          	sw	a5,0(sp)
   10c5c:	00030793          	mv	a5,t1
   10c60:	b0dff0ef          	jal	ra,1076c <call>
   10c64:	fec42783          	lw	a5,-20(s0)
   10c68:	00278713          	addi	a4,a5,2
   10c6c:	41f75793          	srai	a5,a4,0x1f
   10c70:	01e7d793          	srli	a5,a5,0x1e
   10c74:	00f70733          	add	a4,a4,a5
   10c78:	00377713          	andi	a4,a4,3
   10c7c:	40f707b3          	sub	a5,a4,a5
   10c80:	fef42623          	sw	a5,-20(s0)
   10c84:	f5440893          	addi	a7,s0,-172
   10c88:	f6440813          	addi	a6,s0,-156
   10c8c:	f7440313          	addi	t1,s0,-140
   10c90:	f8440713          	addi	a4,s0,-124
   10c94:	f9440693          	addi	a3,s0,-108
   10c98:	fa440613          	addi	a2,s0,-92
   10c9c:	fb440593          	addi	a1,s0,-76
   10ca0:	fc440513          	addi	a0,s0,-60
   10ca4:	fec42783          	lw	a5,-20(s0)
   10ca8:	00f12023          	sw	a5,0(sp)
   10cac:	00030793          	mv	a5,t1
   10cb0:	abdff0ef          	jal	ra,1076c <call>
   10cb4:	fec42783          	lw	a5,-20(s0)
   10cb8:	00278713          	addi	a4,a5,2
   10cbc:	41f75793          	srai	a5,a4,0x1f
   10cc0:	01e7d793          	srli	a5,a5,0x1e
   10cc4:	00f70733          	add	a4,a4,a5
   10cc8:	00377713          	andi	a4,a4,3
   10ccc:	40f707b3          	sub	a5,a4,a5
   10cd0:	fef42623          	sw	a5,-20(s0)
   10cd4:	2380006f          	j	10f0c <main+0x5a0>
   10cd8:	fdc42703          	lw	a4,-36(s0)
   10cdc:	00200793          	li	a5,2
   10ce0:	00f70863          	beq	a4,a5,10cf0 <main+0x384>
   10ce4:	fdc42703          	lw	a4,-36(s0)
   10ce8:	00100793          	li	a5,1
   10cec:	e4f71ce3          	bne	a4,a5,10b44 <main+0x1d8>
   10cf0:	fec42783          	lw	a5,-20(s0)
   10cf4:	00279793          	slli	a5,a5,0x2
   10cf8:	ff040713          	addi	a4,s0,-16
   10cfc:	00f707b3          	add	a5,a4,a5
   10d00:	fd47a783          	lw	a5,-44(a5)
   10d04:	00078513          	mv	a0,a5
   10d08:	be0ff0ef          	jal	ra,100e8 <getValue>
   10d0c:	00050793          	mv	a5,a0
   10d10:	06079c63          	bnez	a5,10d88 <main+0x41c>
   10d14:	fec42783          	lw	a5,-20(s0)
   10d18:	00279793          	slli	a5,a5,0x2
   10d1c:	ff040713          	addi	a4,s0,-16
   10d20:	00f707b3          	add	a5,a4,a5
   10d24:	fc47a783          	lw	a5,-60(a5)
   10d28:	00078513          	mv	a0,a5
   10d2c:	bbcff0ef          	jal	ra,100e8 <getValue>
   10d30:	00050793          	mv	a5,a0
   10d34:	04079a63          	bnez	a5,10d88 <main+0x41c>
   10d38:	fec42783          	lw	a5,-20(s0)
   10d3c:	00178793          	addi	a5,a5,1
   10d40:	00279793          	slli	a5,a5,0x2
   10d44:	ff040713          	addi	a4,s0,-16
   10d48:	00f707b3          	add	a5,a4,a5
   10d4c:	fd47a783          	lw	a5,-44(a5)
   10d50:	00078513          	mv	a0,a5
   10d54:	b94ff0ef          	jal	ra,100e8 <getValue>
   10d58:	00050793          	mv	a5,a0
   10d5c:	02079663          	bnez	a5,10d88 <main+0x41c>
   10d60:	fec42783          	lw	a5,-20(s0)
   10d64:	00178793          	addi	a5,a5,1
   10d68:	00279793          	slli	a5,a5,0x2
   10d6c:	ff040713          	addi	a4,s0,-16
   10d70:	00f707b3          	add	a5,a4,a5
   10d74:	fc47a783          	lw	a5,-60(a5)
   10d78:	00078513          	mv	a0,a5
   10d7c:	b6cff0ef          	jal	ra,100e8 <getValue>
   10d80:	00050793          	mv	a5,a0
   10d84:	02078a63          	beqz	a5,10db8 <main+0x44c>
   10d88:	f5440893          	addi	a7,s0,-172
   10d8c:	f6440813          	addi	a6,s0,-156
   10d90:	f7440313          	addi	t1,s0,-140
   10d94:	f8440713          	addi	a4,s0,-124
   10d98:	f9440693          	addi	a3,s0,-108
   10d9c:	fa440613          	addi	a2,s0,-92
   10da0:	fb440593          	addi	a1,s0,-76
   10da4:	fc440513          	addi	a0,s0,-60
   10da8:	fec42783          	lw	a5,-20(s0)
   10dac:	00f12023          	sw	a5,0(sp)
   10db0:	00030793          	mv	a5,t1
   10db4:	9b9ff0ef          	jal	ra,1076c <call>
   10db8:	fec42783          	lw	a5,-20(s0)
   10dbc:	00278713          	addi	a4,a5,2
   10dc0:	41f75793          	srai	a5,a4,0x1f
   10dc4:	01e7d793          	srli	a5,a5,0x1e
   10dc8:	00f70733          	add	a4,a4,a5
   10dcc:	00377713          	andi	a4,a4,3
   10dd0:	40f707b3          	sub	a5,a4,a5
   10dd4:	fef42623          	sw	a5,-20(s0)
   10dd8:	fec42783          	lw	a5,-20(s0)
   10ddc:	00279793          	slli	a5,a5,0x2
   10de0:	ff040713          	addi	a4,s0,-16
   10de4:	00f707b3          	add	a5,a4,a5
   10de8:	fd47a783          	lw	a5,-44(a5)
   10dec:	00078513          	mv	a0,a5
   10df0:	af8ff0ef          	jal	ra,100e8 <getValue>
   10df4:	00050793          	mv	a5,a0
   10df8:	06079c63          	bnez	a5,10e70 <main+0x504>
   10dfc:	fec42783          	lw	a5,-20(s0)
   10e00:	00279793          	slli	a5,a5,0x2
   10e04:	ff040713          	addi	a4,s0,-16
   10e08:	00f707b3          	add	a5,a4,a5
   10e0c:	fc47a783          	lw	a5,-60(a5)
   10e10:	00078513          	mv	a0,a5
   10e14:	ad4ff0ef          	jal	ra,100e8 <getValue>
   10e18:	00050793          	mv	a5,a0
   10e1c:	04079a63          	bnez	a5,10e70 <main+0x504>
   10e20:	fec42783          	lw	a5,-20(s0)
   10e24:	00178793          	addi	a5,a5,1
   10e28:	00279793          	slli	a5,a5,0x2
   10e2c:	ff040713          	addi	a4,s0,-16
   10e30:	00f707b3          	add	a5,a4,a5
   10e34:	fd47a783          	lw	a5,-44(a5)
   10e38:	00078513          	mv	a0,a5
   10e3c:	aacff0ef          	jal	ra,100e8 <getValue>
   10e40:	00050793          	mv	a5,a0
   10e44:	02079663          	bnez	a5,10e70 <main+0x504>
   10e48:	fec42783          	lw	a5,-20(s0)
   10e4c:	00178793          	addi	a5,a5,1
   10e50:	00279793          	slli	a5,a5,0x2
   10e54:	ff040713          	addi	a4,s0,-16
   10e58:	00f707b3          	add	a5,a4,a5
   10e5c:	fc47a783          	lw	a5,-60(a5)
   10e60:	00078513          	mv	a0,a5
   10e64:	a84ff0ef          	jal	ra,100e8 <getValue>
   10e68:	00050793          	mv	a5,a0
   10e6c:	cc078ce3          	beqz	a5,10b44 <main+0x1d8>
   10e70:	f5440893          	addi	a7,s0,-172
   10e74:	f6440813          	addi	a6,s0,-156
   10e78:	f7440313          	addi	t1,s0,-140
   10e7c:	f8440713          	addi	a4,s0,-124
   10e80:	f9440693          	addi	a3,s0,-108
   10e84:	fa440613          	addi	a2,s0,-92
   10e88:	fb440593          	addi	a1,s0,-76
   10e8c:	fc440513          	addi	a0,s0,-60
   10e90:	fec42783          	lw	a5,-20(s0)
   10e94:	00f12023          	sw	a5,0(sp)
   10e98:	00030793          	mv	a5,t1
   10e9c:	8d1ff0ef          	jal	ra,1076c <call>
   10ea0:	fec42783          	lw	a5,-20(s0)
   10ea4:	00278713          	addi	a4,a5,2
   10ea8:	41f75793          	srai	a5,a4,0x1f
   10eac:	01e7d793          	srli	a5,a5,0x1e
   10eb0:	00f70733          	add	a4,a4,a5
   10eb4:	00377713          	andi	a4,a4,3
   10eb8:	40f707b3          	sub	a5,a4,a5
   10ebc:	fef42623          	sw	a5,-20(s0)
   10ec0:	c85ff06f          	j	10b44 <main+0x1d8>
   10ec4:	fe042783          	lw	a5,-32(s0)
   10ec8:	c6079ee3          	bnez	a5,10b44 <main+0x1d8>
   10ecc:	fd442783          	lw	a5,-44(s0)
   10ed0:	00279793          	slli	a5,a5,0x2
   10ed4:	ff040713          	addi	a4,s0,-16
   10ed8:	00f707b3          	add	a5,a4,a5
   10edc:	fb47a783          	lw	a5,-76(a5)
   10ee0:	00078513          	mv	a0,a5
   10ee4:	9c8ff0ef          	jal	ra,100ac <turnOff>
   10ee8:	fd442783          	lw	a5,-44(s0)
   10eec:	00279793          	slli	a5,a5,0x2
   10ef0:	ff040713          	addi	a4,s0,-16
   10ef4:	00f707b3          	add	a5,a4,a5
   10ef8:	f747a783          	lw	a5,-140(a5)
   10efc:	00078513          	mv	a0,a5
   10f00:	974ff0ef          	jal	ra,10074 <turnOn>
   10f04:	00100793          	li	a5,1
   10f08:	fef42023          	sw	a5,-32(s0)
   10f0c:	c39ff06f          	j	10b44 <main+0x1d8>
   ```
###NUMBER OF DIFFERENT INSTRUCTIONS: 27
```
addi
sw
li
mv
lw
ret
sll
or
nop
not
and
sra
andi
jal
j
bne
beqz
slli
add
sub
blt
bge
bnez
lui
beq
srai
srli
```
### CITATIONS
1) _Infrared (IR) Sensor Module with Arduino_. Solarduino. 12 Jan. 2020. [encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU](encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU). Accessed 30 Oct. 2023.
2) _IR Sensor Working_. Robocraze. [robocraze.com/blogs/post/ir-sensor-working](robocraze.com/blogs/post/ir-sensor-working). Accessed 30 Oct. 2023.
3) ShubhamGitHub528. “Automatic Garage Door System.” _Home Automation System_. Github. 28 Oct. 2023. [github.com/ShubhamGitHub528/Home-Automation-System](github.com/ShubhamGitHub528/Home-Automation-System). 
