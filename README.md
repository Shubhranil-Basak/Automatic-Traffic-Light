# Automatic Traffic Light
This repository contains RISC-V based traffic light automation.
# OVERVIEW
Traffic lights usually consists of three signals through the usage of colors, arrows, and other images to convey various messages. Traffic lights are in sets of red, yellow, and green lights at intersection of roads. Traffic is then controlled as vehicles receive signals/messages of when to stop and when to go.
# AIM
The project's goal is to design an automatic machine utilizing a specialized RISC-V processor for controlling traffic by releasing a specific number of cars and pedestrians depending on whoever comes first. The objective of this program is to minimize traffic problems, energy consumption, and overall expenses. 
# BLOCK DIAGRAM 
<img width="810" alt="Block Diagram" src="https://github.com/AryanAAB/Automatic-Traffic-Light/assets/142584708/0538173c-416c-49be-acfe-d18c96bad4db">

# MATERIALS REQUIRED
LED : https://tinyurl.com/yc5w423x : ₹125

IR Sensors : https://tinyurl.com/8dybpmhn : ₹510
# HOW DOES AN IR SENSOR WORK?
An IR Sensor consists of an IR LED trasmitter that emits infrared radition. It has the same appearance as a standard LED, but the radiation it emits is not visible to the human eye. If an object blocks the pathway of the infrared waves, then the reflected radiations are detected by the infrared receivers. The sensor output can be decided by the IR receiver depending on the intensity of the response. These infrared receivers are available in photodiode form. IR photodiode are different from regular photodiodes in that they only detect IR radiation. Different types of infrared receivers exist based on voltage, wavelength, package, and other factors.

When using an IR transmitter and receiver, the wavelength of the receiver must match that of the transmitter because the infrared photodiode is activated by the infrared light produced by the infrared LED. The photodiode’s resistance and the change in output voltage are proportional to the amount of infrared light obtained.

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/144095577/dd21f4aa-b0f3-4a6a-9c71-0b6cb3cbec00)


# REGISTER ARCHITECTURE for x30 for GPIOs

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

# Assembly Structure using C

```C
#include <time.h>
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
	asm volatile(
		"ori x30, x30, %0\n\t"
		:
		: "i"(pin_mask)
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
		"andi x30, x30, %0\n\t"
		:
		: "i"(pin_mask)
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
	while(difftime(currTime, startTime) <= 1)
		currTime = time(NULL);
	
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
	time_t startTime, currentTime;
	startTime = time(NULL);
		
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
			"ori x30, x30, %0\n\t" //x30 or pin_mask and store in x30 (%0 means go to first input that is given)
			:
			: "i"(pin_mask)
			: "x30"
		);

		int rand = randomNumber(0, 3);
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
				}
			}
		}
    return 0;
}
```

# Non-assembly code in C

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

# Screenshot

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/144095577/99e03b2b-898a-4eab-94e5-ef1cac09c7cb)

* In the first 4 line we can see that right turn red is on for all the lanes
* In line 5 we can see that yellow light is on for lane 4 straight
* This is because as Green light for lane 4 was on at the beginning
* And the sensor did not return any response as it did not detect any car
* Thus it instantly changes to yellow.
* In the next 3 line red light for the straight road is on for lane 1, 2 and 3 but not for lane 4
* All the other lines in set of 8 are the same thing and it will be the same.
* This code will run for 5 seconds.


# Citations
1) _Infrared (IR) Sensor Module with Arduino_. Solarduino. 12 Jan. 2020. [encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU](encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU). Accessed 30 Oct. 2023.
2) _IR Sensor Working_. Robocraze. [robocraze.com/blogs/post/ir-sensor-working](robocraze.com/blogs/post/ir-sensor-working). Accessed 30 Oct. 2023.
3) ShubhamGitHub528. “Automatic Garage Door System.” _Home Automation System_. Github. 28 Oct. 2023. [github.com/ShubhamGitHub528/Home-Automation-System](github.com/ShubhamGitHub528/Home-Automation-System). 
