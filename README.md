# AUTOMATIC TRAFFIC LIGHT
This repository contains RISC-V based traffic light automation.
### OVERVIEW
Traffic lights usually consists of three signals through the usage of colors, arrows, and other images to convey various messages. Traffic lights are in sets of red, yellow, and green lights at intersection of roads. Traffic is then controlled as vehicles receive signals/messages of when to stop and when to go.
### AIM
The project's goal is to design an automatic machine utilizing a specialized RISC-V processor for controlling traffic by releasing a specific number of cars and pedestrians depending on whoever comes first. The objective of this program is to minimize traffic problems, energy consumption, and overall expenses. 
### BLOCK DIAGRAM 
![Block Diagram](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/142584708/7f56479b-aab5-4d16-8394-f79927c6e400)

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
 * If nobody is present at the signals, this code would give priority to side 1
 */

//Function prototypes
void turnOn(const int);
void turnOff(const int);
int getValue(const int);
void turnOnYellow(int *, const int, const int, int *);
void turnOffLight(int *, const int, const int, int *);
void turnOffPriorityLight(const int, const int, const int);
void ONLimit(const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int);
void perform(const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, int *, int *);

/*
 * Turns on the LED at port "port"
 * @param port : The port of the LED light to turn on (from x30)
 */
void turnOn(const int port)
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
void turnOff(const int port)
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
int getValue(const int port)
{
	int result = 0;
	asm volatile(
		"addi %0, x30, 0x0\n\t"
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
void turnOnYellow(int * green, const int greenLED, const int yellowLED, int * yellow)
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
void turnOffLight(int * lightOff, const int lightOffLED, const int lightOnLED, int * lightOn)
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
void turnOffPriorityLight(const int red, const int yellow, const int green)
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
 * First turns on right light and the straight light.
 * @param sensor1Straight : Port of Straight Sensor 1
 * @param sensor1Right : Port of Straight Sensor 1
 * @param sensor2Straight : Port of Straight Sensor 2
 * @param sensor2Right : Port of Straight Sensor 2
 * @param red1Straight : Port of Straight red light 1
 * @param red2Straight : Port of Straight red light 2
 * @param red1Right : Port of Right red light 1
 * @param red2Right : Port of Right red light 2
 * @param yellow1Straight : Port of Straight yellow light 1
 * @param yellow2Straight : Port of Straight yellow light 2
 * @param yellow1Right : Port of Right yellow light 1
 * @param yellow2Right : Port of Right yellow light 2
 * @param green1Straight : Port of Straight green light 1
 * @param green2Straight : Port of Straight green light 2
 * @param green1Right : Port of Right green light 1
 * @param green2Right : Port of Right green light 2
 */
void OnLimit(const int sensor1Straight, const int sensor1Right, const int sensor2Straight, const int sensor2Right, const int red1Straight, const int red2Straight, const int red1Right, const int red2Right, const int yellow1Straight, const int yellow2Straight, const int yellow1Right, const int yellow2Right, const int green1Straight, const int green2Straight, const int green1Right, const int green2Right)
{
	const int RIGHT_TIME_LIMIT = 15;
	const int STRAIGHT_TIME_LIMIT = 45;
	
	int greenOn1 = 0;
	int greenOn2 = 0;
	
	perform(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right, RIGHT_TIME_LIMIT, 0, &greenOn1, &greenOn2);
	
	perform(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right, STRAIGHT_TIME_LIMIT, 1, &greenOn1, &greenOn2);
}

/*
 * Turns on the lights specified. 
 * @param sensor1Straight : Port of Straight Sensor 1
 * @param sensor1Right : Port of Straight Sensor 1
 * @param sensor2Straight : Port of Straight Sensor 2
 * @param sensor2Right : Port of Straight Sensor 2
 * @param red1Straight : Port of Straight red light 1
 * @param red2Straight : Port of Straight red light 2
 * @param red1Right : Port of Right red light 1
 * @param red2Right : Port of Right red light 2
 * @param yellow1Straight : Port of Straight yellow light 1
 * @param yellow2Straight : Port of Straight yellow light 2
 * @param yellow1Right : Port of Right yellow light 1
 * @param yellow2Right : Port of Right yellow light 2
 * @param green1Straight : Port of Straight green light 1
 * @param green2Straight : Port of Straight green light 2
 * @param green1Right : Port of Right green light 1
 * @param green2Right : Port of Right green light 2
 * @param Limit : The time limit
 * @param goStraight : If you want to go straight = 1; otherwise = 0
 * @param greenOn1 : If you want to go straight then greenOn would store if the green signal 1 is already on
 * @param greenOn2 : If you want to go straight then greenOn would store if the green signal 2 is already on
 */
void perform(const int sensor1Straight, const int sensor1Right, const int sensor2Straight, const int sensor2Right, const int red1Straight, const int red2Straight, const int red1Right, const int red2Right, const int yellow1Straight, const int yellow2Straight, const int yellow1Right, const int yellow2Right, const int green1Straight, const int green2Straight, const int green1Right, const int green2Right, const int LIMIT, const int goStraight, int * greenOn1, int * greenOn2)
{
	int counter = 0;
	
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
		
	if(goStraight && greenOn1)
	{
		red1 = 0;
		green1 = 1;
	}
	if(goStraight && greenOn2)
	{
		red2 = 0;
		green2 = 1;
	}

	if(goStraight == 1 && getValue(sensor1Straight))
		turnOffLight(&red1, red1Straight, green1Straight, &green1);
		
	else if(goStraight == 0 && getValue(sensor1Right))
		turnOffLight(&red1, red1Right, green1Right, &green1);
	
	if(goStraight == 1 && getValue(sensor2Straight))
		turnOffLight(&red2, red2Straight, green2Straight, &green2);
		
	else if(goStraight == 0 && getValue(sensor2Right))
		turnOffLight(&red2, red2Right, green2Right, &green2);
		
	//After this loop, only red light would be turned on if you want to go straight.
	//If you want to go right, it is possible that the going straight light would be on.
	//However, going right light would be off.
	while(!red1 || !red2)
	{
		if(green1 && goStraight == 1 && (getValue(sensor1Straight) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Straight, yellow1Straight, &yellow1);
			
		else if(green1 && goStraight == 0 && (getValue(sensor1Right) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Right, yellow1Right, &yellow1);
			
		
		if(green2 && goStraight == 1 && (getValue(sensor2Straight) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Straight, yellow2Straight, &yellow2);
		
		else if(green2 && goStraight == 0 && (getValue(sensor2Right) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Right, yellow2Right, &yellow2);

		if(yellow1 && goStraight == 1 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Straight, red1Straight, &red1);
		
		else if(yellow1 && goStraight == 0 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Right, red1Right, &red1);
		
		
		if(yellow2 && goStraight == 1 && yellowCounter2 >= 1 * 1000)
			turnOffLight(&yellow2, yellow2Straight, red2Straight, &red2);
		
		else if(yellow2 && goStraight == 0 && yellowCounter2 >= 1 * 1000)
			turnOffLight(&yellow2, yellow2Right, red2Right, &red2);
			
		//If this function performs for going right and the opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red2 && !done1 && getValue(sensor1Straight))
		{
			done1 = 1;
			turnOff(red1Straight);
			turnOn(green1Straight);
		}
			
		//If this function performs for going right and opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red1 && !done2 && getValue(sensor2Straight))
		{
			done2 = 1;
			turnOff(red2Straight);
			turnOn(green2Straight);
		}
		counter++;
		
		if(yellow1)
			yellowCounter1++;
		if(yellow2)
			yellowCounter2++;
	}
		
	* greenOn1 = done1;
	* greenOn2 = done2;
}

int main(void)
{
		//Format: Side1, Side2, Side3, Side4
		
		//These are on x30
		const int sensor1Straight = 0, sensor2Straight = 1, sensor3Straight = 2, sensor4Straight = 3;
		const int sensor1Right = 4, sensor2Right = 5, sensor3Right = 6, sensor4Right = 7;
		
		//These are on x30
		const int red1Straight = 8, red2Straight = 9, red3Straight = 10, red4Straight = 11;
		const int red1Right = 12, red2Right = 13, red3Right = 14, red4Right = 15;
		const int yellow1Straight = 16, yellow2Straight = 17, yellow3Straight = 18, yellow4Straight = 19;
		const int yellow1Right = 20,  yellow2Right = 21, yellow3Right = 22, yellow4Right = 23;
		const int green1Straight = 24, green2Straight = 25, green3Straight = 26, green4Straight = 27;
		const int green1Right = 28, green2Right = 29, green3Right = 30, green4Right = 31;
		
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
		pin_mask |= 1 << red1Straight | 1 << red1Right | 1 << red2Straight | 1 << red2Right | 1 << red3Straight | 1 << red3Right | 1 << red4Straight | 1 << red4Right;

		//Turn on all red lights
		asm volatile(
			"or x30, x30, %0\n\t" //x30 or pin_mask and store in x30 (%0 means go to first input that is given)
			:
			: "r"(pin_mask)
			: "x30"
		);

		int on = 0;
		
		while(1)
		{
			int count = getValue(sensor1Straight) + getValue(sensor2Straight) + getValue(sensor3Straight) + getValue(sensor4Straight) + getValue(sensor1Right) + getValue(sensor2Right) + getValue(sensor3Right) + getValue(sensor4Right);
			
			if(count != 0)
			{
				if(on)
				{
					turnOffPriorityLight(red1Straight, yellow1Straight, green1Straight);
					on = 0;
				}
				if(count == 4 || count == 3)
				{
					if(open == 0)
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right); 
					else
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
					
					open = (open + 2) % 4;	
					
					if(open == 0)
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right); 
					else
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
					
					open = (open + 2) % 4;
				}
				else if(count == 2 || count == 1)
				{
					if(open == 0 && getValue(sensor1Straight) || getValue(sensor1Right) || getValue(sensor2Straight) || getValue(sensor2Right))
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right);
					
					else if(getValue(sensor3Straight) || getValue(sensor3Right) || getValue(sensor4Straight) || getValue(sensor4Right))
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
						
					open = (open + 2) % 4;
					
					if(open == 0 && getValue(sensor1Straight) || getValue(sensor1Right) || getValue(sensor2Straight) || getValue(sensor2Right))
					{
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right);
						open = (open + 2) % 4;
					}
					
					else if(getValue(sensor3Straight) || getValue(sensor3Right) || getValue(sensor4Straight) || getValue(sensor4Right))
					{
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
						open = (open + 2) % 4;
					}	
				}
			}
			else
			{
				if(!on)
				{
					turnOff(red1Straight);
					turnOn(green1Straight);
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
//We used time library for testing purposes
//In the original C code, we used a counter instead

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

//We used a hardware array for ease of the testing process

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

00010054 <turnOn>:
   10054:	fd010113          	addi	sp,sp,-48
   10058:	02812623          	sw	s0,44(sp)
   1005c:	03010413          	addi	s0,sp,48
   10060:	fca42e23          	sw	a0,-36(s0)
   10064:	fdc42783          	lw	a5,-36(s0)
   10068:	00100713          	li	a4,1
   1006c:	00f717b3          	sll	a5,a4,a5
   10070:	fef42623          	sw	a5,-20(s0)
   10074:	fec42783          	lw	a5,-20(s0)
   10078:	00ff6f33          	or	t5,t5,a5
   1007c:	00000013          	nop
   10080:	02c12403          	lw	s0,44(sp)
   10084:	03010113          	addi	sp,sp,48
   10088:	00008067          	ret

0001008c <turnOff>:
   1008c:	fd010113          	addi	sp,sp,-48
   10090:	02812623          	sw	s0,44(sp)
   10094:	03010413          	addi	s0,sp,48
   10098:	fca42e23          	sw	a0,-36(s0)
   1009c:	fdc42783          	lw	a5,-36(s0)
   100a0:	00100713          	li	a4,1
   100a4:	00f717b3          	sll	a5,a4,a5
   100a8:	fff7c793          	not	a5,a5
   100ac:	fef42623          	sw	a5,-20(s0)
   100b0:	fec42783          	lw	a5,-20(s0)
   100b4:	00ff7f33          	and	t5,t5,a5
   100b8:	00000013          	nop
   100bc:	02c12403          	lw	s0,44(sp)
   100c0:	03010113          	addi	sp,sp,48
   100c4:	00008067          	ret

000100c8 <getValue>:
   100c8:	fd010113          	addi	sp,sp,-48
   100cc:	02812623          	sw	s0,44(sp)
   100d0:	03010413          	addi	s0,sp,48
   100d4:	fca42e23          	sw	a0,-36(s0)
   100d8:	fe042623          	sw	zero,-20(s0)
   100dc:	000f0793          	mv	a5,t5
   100e0:	fef42623          	sw	a5,-20(s0)
   100e4:	fdc42783          	lw	a5,-36(s0)
   100e8:	fec42703          	lw	a4,-20(s0)
   100ec:	40f757b3          	sra	a5,a4,a5
   100f0:	0017f793          	andi	a5,a5,1
   100f4:	00078513          	mv	a0,a5
   100f8:	02c12403          	lw	s0,44(sp)
   100fc:	03010113          	addi	sp,sp,48
   10100:	00008067          	ret

00010104 <turnOnYellow>:
   10104:	fe010113          	addi	sp,sp,-32
   10108:	00112e23          	sw	ra,28(sp)
   1010c:	00812c23          	sw	s0,24(sp)
   10110:	02010413          	addi	s0,sp,32
   10114:	fea42623          	sw	a0,-20(s0)
   10118:	feb42423          	sw	a1,-24(s0)
   1011c:	fec42223          	sw	a2,-28(s0)
   10120:	fed42023          	sw	a3,-32(s0)
   10124:	fec42783          	lw	a5,-20(s0)
   10128:	0007a023          	sw	zero,0(a5)
   1012c:	fe842503          	lw	a0,-24(s0)
   10130:	f5dff0ef          	jal	ra,1008c <turnOff>
   10134:	fe442503          	lw	a0,-28(s0)
   10138:	f1dff0ef          	jal	ra,10054 <turnOn>
   1013c:	fe042783          	lw	a5,-32(s0)
   10140:	00100713          	li	a4,1
   10144:	00e7a023          	sw	a4,0(a5)
   10148:	00000013          	nop
   1014c:	01c12083          	lw	ra,28(sp)
   10150:	01812403          	lw	s0,24(sp)
   10154:	02010113          	addi	sp,sp,32
   10158:	00008067          	ret

0001015c <turnOffLight>:
   1015c:	fe010113          	addi	sp,sp,-32
   10160:	00112e23          	sw	ra,28(sp)
   10164:	00812c23          	sw	s0,24(sp)
   10168:	02010413          	addi	s0,sp,32
   1016c:	fea42623          	sw	a0,-20(s0)
   10170:	feb42423          	sw	a1,-24(s0)
   10174:	fec42223          	sw	a2,-28(s0)
   10178:	fed42023          	sw	a3,-32(s0)
   1017c:	fec42783          	lw	a5,-20(s0)
   10180:	0007a023          	sw	zero,0(a5)
   10184:	fe842503          	lw	a0,-24(s0)
   10188:	f05ff0ef          	jal	ra,1008c <turnOff>
   1018c:	fe442503          	lw	a0,-28(s0)
   10190:	ec5ff0ef          	jal	ra,10054 <turnOn>
   10194:	fe042783          	lw	a5,-32(s0)
   10198:	00100713          	li	a4,1
   1019c:	00e7a023          	sw	a4,0(a5)
   101a0:	00000013          	nop
   101a4:	01c12083          	lw	ra,28(sp)
   101a8:	01812403          	lw	s0,24(sp)
   101ac:	02010113          	addi	sp,sp,32
   101b0:	00008067          	ret

000101b4 <turnOffPriorityLight>:
   101b4:	fd010113          	addi	sp,sp,-48
   101b8:	02112623          	sw	ra,44(sp)
   101bc:	02812423          	sw	s0,40(sp)
   101c0:	03010413          	addi	s0,sp,48
   101c4:	fca42e23          	sw	a0,-36(s0)
   101c8:	fcb42c23          	sw	a1,-40(s0)
   101cc:	fcc42a23          	sw	a2,-44(s0)
   101d0:	fe042623          	sw	zero,-20(s0)
   101d4:	fd442503          	lw	a0,-44(s0)
   101d8:	eb5ff0ef          	jal	ra,1008c <turnOff>
   101dc:	fd842503          	lw	a0,-40(s0)
   101e0:	e75ff0ef          	jal	ra,10054 <turnOn>
   101e4:	0100006f          	j	101f4 <turnOffPriorityLight+0x40>
   101e8:	fec42783          	lw	a5,-20(s0)
   101ec:	00178793          	addi	a5,a5,1
   101f0:	fef42623          	sw	a5,-20(s0)
   101f4:	fec42703          	lw	a4,-20(s0)
   101f8:	3e800793          	li	a5,1000
   101fc:	fef716e3          	bne	a4,a5,101e8 <turnOffPriorityLight+0x34>
   10200:	fd842503          	lw	a0,-40(s0)
   10204:	e89ff0ef          	jal	ra,1008c <turnOff>
   10208:	fdc42503          	lw	a0,-36(s0)
   1020c:	e49ff0ef          	jal	ra,10054 <turnOn>
   10210:	00000013          	nop
   10214:	02c12083          	lw	ra,44(sp)
   10218:	02812403          	lw	s0,40(sp)
   1021c:	03010113          	addi	sp,sp,48
   10220:	00008067          	ret

00010224 <OnLimit>:
   10224:	f9010113          	addi	sp,sp,-112
   10228:	06112623          	sw	ra,108(sp)
   1022c:	06812423          	sw	s0,104(sp)
   10230:	07010413          	addi	s0,sp,112
   10234:	fca42e23          	sw	a0,-36(s0)
   10238:	fcb42c23          	sw	a1,-40(s0)
   1023c:	fcc42a23          	sw	a2,-44(s0)
   10240:	fcd42823          	sw	a3,-48(s0)
   10244:	fce42623          	sw	a4,-52(s0)
   10248:	fcf42423          	sw	a5,-56(s0)
   1024c:	fd042223          	sw	a6,-60(s0)
   10250:	fd142023          	sw	a7,-64(s0)
   10254:	00f00793          	li	a5,15
   10258:	fef42623          	sw	a5,-20(s0)
   1025c:	02d00793          	li	a5,45
   10260:	fef42423          	sw	a5,-24(s0)
   10264:	fe042223          	sw	zero,-28(s0)
   10268:	fe042023          	sw	zero,-32(s0)
   1026c:	fe040793          	addi	a5,s0,-32
   10270:	02f12623          	sw	a5,44(sp)
   10274:	fe440793          	addi	a5,s0,-28
   10278:	02f12423          	sw	a5,40(sp)
   1027c:	02012223          	sw	zero,36(sp)
   10280:	fec42783          	lw	a5,-20(s0)
   10284:	02f12023          	sw	a5,32(sp)
   10288:	01c42783          	lw	a5,28(s0)
   1028c:	00f12e23          	sw	a5,28(sp)
   10290:	01842783          	lw	a5,24(s0)
   10294:	00f12c23          	sw	a5,24(sp)
   10298:	01442783          	lw	a5,20(s0)
   1029c:	00f12a23          	sw	a5,20(sp)
   102a0:	01042783          	lw	a5,16(s0)
   102a4:	00f12823          	sw	a5,16(sp)
   102a8:	00c42783          	lw	a5,12(s0)
   102ac:	00f12623          	sw	a5,12(sp)
   102b0:	00842783          	lw	a5,8(s0)
   102b4:	00f12423          	sw	a5,8(sp)
   102b8:	00442783          	lw	a5,4(s0)
   102bc:	00f12223          	sw	a5,4(sp)
   102c0:	00042783          	lw	a5,0(s0)
   102c4:	00f12023          	sw	a5,0(sp)
   102c8:	fc042883          	lw	a7,-64(s0)
   102cc:	fc442803          	lw	a6,-60(s0)
   102d0:	fc842783          	lw	a5,-56(s0)
   102d4:	fcc42703          	lw	a4,-52(s0)
   102d8:	fd042683          	lw	a3,-48(s0)
   102dc:	fd442603          	lw	a2,-44(s0)
   102e0:	fd842583          	lw	a1,-40(s0)
   102e4:	fdc42503          	lw	a0,-36(s0)
   102e8:	09c000ef          	jal	ra,10384 <perform>
   102ec:	fe040793          	addi	a5,s0,-32
   102f0:	02f12623          	sw	a5,44(sp)
   102f4:	fe440793          	addi	a5,s0,-28
   102f8:	02f12423          	sw	a5,40(sp)
   102fc:	00100793          	li	a5,1
   10300:	02f12223          	sw	a5,36(sp)
   10304:	fe842783          	lw	a5,-24(s0)
   10308:	02f12023          	sw	a5,32(sp)
   1030c:	01c42783          	lw	a5,28(s0)
   10310:	00f12e23          	sw	a5,28(sp)
   10314:	01842783          	lw	a5,24(s0)
   10318:	00f12c23          	sw	a5,24(sp)
   1031c:	01442783          	lw	a5,20(s0)
   10320:	00f12a23          	sw	a5,20(sp)
   10324:	01042783          	lw	a5,16(s0)
   10328:	00f12823          	sw	a5,16(sp)
   1032c:	00c42783          	lw	a5,12(s0)
   10330:	00f12623          	sw	a5,12(sp)
   10334:	00842783          	lw	a5,8(s0)
   10338:	00f12423          	sw	a5,8(sp)
   1033c:	00442783          	lw	a5,4(s0)
   10340:	00f12223          	sw	a5,4(sp)
   10344:	00042783          	lw	a5,0(s0)
   10348:	00f12023          	sw	a5,0(sp)
   1034c:	fc042883          	lw	a7,-64(s0)
   10350:	fc442803          	lw	a6,-60(s0)
   10354:	fc842783          	lw	a5,-56(s0)
   10358:	fcc42703          	lw	a4,-52(s0)
   1035c:	fd042683          	lw	a3,-48(s0)
   10360:	fd442603          	lw	a2,-44(s0)
   10364:	fd842583          	lw	a1,-40(s0)
   10368:	fdc42503          	lw	a0,-36(s0)
   1036c:	018000ef          	jal	ra,10384 <perform>
   10370:	00000013          	nop
   10374:	06c12083          	lw	ra,108(sp)
   10378:	06812403          	lw	s0,104(sp)
   1037c:	07010113          	addi	sp,sp,112
   10380:	00008067          	ret

00010384 <perform>:
   10384:	fa010113          	addi	sp,sp,-96
   10388:	04112e23          	sw	ra,92(sp)
   1038c:	04812c23          	sw	s0,88(sp)
   10390:	06010413          	addi	s0,sp,96
   10394:	faa42e23          	sw	a0,-68(s0)
   10398:	fab42c23          	sw	a1,-72(s0)
   1039c:	fac42a23          	sw	a2,-76(s0)
   103a0:	fad42823          	sw	a3,-80(s0)
   103a4:	fae42623          	sw	a4,-84(s0)
   103a8:	faf42423          	sw	a5,-88(s0)
   103ac:	fb042223          	sw	a6,-92(s0)
   103b0:	fb142023          	sw	a7,-96(s0)
   103b4:	fe042623          	sw	zero,-20(s0)
   103b8:	fe042423          	sw	zero,-24(s0)
   103bc:	fe042223          	sw	zero,-28(s0)
   103c0:	00100793          	li	a5,1
   103c4:	fcf42c23          	sw	a5,-40(s0)
   103c8:	00100793          	li	a5,1
   103cc:	fcf42a23          	sw	a5,-44(s0)
   103d0:	fc042823          	sw	zero,-48(s0)
   103d4:	fc042623          	sw	zero,-52(s0)
   103d8:	fc042423          	sw	zero,-56(s0)
   103dc:	fc042223          	sw	zero,-60(s0)
   103e0:	fe042023          	sw	zero,-32(s0)
   103e4:	fc042e23          	sw	zero,-36(s0)
   103e8:	02442783          	lw	a5,36(s0)
   103ec:	00078c63          	beqz	a5,10404 <perform+0x80>
   103f0:	02842783          	lw	a5,40(s0)
   103f4:	00078863          	beqz	a5,10404 <perform+0x80>
   103f8:	fc042c23          	sw	zero,-40(s0)
   103fc:	00100793          	li	a5,1
   10400:	fcf42823          	sw	a5,-48(s0)
   10404:	02442783          	lw	a5,36(s0)
   10408:	00078c63          	beqz	a5,10420 <perform+0x9c>
   1040c:	02c42783          	lw	a5,44(s0)
   10410:	00078863          	beqz	a5,10420 <perform+0x9c>
   10414:	fc042a23          	sw	zero,-44(s0)
   10418:	00100793          	li	a5,1
   1041c:	fcf42623          	sw	a5,-52(s0)
   10420:	02442703          	lw	a4,36(s0)
   10424:	00100793          	li	a5,1
   10428:	02f71a63          	bne	a4,a5,1045c <perform+0xd8>
   1042c:	fbc42503          	lw	a0,-68(s0)
   10430:	c99ff0ef          	jal	ra,100c8 <getValue>
   10434:	00050793          	mv	a5,a0
   10438:	02078263          	beqz	a5,1045c <perform+0xd8>
   1043c:	fd040713          	addi	a4,s0,-48
   10440:	fd840793          	addi	a5,s0,-40
   10444:	00070693          	mv	a3,a4
   10448:	01042603          	lw	a2,16(s0)
   1044c:	fac42583          	lw	a1,-84(s0)
   10450:	00078513          	mv	a0,a5
   10454:	d09ff0ef          	jal	ra,1015c <turnOffLight>
   10458:	0380006f          	j	10490 <perform+0x10c>
   1045c:	02442783          	lw	a5,36(s0)
   10460:	02079863          	bnez	a5,10490 <perform+0x10c>
   10464:	fb842503          	lw	a0,-72(s0)
   10468:	c61ff0ef          	jal	ra,100c8 <getValue>
   1046c:	00050793          	mv	a5,a0
   10470:	02078063          	beqz	a5,10490 <perform+0x10c>
   10474:	fd040713          	addi	a4,s0,-48
   10478:	fd840793          	addi	a5,s0,-40
   1047c:	00070693          	mv	a3,a4
   10480:	01842603          	lw	a2,24(s0)
   10484:	fa442583          	lw	a1,-92(s0)
   10488:	00078513          	mv	a0,a5
   1048c:	cd1ff0ef          	jal	ra,1015c <turnOffLight>
   10490:	02442703          	lw	a4,36(s0)
   10494:	00100793          	li	a5,1
   10498:	02f71a63          	bne	a4,a5,104cc <perform+0x148>
   1049c:	fb442503          	lw	a0,-76(s0)
   104a0:	c29ff0ef          	jal	ra,100c8 <getValue>
   104a4:	00050793          	mv	a5,a0
   104a8:	02078263          	beqz	a5,104cc <perform+0x148>
   104ac:	fcc40713          	addi	a4,s0,-52
   104b0:	fd440793          	addi	a5,s0,-44
   104b4:	00070693          	mv	a3,a4
   104b8:	01442603          	lw	a2,20(s0)
   104bc:	fa842583          	lw	a1,-88(s0)
   104c0:	00078513          	mv	a0,a5
   104c4:	c99ff0ef          	jal	ra,1015c <turnOffLight>
   104c8:	0380006f          	j	10500 <perform+0x17c>
   104cc:	02442783          	lw	a5,36(s0)
   104d0:	38079463          	bnez	a5,10858 <perform+0x4d4>
   104d4:	fb042503          	lw	a0,-80(s0)
   104d8:	bf1ff0ef          	jal	ra,100c8 <getValue>
   104dc:	00050793          	mv	a5,a0
   104e0:	36078c63          	beqz	a5,10858 <perform+0x4d4>
   104e4:	fcc40713          	addi	a4,s0,-52
   104e8:	fd440793          	addi	a5,s0,-44
   104ec:	00070693          	mv	a3,a4
   104f0:	01c42603          	lw	a2,28(s0)
   104f4:	fa042583          	lw	a1,-96(s0)
   104f8:	00078513          	mv	a0,a5
   104fc:	c61ff0ef          	jal	ra,1015c <turnOffLight>
   10500:	3580006f          	j	10858 <perform+0x4d4>
   10504:	fd042783          	lw	a5,-48(s0)
   10508:	06078663          	beqz	a5,10574 <perform+0x1f0>
   1050c:	02442703          	lw	a4,36(s0)
   10510:	00100793          	li	a5,1
   10514:	06f71063          	bne	a4,a5,10574 <perform+0x1f0>
   10518:	fbc42503          	lw	a0,-68(s0)
   1051c:	badff0ef          	jal	ra,100c8 <getValue>
   10520:	00050713          	mv	a4,a0
   10524:	00100793          	li	a5,1
   10528:	02f70663          	beq	a4,a5,10554 <perform+0x1d0>
   1052c:	02042703          	lw	a4,32(s0)
   10530:	00070793          	mv	a5,a4
   10534:	00579793          	slli	a5,a5,0x5
   10538:	40e787b3          	sub	a5,a5,a4
   1053c:	00279793          	slli	a5,a5,0x2
   10540:	00e787b3          	add	a5,a5,a4
   10544:	00379793          	slli	a5,a5,0x3
   10548:	00078713          	mv	a4,a5
   1054c:	fec42783          	lw	a5,-20(s0)
   10550:	02e7c263          	blt	a5,a4,10574 <perform+0x1f0>
   10554:	fc840713          	addi	a4,s0,-56
   10558:	fd040793          	addi	a5,s0,-48
   1055c:	00070693          	mv	a3,a4
   10560:	00042603          	lw	a2,0(s0)
   10564:	01042583          	lw	a1,16(s0)
   10568:	00078513          	mv	a0,a5
   1056c:	b99ff0ef          	jal	ra,10104 <turnOnYellow>
   10570:	06c0006f          	j	105dc <perform+0x258>
   10574:	fd042783          	lw	a5,-48(s0)
   10578:	06078263          	beqz	a5,105dc <perform+0x258>
   1057c:	02442783          	lw	a5,36(s0)
   10580:	04079e63          	bnez	a5,105dc <perform+0x258>
   10584:	fb842503          	lw	a0,-72(s0)
   10588:	b41ff0ef          	jal	ra,100c8 <getValue>
   1058c:	00050713          	mv	a4,a0
   10590:	00100793          	li	a5,1
   10594:	02f70663          	beq	a4,a5,105c0 <perform+0x23c>
   10598:	02042703          	lw	a4,32(s0)
   1059c:	00070793          	mv	a5,a4
   105a0:	00579793          	slli	a5,a5,0x5
   105a4:	40e787b3          	sub	a5,a5,a4
   105a8:	00279793          	slli	a5,a5,0x2
   105ac:	00e787b3          	add	a5,a5,a4
   105b0:	00379793          	slli	a5,a5,0x3
   105b4:	00078713          	mv	a4,a5
   105b8:	fec42783          	lw	a5,-20(s0)
   105bc:	02e7c063          	blt	a5,a4,105dc <perform+0x258>
   105c0:	fc840713          	addi	a4,s0,-56
   105c4:	fd040793          	addi	a5,s0,-48
   105c8:	00070693          	mv	a3,a4
   105cc:	00842603          	lw	a2,8(s0)
   105d0:	01842583          	lw	a1,24(s0)
   105d4:	00078513          	mv	a0,a5
   105d8:	b2dff0ef          	jal	ra,10104 <turnOnYellow>
   105dc:	fcc42783          	lw	a5,-52(s0)
   105e0:	06078663          	beqz	a5,1064c <perform+0x2c8>
   105e4:	02442703          	lw	a4,36(s0)
   105e8:	00100793          	li	a5,1
   105ec:	06f71063          	bne	a4,a5,1064c <perform+0x2c8>
   105f0:	fb442503          	lw	a0,-76(s0)
   105f4:	ad5ff0ef          	jal	ra,100c8 <getValue>
   105f8:	00050713          	mv	a4,a0
   105fc:	00100793          	li	a5,1
   10600:	02f70663          	beq	a4,a5,1062c <perform+0x2a8>
   10604:	02042703          	lw	a4,32(s0)
   10608:	00070793          	mv	a5,a4
   1060c:	00579793          	slli	a5,a5,0x5
   10610:	40e787b3          	sub	a5,a5,a4
   10614:	00279793          	slli	a5,a5,0x2
   10618:	00e787b3          	add	a5,a5,a4
   1061c:	00379793          	slli	a5,a5,0x3
   10620:	00078713          	mv	a4,a5
   10624:	fec42783          	lw	a5,-20(s0)
   10628:	02e7c263          	blt	a5,a4,1064c <perform+0x2c8>
   1062c:	fc440713          	addi	a4,s0,-60
   10630:	fcc40793          	addi	a5,s0,-52
   10634:	00070693          	mv	a3,a4
   10638:	00442603          	lw	a2,4(s0)
   1063c:	01442583          	lw	a1,20(s0)
   10640:	00078513          	mv	a0,a5
   10644:	ac1ff0ef          	jal	ra,10104 <turnOnYellow>
   10648:	06c0006f          	j	106b4 <perform+0x330>
   1064c:	fcc42783          	lw	a5,-52(s0)
   10650:	06078263          	beqz	a5,106b4 <perform+0x330>
   10654:	02442783          	lw	a5,36(s0)
   10658:	04079e63          	bnez	a5,106b4 <perform+0x330>
   1065c:	fb042503          	lw	a0,-80(s0)
   10660:	a69ff0ef          	jal	ra,100c8 <getValue>
   10664:	00050713          	mv	a4,a0
   10668:	00100793          	li	a5,1
   1066c:	02f70663          	beq	a4,a5,10698 <perform+0x314>
   10670:	02042703          	lw	a4,32(s0)
   10674:	00070793          	mv	a5,a4
   10678:	00579793          	slli	a5,a5,0x5
   1067c:	40e787b3          	sub	a5,a5,a4
   10680:	00279793          	slli	a5,a5,0x2
   10684:	00e787b3          	add	a5,a5,a4
   10688:	00379793          	slli	a5,a5,0x3
   1068c:	00078713          	mv	a4,a5
   10690:	fec42783          	lw	a5,-20(s0)
   10694:	02e7c063          	blt	a5,a4,106b4 <perform+0x330>
   10698:	fc440713          	addi	a4,s0,-60
   1069c:	fcc40793          	addi	a5,s0,-52
   106a0:	00070693          	mv	a3,a4
   106a4:	00c42603          	lw	a2,12(s0)
   106a8:	01c42583          	lw	a1,28(s0)
   106ac:	00078513          	mv	a0,a5
   106b0:	a55ff0ef          	jal	ra,10104 <turnOnYellow>
   106b4:	fc842783          	lw	a5,-56(s0)
   106b8:	02078e63          	beqz	a5,106f4 <perform+0x370>
   106bc:	02442703          	lw	a4,36(s0)
   106c0:	00100793          	li	a5,1
   106c4:	02f71863          	bne	a4,a5,106f4 <perform+0x370>
   106c8:	fe042703          	lw	a4,-32(s0)
   106cc:	3e700793          	li	a5,999
   106d0:	02e7d263          	bge	a5,a4,106f4 <perform+0x370>
   106d4:	fd840713          	addi	a4,s0,-40
   106d8:	fc840793          	addi	a5,s0,-56
   106dc:	00070693          	mv	a3,a4
   106e0:	fac42603          	lw	a2,-84(s0)
   106e4:	00042583          	lw	a1,0(s0)
   106e8:	00078513          	mv	a0,a5
   106ec:	a71ff0ef          	jal	ra,1015c <turnOffLight>
   106f0:	03c0006f          	j	1072c <perform+0x3a8>
   106f4:	fc842783          	lw	a5,-56(s0)
   106f8:	02078a63          	beqz	a5,1072c <perform+0x3a8>
   106fc:	02442783          	lw	a5,36(s0)
   10700:	02079663          	bnez	a5,1072c <perform+0x3a8>
   10704:	fe042703          	lw	a4,-32(s0)
   10708:	3e700793          	li	a5,999
   1070c:	02e7d063          	bge	a5,a4,1072c <perform+0x3a8>
   10710:	fd840713          	addi	a4,s0,-40
   10714:	fc840793          	addi	a5,s0,-56
   10718:	00070693          	mv	a3,a4
   1071c:	fa442603          	lw	a2,-92(s0)
   10720:	00842583          	lw	a1,8(s0)
   10724:	00078513          	mv	a0,a5
   10728:	a35ff0ef          	jal	ra,1015c <turnOffLight>
   1072c:	fc442783          	lw	a5,-60(s0)
   10730:	02078e63          	beqz	a5,1076c <perform+0x3e8>
   10734:	02442703          	lw	a4,36(s0)
   10738:	00100793          	li	a5,1
   1073c:	02f71863          	bne	a4,a5,1076c <perform+0x3e8>
   10740:	fdc42703          	lw	a4,-36(s0)
   10744:	3e700793          	li	a5,999
   10748:	02e7d263          	bge	a5,a4,1076c <perform+0x3e8>
   1074c:	fd440713          	addi	a4,s0,-44
   10750:	fc440793          	addi	a5,s0,-60
   10754:	00070693          	mv	a3,a4
   10758:	fa842603          	lw	a2,-88(s0)
   1075c:	00442583          	lw	a1,4(s0)
   10760:	00078513          	mv	a0,a5
   10764:	9f9ff0ef          	jal	ra,1015c <turnOffLight>
   10768:	03c0006f          	j	107a4 <perform+0x420>
   1076c:	fc442783          	lw	a5,-60(s0)
   10770:	02078a63          	beqz	a5,107a4 <perform+0x420>
   10774:	02442783          	lw	a5,36(s0)
   10778:	02079663          	bnez	a5,107a4 <perform+0x420>
   1077c:	fdc42703          	lw	a4,-36(s0)
   10780:	3e700793          	li	a5,999
   10784:	02e7d063          	bge	a5,a4,107a4 <perform+0x420>
   10788:	fd440713          	addi	a4,s0,-44
   1078c:	fc440793          	addi	a5,s0,-60
   10790:	00070693          	mv	a3,a4
   10794:	fa042603          	lw	a2,-96(s0)
   10798:	00c42583          	lw	a1,12(s0)
   1079c:	00078513          	mv	a0,a5
   107a0:	9bdff0ef          	jal	ra,1015c <turnOffLight>
   107a4:	02442783          	lw	a5,36(s0)
   107a8:	02079e63          	bnez	a5,107e4 <perform+0x460>
   107ac:	fd442783          	lw	a5,-44(s0)
   107b0:	02078a63          	beqz	a5,107e4 <perform+0x460>
   107b4:	fe842783          	lw	a5,-24(s0)
   107b8:	02079663          	bnez	a5,107e4 <perform+0x460>
   107bc:	fbc42503          	lw	a0,-68(s0)
   107c0:	909ff0ef          	jal	ra,100c8 <getValue>
   107c4:	00050793          	mv	a5,a0
   107c8:	00078e63          	beqz	a5,107e4 <perform+0x460>
   107cc:	00100793          	li	a5,1
   107d0:	fef42423          	sw	a5,-24(s0)
   107d4:	fac42503          	lw	a0,-84(s0)
   107d8:	8b5ff0ef          	jal	ra,1008c <turnOff>
   107dc:	01042503          	lw	a0,16(s0)
   107e0:	875ff0ef          	jal	ra,10054 <turnOn>
   107e4:	02442783          	lw	a5,36(s0)
   107e8:	02079e63          	bnez	a5,10824 <perform+0x4a0>
   107ec:	fd842783          	lw	a5,-40(s0)
   107f0:	02078a63          	beqz	a5,10824 <perform+0x4a0>
   107f4:	fe442783          	lw	a5,-28(s0)
   107f8:	02079663          	bnez	a5,10824 <perform+0x4a0>
   107fc:	fb442503          	lw	a0,-76(s0)
   10800:	8c9ff0ef          	jal	ra,100c8 <getValue>
   10804:	00050793          	mv	a5,a0
   10808:	00078e63          	beqz	a5,10824 <perform+0x4a0>
   1080c:	00100793          	li	a5,1
   10810:	fef42223          	sw	a5,-28(s0)
   10814:	fa842503          	lw	a0,-88(s0)
   10818:	875ff0ef          	jal	ra,1008c <turnOff>
   1081c:	01442503          	lw	a0,20(s0)
   10820:	835ff0ef          	jal	ra,10054 <turnOn>
   10824:	fec42783          	lw	a5,-20(s0)
   10828:	00178793          	addi	a5,a5,1
   1082c:	fef42623          	sw	a5,-20(s0)
   10830:	fc842783          	lw	a5,-56(s0)
   10834:	00078863          	beqz	a5,10844 <perform+0x4c0>
   10838:	fe042783          	lw	a5,-32(s0)
   1083c:	00178793          	addi	a5,a5,1
   10840:	fef42023          	sw	a5,-32(s0)
   10844:	fc442783          	lw	a5,-60(s0)
   10848:	00078863          	beqz	a5,10858 <perform+0x4d4>
   1084c:	fdc42783          	lw	a5,-36(s0)
   10850:	00178793          	addi	a5,a5,1
   10854:	fcf42e23          	sw	a5,-36(s0)
   10858:	fd842783          	lw	a5,-40(s0)
   1085c:	ca0784e3          	beqz	a5,10504 <perform+0x180>
   10860:	fd442783          	lw	a5,-44(s0)
   10864:	ca0780e3          	beqz	a5,10504 <perform+0x180>
   10868:	02842783          	lw	a5,40(s0)
   1086c:	fe842703          	lw	a4,-24(s0)
   10870:	00e7a023          	sw	a4,0(a5)
   10874:	02c42783          	lw	a5,44(s0)
   10878:	fe442703          	lw	a4,-28(s0)
   1087c:	00e7a023          	sw	a4,0(a5)
   10880:	00000013          	nop
   10884:	05c12083          	lw	ra,92(sp)
   10888:	05812403          	lw	s0,88(sp)
   1088c:	06010113          	addi	sp,sp,96
   10890:	00008067          	ret

00010894 <main>:
   10894:	f4010113          	addi	sp,sp,-192
   10898:	0a112e23          	sw	ra,188(sp)
   1089c:	0a812c23          	sw	s0,184(sp)
   108a0:	0a912a23          	sw	s1,180(sp)
   108a4:	0c010413          	addi	s0,sp,192
   108a8:	fe042223          	sw	zero,-28(s0)
   108ac:	00100793          	li	a5,1
   108b0:	fef42023          	sw	a5,-32(s0)
   108b4:	00200793          	li	a5,2
   108b8:	fcf42e23          	sw	a5,-36(s0)
   108bc:	00300793          	li	a5,3
   108c0:	fcf42c23          	sw	a5,-40(s0)
   108c4:	00400793          	li	a5,4
   108c8:	fcf42a23          	sw	a5,-44(s0)
   108cc:	00500793          	li	a5,5
   108d0:	fcf42823          	sw	a5,-48(s0)
   108d4:	00600793          	li	a5,6
   108d8:	fcf42623          	sw	a5,-52(s0)
   108dc:	00700793          	li	a5,7
   108e0:	fcf42423          	sw	a5,-56(s0)
   108e4:	00800793          	li	a5,8
   108e8:	fcf42223          	sw	a5,-60(s0)
   108ec:	00900793          	li	a5,9
   108f0:	fcf42023          	sw	a5,-64(s0)
   108f4:	00a00793          	li	a5,10
   108f8:	faf42e23          	sw	a5,-68(s0)
   108fc:	00b00793          	li	a5,11
   10900:	faf42c23          	sw	a5,-72(s0)
   10904:	00c00793          	li	a5,12
   10908:	faf42a23          	sw	a5,-76(s0)
   1090c:	00d00793          	li	a5,13
   10910:	faf42823          	sw	a5,-80(s0)
   10914:	00e00793          	li	a5,14
   10918:	faf42623          	sw	a5,-84(s0)
   1091c:	00f00793          	li	a5,15
   10920:	faf42423          	sw	a5,-88(s0)
   10924:	01000793          	li	a5,16
   10928:	faf42223          	sw	a5,-92(s0)
   1092c:	01100793          	li	a5,17
   10930:	faf42023          	sw	a5,-96(s0)
   10934:	01200793          	li	a5,18
   10938:	f8f42e23          	sw	a5,-100(s0)
   1093c:	01300793          	li	a5,19
   10940:	f8f42c23          	sw	a5,-104(s0)
   10944:	01400793          	li	a5,20
   10948:	f8f42a23          	sw	a5,-108(s0)
   1094c:	01500793          	li	a5,21
   10950:	f8f42823          	sw	a5,-112(s0)
   10954:	01600793          	li	a5,22
   10958:	f8f42623          	sw	a5,-116(s0)
   1095c:	01700793          	li	a5,23
   10960:	f8f42423          	sw	a5,-120(s0)
   10964:	01800793          	li	a5,24
   10968:	f8f42223          	sw	a5,-124(s0)
   1096c:	01900793          	li	a5,25
   10970:	f8f42023          	sw	a5,-128(s0)
   10974:	01a00793          	li	a5,26
   10978:	f6f42e23          	sw	a5,-132(s0)
   1097c:	01b00793          	li	a5,27
   10980:	f6f42c23          	sw	a5,-136(s0)
   10984:	01c00793          	li	a5,28
   10988:	f6f42a23          	sw	a5,-140(s0)
   1098c:	01d00793          	li	a5,29
   10990:	f6f42823          	sw	a5,-144(s0)
   10994:	01e00793          	li	a5,30
   10998:	f6f42623          	sw	a5,-148(s0)
   1099c:	01f00793          	li	a5,31
   109a0:	f6f42423          	sw	a5,-152(s0)
   109a4:	fe042623          	sw	zero,-20(s0)
   109a8:	000f7f13          	andi	t5,t5,0
   109ac:	f6042223          	sw	zero,-156(s0)
   109b0:	fc442783          	lw	a5,-60(s0)
   109b4:	00100713          	li	a4,1
   109b8:	00f71733          	sll	a4,a4,a5
   109bc:	fb442783          	lw	a5,-76(s0)
   109c0:	00100693          	li	a3,1
   109c4:	00f697b3          	sll	a5,a3,a5
   109c8:	00f76733          	or	a4,a4,a5
   109cc:	fc042783          	lw	a5,-64(s0)
   109d0:	00100693          	li	a3,1
   109d4:	00f697b3          	sll	a5,a3,a5
   109d8:	00f76733          	or	a4,a4,a5
   109dc:	fb042783          	lw	a5,-80(s0)
   109e0:	00100693          	li	a3,1
   109e4:	00f697b3          	sll	a5,a3,a5
   109e8:	00f76733          	or	a4,a4,a5
   109ec:	fbc42783          	lw	a5,-68(s0)
   109f0:	00100693          	li	a3,1
   109f4:	00f697b3          	sll	a5,a3,a5
   109f8:	00f76733          	or	a4,a4,a5
   109fc:	fac42783          	lw	a5,-84(s0)
   10a00:	00100693          	li	a3,1
   10a04:	00f697b3          	sll	a5,a3,a5
   10a08:	00f76733          	or	a4,a4,a5
   10a0c:	fb842783          	lw	a5,-72(s0)
   10a10:	00100693          	li	a3,1
   10a14:	00f697b3          	sll	a5,a3,a5
   10a18:	00f76733          	or	a4,a4,a5
   10a1c:	fa842783          	lw	a5,-88(s0)
   10a20:	00100693          	li	a3,1
   10a24:	00f697b3          	sll	a5,a3,a5
   10a28:	00f767b3          	or	a5,a4,a5
   10a2c:	f6442703          	lw	a4,-156(s0)
   10a30:	00f767b3          	or	a5,a4,a5
   10a34:	f6f42223          	sw	a5,-156(s0)
   10a38:	f6442783          	lw	a5,-156(s0)
   10a3c:	00ff6f33          	or	t5,t5,a5
   10a40:	fe042423          	sw	zero,-24(s0)
   10a44:	fe442503          	lw	a0,-28(s0)
   10a48:	e80ff0ef          	jal	ra,100c8 <getValue>
   10a4c:	00050493          	mv	s1,a0
   10a50:	fe042503          	lw	a0,-32(s0)
   10a54:	e74ff0ef          	jal	ra,100c8 <getValue>
   10a58:	00050793          	mv	a5,a0
   10a5c:	00f484b3          	add	s1,s1,a5
   10a60:	fdc42503          	lw	a0,-36(s0)
   10a64:	e64ff0ef          	jal	ra,100c8 <getValue>
   10a68:	00050793          	mv	a5,a0
   10a6c:	00f484b3          	add	s1,s1,a5
   10a70:	fd842503          	lw	a0,-40(s0)
   10a74:	e54ff0ef          	jal	ra,100c8 <getValue>
   10a78:	00050793          	mv	a5,a0
   10a7c:	00f484b3          	add	s1,s1,a5
   10a80:	fd442503          	lw	a0,-44(s0)
   10a84:	e44ff0ef          	jal	ra,100c8 <getValue>
   10a88:	00050793          	mv	a5,a0
   10a8c:	00f484b3          	add	s1,s1,a5
   10a90:	fd042503          	lw	a0,-48(s0)
   10a94:	e34ff0ef          	jal	ra,100c8 <getValue>
   10a98:	00050793          	mv	a5,a0
   10a9c:	00f484b3          	add	s1,s1,a5
   10aa0:	fcc42503          	lw	a0,-52(s0)
   10aa4:	e24ff0ef          	jal	ra,100c8 <getValue>
   10aa8:	00050793          	mv	a5,a0
   10aac:	00f484b3          	add	s1,s1,a5
   10ab0:	fc842503          	lw	a0,-56(s0)
   10ab4:	e14ff0ef          	jal	ra,100c8 <getValue>
   10ab8:	00050793          	mv	a5,a0
   10abc:	00f487b3          	add	a5,s1,a5
   10ac0:	f6f42023          	sw	a5,-160(s0)
   10ac4:	f6042783          	lw	a5,-160(s0)
   10ac8:	54078463          	beqz	a5,11010 <main+0x77c>
   10acc:	fe842783          	lw	a5,-24(s0)
   10ad0:	00078c63          	beqz	a5,10ae8 <main+0x254>
   10ad4:	f8442603          	lw	a2,-124(s0)
   10ad8:	fa442583          	lw	a1,-92(s0)
   10adc:	fc442503          	lw	a0,-60(s0)
   10ae0:	ed4ff0ef          	jal	ra,101b4 <turnOffPriorityLight>
   10ae4:	fe042423          	sw	zero,-24(s0)
   10ae8:	f6042703          	lw	a4,-160(s0)
   10aec:	00400793          	li	a5,4
   10af0:	00f70863          	beq	a4,a5,10b00 <main+0x26c>
   10af4:	f6042703          	lw	a4,-160(s0)
   10af8:	00300793          	li	a5,3
   10afc:	1ef71863          	bne	a4,a5,10cec <main+0x458>
   10b00:	fec42783          	lw	a5,-20(s0)
   10b04:	06079663          	bnez	a5,10b70 <main+0x2dc>
   10b08:	f7042783          	lw	a5,-144(s0)
   10b0c:	00f12e23          	sw	a5,28(sp)
   10b10:	f7442783          	lw	a5,-140(s0)
   10b14:	00f12c23          	sw	a5,24(sp)
   10b18:	f8042783          	lw	a5,-128(s0)
   10b1c:	00f12a23          	sw	a5,20(sp)
   10b20:	f8442783          	lw	a5,-124(s0)
   10b24:	00f12823          	sw	a5,16(sp)
   10b28:	f9042783          	lw	a5,-112(s0)
   10b2c:	00f12623          	sw	a5,12(sp)
   10b30:	f9442783          	lw	a5,-108(s0)
   10b34:	00f12423          	sw	a5,8(sp)
   10b38:	fa042783          	lw	a5,-96(s0)
   10b3c:	00f12223          	sw	a5,4(sp)
   10b40:	fa442783          	lw	a5,-92(s0)
   10b44:	00f12023          	sw	a5,0(sp)
   10b48:	fb042883          	lw	a7,-80(s0)
   10b4c:	fb442803          	lw	a6,-76(s0)
   10b50:	fc042783          	lw	a5,-64(s0)
   10b54:	fc442703          	lw	a4,-60(s0)
   10b58:	fd042683          	lw	a3,-48(s0)
   10b5c:	fe042603          	lw	a2,-32(s0)
   10b60:	fd442583          	lw	a1,-44(s0)
   10b64:	fe442503          	lw	a0,-28(s0)
   10b68:	ebcff0ef          	jal	ra,10224 <OnLimit>
   10b6c:	0680006f          	j	10bd4 <main+0x340>
   10b70:	f6842783          	lw	a5,-152(s0)
   10b74:	00f12e23          	sw	a5,28(sp)
   10b78:	f6c42783          	lw	a5,-148(s0)
   10b7c:	00f12c23          	sw	a5,24(sp)
   10b80:	f7842783          	lw	a5,-136(s0)
   10b84:	00f12a23          	sw	a5,20(sp)
   10b88:	f7c42783          	lw	a5,-132(s0)
   10b8c:	00f12823          	sw	a5,16(sp)
   10b90:	f8842783          	lw	a5,-120(s0)
   10b94:	00f12623          	sw	a5,12(sp)
   10b98:	f8c42783          	lw	a5,-116(s0)
   10b9c:	00f12423          	sw	a5,8(sp)
   10ba0:	f9842783          	lw	a5,-104(s0)
   10ba4:	00f12223          	sw	a5,4(sp)
   10ba8:	f9c42783          	lw	a5,-100(s0)
   10bac:	00f12023          	sw	a5,0(sp)
   10bb0:	fa842883          	lw	a7,-88(s0)
   10bb4:	fac42803          	lw	a6,-84(s0)
   10bb8:	fb842783          	lw	a5,-72(s0)
   10bbc:	fbc42703          	lw	a4,-68(s0)
   10bc0:	fc842683          	lw	a3,-56(s0)
   10bc4:	fd842603          	lw	a2,-40(s0)
   10bc8:	fcc42583          	lw	a1,-52(s0)
   10bcc:	fdc42503          	lw	a0,-36(s0)
   10bd0:	e54ff0ef          	jal	ra,10224 <OnLimit>
   10bd4:	fec42783          	lw	a5,-20(s0)
   10bd8:	00278713          	addi	a4,a5,2
   10bdc:	41f75793          	srai	a5,a4,0x1f
   10be0:	01e7d793          	srli	a5,a5,0x1e
   10be4:	00f70733          	add	a4,a4,a5
   10be8:	00377713          	andi	a4,a4,3
   10bec:	40f707b3          	sub	a5,a4,a5
   10bf0:	fef42623          	sw	a5,-20(s0)
   10bf4:	fec42783          	lw	a5,-20(s0)
   10bf8:	06079663          	bnez	a5,10c64 <main+0x3d0>
   10bfc:	f7042783          	lw	a5,-144(s0)
   10c00:	00f12e23          	sw	a5,28(sp)
   10c04:	f7442783          	lw	a5,-140(s0)
   10c08:	00f12c23          	sw	a5,24(sp)
   10c0c:	f8042783          	lw	a5,-128(s0)
   10c10:	00f12a23          	sw	a5,20(sp)
   10c14:	f8442783          	lw	a5,-124(s0)
   10c18:	00f12823          	sw	a5,16(sp)
   10c1c:	f9042783          	lw	a5,-112(s0)
   10c20:	00f12623          	sw	a5,12(sp)
   10c24:	f9442783          	lw	a5,-108(s0)
   10c28:	00f12423          	sw	a5,8(sp)
   10c2c:	fa042783          	lw	a5,-96(s0)
   10c30:	00f12223          	sw	a5,4(sp)
   10c34:	fa442783          	lw	a5,-92(s0)
   10c38:	00f12023          	sw	a5,0(sp)
   10c3c:	fb042883          	lw	a7,-80(s0)
   10c40:	fb442803          	lw	a6,-76(s0)
   10c44:	fc042783          	lw	a5,-64(s0)
   10c48:	fc442703          	lw	a4,-60(s0)
   10c4c:	fd042683          	lw	a3,-48(s0)
   10c50:	fe042603          	lw	a2,-32(s0)
   10c54:	fd442583          	lw	a1,-44(s0)
   10c58:	fe442503          	lw	a0,-28(s0)
   10c5c:	dc8ff0ef          	jal	ra,10224 <OnLimit>
   10c60:	0680006f          	j	10cc8 <main+0x434>
   10c64:	f6842783          	lw	a5,-152(s0)
   10c68:	00f12e23          	sw	a5,28(sp)
   10c6c:	f6c42783          	lw	a5,-148(s0)
   10c70:	00f12c23          	sw	a5,24(sp)
   10c74:	f7842783          	lw	a5,-136(s0)
   10c78:	00f12a23          	sw	a5,20(sp)
   10c7c:	f7c42783          	lw	a5,-132(s0)
   10c80:	00f12823          	sw	a5,16(sp)
   10c84:	f8842783          	lw	a5,-120(s0)
   10c88:	00f12623          	sw	a5,12(sp)
   10c8c:	f8c42783          	lw	a5,-116(s0)
   10c90:	00f12423          	sw	a5,8(sp)
   10c94:	f9842783          	lw	a5,-104(s0)
   10c98:	00f12223          	sw	a5,4(sp)
   10c9c:	f9c42783          	lw	a5,-100(s0)
   10ca0:	00f12023          	sw	a5,0(sp)
   10ca4:	fa842883          	lw	a7,-88(s0)
   10ca8:	fac42803          	lw	a6,-84(s0)
   10cac:	fb842783          	lw	a5,-72(s0)
   10cb0:	fbc42703          	lw	a4,-68(s0)
   10cb4:	fc842683          	lw	a3,-56(s0)
   10cb8:	fd842603          	lw	a2,-40(s0)
   10cbc:	fcc42583          	lw	a1,-52(s0)
   10cc0:	fdc42503          	lw	a0,-36(s0)
   10cc4:	d60ff0ef          	jal	ra,10224 <OnLimit>
   10cc8:	fec42783          	lw	a5,-20(s0)
   10ccc:	00278713          	addi	a4,a5,2
   10cd0:	41f75793          	srai	a5,a4,0x1f
   10cd4:	01e7d793          	srli	a5,a5,0x1e
   10cd8:	00f70733          	add	a4,a4,a5
   10cdc:	00377713          	andi	a4,a4,3
   10ce0:	40f707b3          	sub	a5,a4,a5
   10ce4:	fef42623          	sw	a5,-20(s0)
   10ce8:	3480006f          	j	11030 <main+0x79c>
   10cec:	f6042703          	lw	a4,-160(s0)
   10cf0:	00200793          	li	a5,2
   10cf4:	00f70863          	beq	a4,a5,10d04 <main+0x470>
   10cf8:	f6042703          	lw	a4,-160(s0)
   10cfc:	00100793          	li	a5,1
   10d00:	d4f712e3          	bne	a4,a5,10a44 <main+0x1b0>
   10d04:	fec42783          	lw	a5,-20(s0)
   10d08:	00079a63          	bnez	a5,10d1c <main+0x488>
   10d0c:	fe442503          	lw	a0,-28(s0)
   10d10:	bb8ff0ef          	jal	ra,100c8 <getValue>
   10d14:	00050793          	mv	a5,a0
   10d18:	02079a63          	bnez	a5,10d4c <main+0x4b8>
   10d1c:	fd442503          	lw	a0,-44(s0)
   10d20:	ba8ff0ef          	jal	ra,100c8 <getValue>
   10d24:	00050793          	mv	a5,a0
   10d28:	02079263          	bnez	a5,10d4c <main+0x4b8>
   10d2c:	fe042503          	lw	a0,-32(s0)
   10d30:	b98ff0ef          	jal	ra,100c8 <getValue>
   10d34:	00050793          	mv	a5,a0
   10d38:	00079a63          	bnez	a5,10d4c <main+0x4b8>
   10d3c:	fd042503          	lw	a0,-48(s0)
   10d40:	b88ff0ef          	jal	ra,100c8 <getValue>
   10d44:	00050793          	mv	a5,a0
   10d48:	06078663          	beqz	a5,10db4 <main+0x520>
   10d4c:	f7042783          	lw	a5,-144(s0)
   10d50:	00f12e23          	sw	a5,28(sp)
   10d54:	f7442783          	lw	a5,-140(s0)
   10d58:	00f12c23          	sw	a5,24(sp)
   10d5c:	f8042783          	lw	a5,-128(s0)
   10d60:	00f12a23          	sw	a5,20(sp)
   10d64:	f8442783          	lw	a5,-124(s0)
   10d68:	00f12823          	sw	a5,16(sp)
   10d6c:	f9042783          	lw	a5,-112(s0)
   10d70:	00f12623          	sw	a5,12(sp)
   10d74:	f9442783          	lw	a5,-108(s0)
   10d78:	00f12423          	sw	a5,8(sp)
   10d7c:	fa042783          	lw	a5,-96(s0)
   10d80:	00f12223          	sw	a5,4(sp)
   10d84:	fa442783          	lw	a5,-92(s0)
   10d88:	00f12023          	sw	a5,0(sp)
   10d8c:	fb042883          	lw	a7,-80(s0)
   10d90:	fb442803          	lw	a6,-76(s0)
   10d94:	fc042783          	lw	a5,-64(s0)
   10d98:	fc442703          	lw	a4,-60(s0)
   10d9c:	fd042683          	lw	a3,-48(s0)
   10da0:	fe042603          	lw	a2,-32(s0)
   10da4:	fd442583          	lw	a1,-44(s0)
   10da8:	fe442503          	lw	a0,-28(s0)
   10dac:	c78ff0ef          	jal	ra,10224 <OnLimit>
   10db0:	0a80006f          	j	10e58 <main+0x5c4>
   10db4:	fdc42503          	lw	a0,-36(s0)
   10db8:	b10ff0ef          	jal	ra,100c8 <getValue>
   10dbc:	00050793          	mv	a5,a0
   10dc0:	02079a63          	bnez	a5,10df4 <main+0x560>
   10dc4:	fcc42503          	lw	a0,-52(s0)
   10dc8:	b00ff0ef          	jal	ra,100c8 <getValue>
   10dcc:	00050793          	mv	a5,a0
   10dd0:	02079263          	bnez	a5,10df4 <main+0x560>
   10dd4:	fd842503          	lw	a0,-40(s0)
   10dd8:	af0ff0ef          	jal	ra,100c8 <getValue>
   10ddc:	00050793          	mv	a5,a0
   10de0:	00079a63          	bnez	a5,10df4 <main+0x560>
   10de4:	fc842503          	lw	a0,-56(s0)
   10de8:	ae0ff0ef          	jal	ra,100c8 <getValue>
   10dec:	00050793          	mv	a5,a0
   10df0:	06078463          	beqz	a5,10e58 <main+0x5c4>
   10df4:	f6842783          	lw	a5,-152(s0)
   10df8:	00f12e23          	sw	a5,28(sp)
   10dfc:	f6c42783          	lw	a5,-148(s0)
   10e00:	00f12c23          	sw	a5,24(sp)
   10e04:	f7842783          	lw	a5,-136(s0)
   10e08:	00f12a23          	sw	a5,20(sp)
   10e0c:	f7c42783          	lw	a5,-132(s0)
   10e10:	00f12823          	sw	a5,16(sp)
   10e14:	f8842783          	lw	a5,-120(s0)
   10e18:	00f12623          	sw	a5,12(sp)
   10e1c:	f8c42783          	lw	a5,-116(s0)
   10e20:	00f12423          	sw	a5,8(sp)
   10e24:	f9842783          	lw	a5,-104(s0)
   10e28:	00f12223          	sw	a5,4(sp)
   10e2c:	f9c42783          	lw	a5,-100(s0)
   10e30:	00f12023          	sw	a5,0(sp)
   10e34:	fa842883          	lw	a7,-88(s0)
   10e38:	fac42803          	lw	a6,-84(s0)
   10e3c:	fb842783          	lw	a5,-72(s0)
   10e40:	fbc42703          	lw	a4,-68(s0)
   10e44:	fc842683          	lw	a3,-56(s0)
   10e48:	fd842603          	lw	a2,-40(s0)
   10e4c:	fcc42583          	lw	a1,-52(s0)
   10e50:	fdc42503          	lw	a0,-36(s0)
   10e54:	bd0ff0ef          	jal	ra,10224 <OnLimit>
   10e58:	fec42783          	lw	a5,-20(s0)
   10e5c:	00278713          	addi	a4,a5,2
   10e60:	41f75793          	srai	a5,a4,0x1f
   10e64:	01e7d793          	srli	a5,a5,0x1e
   10e68:	00f70733          	add	a4,a4,a5
   10e6c:	00377713          	andi	a4,a4,3
   10e70:	40f707b3          	sub	a5,a4,a5
   10e74:	fef42623          	sw	a5,-20(s0)
   10e78:	fec42783          	lw	a5,-20(s0)
   10e7c:	00079a63          	bnez	a5,10e90 <main+0x5fc>
   10e80:	fe442503          	lw	a0,-28(s0)
   10e84:	a44ff0ef          	jal	ra,100c8 <getValue>
   10e88:	00050793          	mv	a5,a0
   10e8c:	02079a63          	bnez	a5,10ec0 <main+0x62c>
   10e90:	fd442503          	lw	a0,-44(s0)
   10e94:	a34ff0ef          	jal	ra,100c8 <getValue>
   10e98:	00050793          	mv	a5,a0
   10e9c:	02079263          	bnez	a5,10ec0 <main+0x62c>
   10ea0:	fe042503          	lw	a0,-32(s0)
   10ea4:	a24ff0ef          	jal	ra,100c8 <getValue>
   10ea8:	00050793          	mv	a5,a0
   10eac:	00079a63          	bnez	a5,10ec0 <main+0x62c>
   10eb0:	fd042503          	lw	a0,-48(s0)
   10eb4:	a14ff0ef          	jal	ra,100c8 <getValue>
   10eb8:	00050793          	mv	a5,a0
   10ebc:	08078663          	beqz	a5,10f48 <main+0x6b4>
   10ec0:	f7042783          	lw	a5,-144(s0)
   10ec4:	00f12e23          	sw	a5,28(sp)
   10ec8:	f7442783          	lw	a5,-140(s0)
   10ecc:	00f12c23          	sw	a5,24(sp)
   10ed0:	f8042783          	lw	a5,-128(s0)
   10ed4:	00f12a23          	sw	a5,20(sp)
   10ed8:	f8442783          	lw	a5,-124(s0)
   10edc:	00f12823          	sw	a5,16(sp)
   10ee0:	f9042783          	lw	a5,-112(s0)
   10ee4:	00f12623          	sw	a5,12(sp)
   10ee8:	f9442783          	lw	a5,-108(s0)
   10eec:	00f12423          	sw	a5,8(sp)
   10ef0:	fa042783          	lw	a5,-96(s0)
   10ef4:	00f12223          	sw	a5,4(sp)
   10ef8:	fa442783          	lw	a5,-92(s0)
   10efc:	00f12023          	sw	a5,0(sp)
   10f00:	fb042883          	lw	a7,-80(s0)
   10f04:	fb442803          	lw	a6,-76(s0)
   10f08:	fc042783          	lw	a5,-64(s0)
   10f0c:	fc442703          	lw	a4,-60(s0)
   10f10:	fd042683          	lw	a3,-48(s0)
   10f14:	fe042603          	lw	a2,-32(s0)
   10f18:	fd442583          	lw	a1,-44(s0)
   10f1c:	fe442503          	lw	a0,-28(s0)
   10f20:	b04ff0ef          	jal	ra,10224 <OnLimit>
   10f24:	fec42783          	lw	a5,-20(s0)
   10f28:	00278713          	addi	a4,a5,2
   10f2c:	41f75793          	srai	a5,a4,0x1f
   10f30:	01e7d793          	srli	a5,a5,0x1e
   10f34:	00f70733          	add	a4,a4,a5
   10f38:	00377713          	andi	a4,a4,3
   10f3c:	40f707b3          	sub	a5,a4,a5
   10f40:	fef42623          	sw	a5,-20(s0)
   10f44:	0ec0006f          	j	11030 <main+0x79c>
   10f48:	fdc42503          	lw	a0,-36(s0)
   10f4c:	97cff0ef          	jal	ra,100c8 <getValue>
   10f50:	00050793          	mv	a5,a0
   10f54:	02079a63          	bnez	a5,10f88 <main+0x6f4>
   10f58:	fcc42503          	lw	a0,-52(s0)
   10f5c:	96cff0ef          	jal	ra,100c8 <getValue>
   10f60:	00050793          	mv	a5,a0
   10f64:	02079263          	bnez	a5,10f88 <main+0x6f4>
   10f68:	fd842503          	lw	a0,-40(s0)
   10f6c:	95cff0ef          	jal	ra,100c8 <getValue>
   10f70:	00050793          	mv	a5,a0
   10f74:	00079a63          	bnez	a5,10f88 <main+0x6f4>
   10f78:	fc842503          	lw	a0,-56(s0)
   10f7c:	94cff0ef          	jal	ra,100c8 <getValue>
   10f80:	00050793          	mv	a5,a0
   10f84:	ac0780e3          	beqz	a5,10a44 <main+0x1b0>
   10f88:	f6842783          	lw	a5,-152(s0)
   10f8c:	00f12e23          	sw	a5,28(sp)
   10f90:	f6c42783          	lw	a5,-148(s0)
   10f94:	00f12c23          	sw	a5,24(sp)
   10f98:	f7842783          	lw	a5,-136(s0)
   10f9c:	00f12a23          	sw	a5,20(sp)
   10fa0:	f7c42783          	lw	a5,-132(s0)
   10fa4:	00f12823          	sw	a5,16(sp)
   10fa8:	f8842783          	lw	a5,-120(s0)
   10fac:	00f12623          	sw	a5,12(sp)
   10fb0:	f8c42783          	lw	a5,-116(s0)
   10fb4:	00f12423          	sw	a5,8(sp)
   10fb8:	f9842783          	lw	a5,-104(s0)
   10fbc:	00f12223          	sw	a5,4(sp)
   10fc0:	f9c42783          	lw	a5,-100(s0)
   10fc4:	00f12023          	sw	a5,0(sp)
   10fc8:	fa842883          	lw	a7,-88(s0)
   10fcc:	fac42803          	lw	a6,-84(s0)
   10fd0:	fb842783          	lw	a5,-72(s0)
   10fd4:	fbc42703          	lw	a4,-68(s0)
   10fd8:	fc842683          	lw	a3,-56(s0)
   10fdc:	fd842603          	lw	a2,-40(s0)
   10fe0:	fcc42583          	lw	a1,-52(s0)
   10fe4:	fdc42503          	lw	a0,-36(s0)
   10fe8:	a3cff0ef          	jal	ra,10224 <OnLimit>
   10fec:	fec42783          	lw	a5,-20(s0)
   10ff0:	00278713          	addi	a4,a5,2
   10ff4:	41f75793          	srai	a5,a4,0x1f
   10ff8:	01e7d793          	srli	a5,a5,0x1e
   10ffc:	00f70733          	add	a4,a4,a5
   11000:	00377713          	andi	a4,a4,3
   11004:	40f707b3          	sub	a5,a4,a5
   11008:	fef42623          	sw	a5,-20(s0)
   1100c:	a39ff06f          	j	10a44 <main+0x1b0>
   11010:	fe842783          	lw	a5,-24(s0)
   11014:	a20798e3          	bnez	a5,10a44 <main+0x1b0>
   11018:	fc442503          	lw	a0,-60(s0)
   1101c:	870ff0ef          	jal	ra,1008c <turnOff>
   11020:	f8442503          	lw	a0,-124(s0)
   11024:	830ff0ef          	jal	ra,10054 <turnOn>
   11028:	00100793          	li	a5,1
   1102c:	fef42423          	sw	a5,-24(s0)
   11030:	a15ff06f          	j	10a44 <main+0x1b0>
```
### NUMBER OF DIFFERENT INSTRUCTIONS: 26
```
addi
sw
lw
li
sll
or
nop
ret
not
and
mv
sra
andi
jal
j
bne
beqz
bnez
slli
sub
add
blt
bge
beq
srai
srli
```
### Spike Code
```C
#include <stdio.h>
#include <stdlib.h>

/* 
 * In this code to simulate time, we assume that one iteration of any while loop is 1ms
 * Therefore, 1s = 1000 ms = 1000 iterations.
 * If nobody is present at the signals, this code would give priority to side 1
 */

//Function prototypes
void turnOn(const int);
void turnOff(const int);
int getValue(const int);
void turnOnYellow(int *, const int, const int, int *);
void turnOffLight(int *, const int, const int, int *);
void turnOffPriorityLight(const int, const int, const int);
void ONLimit(const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int);
void perform(const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, const int, int *, int *);
void printRegister(void);
void print(int);

/*
 * Turns on the LED at port "port"
 * @param port : The port of the LED light to turn on (from x30)
 */
void turnOn(const int port)
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
void turnOff(const int port)
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
int getValue(const int port)
{
	int result = 0;
	asm volatile(
		"addi %0, x30, 0x0\n\t"
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
void turnOnYellow(int * green, const int greenLED, const int yellowLED, int * yellow)
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
void turnOffLight(int * lightOff, const int lightOffLED, const int lightOnLED, int * lightOn)
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
void turnOffPriorityLight(const int red, const int yellow, const int green)
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
 * First turns on right light and the straight light.
 * @param sensor1Straight : Port of Straight Sensor 1
 * @param sensor1Right : Port of Straight Sensor 1
 * @param sensor2Straight : Port of Straight Sensor 2
 * @param sensor2Right : Port of Straight Sensor 2
 * @param red1Straight : Port of Straight red light 1
 * @param red2Straight : Port of Straight red light 2
 * @param red1Right : Port of Right red light 1
 * @param red2Right : Port of Right red light 2
 * @param yellow1Straight : Port of Straight yellow light 1
 * @param yellow2Straight : Port of Straight yellow light 2
 * @param yellow1Right : Port of Right yellow light 1
 * @param yellow2Right : Port of Right yellow light 2
 * @param green1Straight : Port of Straight green light 1
 * @param green2Straight : Port of Straight green light 2
 * @param green1Right : Port of Right green light 1
 * @param green2Right : Port of Right green light 2
 */
void OnLimit(const int sensor1Straight, const int sensor1Right, const int sensor2Straight, const int sensor2Right, const int red1Straight, const int red2Straight, const int red1Right, const int red2Right, const int yellow1Straight, const int yellow2Straight, const int yellow1Right, const int yellow2Right, const int green1Straight, const int green2Straight, const int green1Right, const int green2Right)
{
	const int RIGHT_TIME_LIMIT = 15;
	const int STRAIGHT_TIME_LIMIT = 45;
	
	int greenOn1 = 0;
	int greenOn2 = 0;
	
	perform(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right, RIGHT_TIME_LIMIT, 0, &greenOn1, &greenOn2);
	
	perform(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right, STRAIGHT_TIME_LIMIT, 1, &greenOn1, &greenOn2);
}

/*
 * Turns on the lights specified. 
 * @param sensor1Straight : Port of Straight Sensor 1
 * @param sensor1Right : Port of Straight Sensor 1
 * @param sensor2Straight : Port of Straight Sensor 2
 * @param sensor2Right : Port of Straight Sensor 2
 * @param red1Straight : Port of Straight red light 1
 * @param red2Straight : Port of Straight red light 2
 * @param red1Right : Port of Right red light 1
 * @param red2Right : Port of Right red light 2
 * @param yellow1Straight : Port of Straight yellow light 1
 * @param yellow2Straight : Port of Straight yellow light 2
 * @param yellow1Right : Port of Right yellow light 1
 * @param yellow2Right : Port of Right yellow light 2
 * @param green1Straight : Port of Straight green light 1
 * @param green2Straight : Port of Straight green light 2
 * @param green1Right : Port of Right green light 1
 * @param green2Right : Port of Right green light 2
 * @param Limit : The time limit
 * @param goStraight : If you want to go straight = 1; otherwise = 0
 * @param greenOn1 : If you want to go straight then greenOn would store if the green signal 1 is already on
 * @param greenOn2 : If you want to go straight then greenOn would store if the green signal 2 is already on
 */
void perform(const int sensor1Straight, const int sensor1Right, const int sensor2Straight, const int sensor2Right, const int red1Straight, const int red2Straight, const int red1Right, const int red2Right, const int yellow1Straight, const int yellow2Straight, const int yellow1Right, const int yellow2Right, const int green1Straight, const int green2Straight, const int green1Right, const int green2Right, const int LIMIT, const int goStraight, int * greenOn1, int * greenOn2)
{
	int counter = 0;
	
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
		
	if(goStraight && greenOn1)
	{
		red1 = 0;
		green1 = 1;
	}
	if(goStraight && greenOn2)
	{
		red2 = 0;
		green2 = 1;
	}

	if(goStraight == 1 && getValue(sensor1Straight))
		turnOffLight(&red1, red1Straight, green1Straight, &green1);
		
	else if(goStraight == 0 && getValue(sensor1Right))
		turnOffLight(&red1, red1Right, green1Right, &green1);
	
	if(goStraight == 1 && getValue(sensor2Straight))
		turnOffLight(&red2, red2Straight, green2Straight, &green2);
		
	else if(goStraight == 0 && getValue(sensor2Right))
		turnOffLight(&red2, red2Right, green2Right, &green2);
		
	//After this loop, only red light would be turned on if you want to go straight.
	//If you want to go right, it is possible that the going straight light would be on.
	//However, going right light would be off.
	while(!red1 || !red2)
	{
		printRegister();
		if(green1 && goStraight == 1 && (getValue(sensor1Straight) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Straight, yellow1Straight, &yellow1);
			
		else if(green1 && goStraight == 0 && (getValue(sensor1Right) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Right, yellow1Right, &yellow1);
			
		
		if(green2 && goStraight == 1 && (getValue(sensor2Straight) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Straight, yellow2Straight, &yellow2);
		
		else if(green2 && goStraight == 0 && (getValue(sensor2Right) == 1 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Right, yellow2Right, &yellow2);

		if(yellow1 && goStraight == 1 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Straight, red1Straight, &red1);
		
		else if(yellow1 && goStraight == 0 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Right, red1Right, &red1);
		
		
		if(yellow2 && goStraight == 1 && yellowCounter2 >= 1 * 1000)
			turnOffLight(&yellow2, yellow2Straight, red2Straight, &red2);
		
		else if(yellow2 && goStraight == 0 && yellowCounter2 >= 1 * 1000)
			turnOffLight(&yellow2, yellow2Right, red2Right, &red2);
			
		//If this function performs for going right and the opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red2 && !done1 && getValue(sensor1Straight))
		{
			done1 = 1;
			turnOff(red1Straight);
			turnOn(green1Straight);
		}
			
		//If this function performs for going right and opposite lane already stopped going right then open up going straight for this side
		if(!goStraight && red1 && !done2 && getValue(sensor2Straight))
		{
			done2 = 1;
			turnOff(red2Straight);
			turnOn(green2Straight);
		}
		counter++;
		
		if(yellow1)
			yellowCounter1++;
		if(yellow2)
			yellowCounter2++;
	}
		
	* greenOn1 = done1;
	* greenOn2 = done2;
}

void printRegister(void)
{
	int result = 0;
	asm volatile(
		"addi %0, x30, 0x0\n\t"
		:"=r"(result)
		:
		:"x30"
	);
	
	int index = 0;
	while(result != 0)
	{
		if(result & 1 == 1)
			print(index);
		result >>= 1;
		index++;
	}
}

void print(int index)
{
	switch(index)
	{

		case 0:
			printf("Car detected for going straight at side 1.\n");
			break;
		case 1:
			printf("Car detected for going straight at side 2.\n");
			break;
		case 2:
			printf("Car detected for going straight at side 3.\n");
			break;
		case 3:
			printf("Car detected for going straight at side 4.\n");
			break;
		case 4:
			printf("Car detected for going right at side 1.\n");
			break;
		case 5:
			printf("Car detected for going right at side 2.\n");
			break;
		case 6:
			printf("Car detected for going right at side 3.\n");
			break;
		case 7:
			printf("Car detected for going right at side 4.\n");
			break;
		case 8:
			printf("Straight Red Light Side 1 is on.\n");
			break;
		case 9:
			printf("Straight Red Light Side 2 is on.\n");
			break;
		case 10:
			printf("Straight Red Light Side 3 is on.\n");
			break;
		case 11:
			printf("Straight Red Light Side 4 is on.\n");
			break;
		case 12:
			printf("Right Red Light Side 1 is on.\n");
			break;
		case 13:
			printf("Right Red Light Side 2 is on.\n");
			break;
		case 14:
			printf("Right Red Light Side 3 is on.\n");
			break;
		case 15:
			printf("Right Red Light Side 4 is on.\n");
			break;
		case 16:
			printf("Straight Yellow Light Side 1 is on.\n");
			break;
		case 17:
			printf("Straight Yellow Light Side 2 is on.\n");
			break;
		case 18:
			printf("Straight Yellow Light Side 3 is on.\n");
			break;
		case 19:
			printf("Straight Yellow Light Side 4 is on.\n");
			break;
		case 20:
			printf("Right Yellow Light Side 1 is on.\n");
			break;
		case 21:
			printf("Right Yellow Light Side 2 is on.\n");
			break;
		case 22:
			printf("Right Yellow Light Side 3 is on.\n");
			break;
		case 23:
			printf("Right Yellow Light Side 4 is on.\n");
			break;
		case 24:
			printf("Straight Green Light Side 1 is on.\n");
			break;
		case 25:
			printf("Straight Green Light Side 2 is on.\n");
			break;
		case 26:
			printf("Straight Green Light Side 3 is on.\n");
			break;
		case 27:
			printf("Straight Green Light Side 4 is on.\n");
			break;
		case 28:
			printf("Right Green Light Side 1 is on.\n");
			break;
		case 29:
			printf("Right Green Light Side 2 is on.\n");
			break;
		case 30:
			printf("Right Green Light Side 3 is on.\n");
			break;
		case 31:
			printf("Right Yellow Light Side 4 is on.\n");
			break;
	}
}

int main(void)
{
		//Format: Side1, Side2, Side3, Side4
		
		//These are on x30
		const int sensor1Straight = 0, sensor2Straight = 1, sensor3Straight = 2, sensor4Straight = 3;
		const int sensor1Right = 4, sensor2Right = 5, sensor3Right = 6, sensor4Right = 7;
		//These are on x30
		const int red1Straight = 8, red2Straight = 9, red3Straight = 10, red4Straight = 11;
		const int red1Right = 12, red2Right = 13, red3Right = 14, red4Right = 15;
		const int yellow1Straight = 16, yellow2Straight = 17, yellow3Straight = 18, yellow4Straight = 19;
		const int yellow1Right = 20,  yellow2Right = 21, yellow3Right = 22, yellow4Right = 23;
		const int green1Straight = 24, green2Straight = 25, green3Straight = 26, green4Straight = 27;
		const int green1Right = 28, green2Right = 29, green3Right = 30, green4Right = 31;
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
		pin_mask |= 1 << red1Straight | 1 << red1Right | 1 << red2Straight | 1 << red2Right | 1 << red3Straight | 1 << red3Right | 1 << red4Straight | 1 << red4Right;

		//Turn on all red lights
		asm volatile(
			"or x30, x30, %0\n\t" //x30 or pin_mask and store in x30 (%0 means go to first input that is given)
			:
			: "r"(pin_mask)
			: "x30"
		);

		int on = 0;
		
		int testCase = 1;
		
		//Random test cases
		switch(testCase)
		{
			case 0:
				//No light on 
				break;
			case 1:
				//lane1 right on and lane4 straight and right on
				pin_mask = 0;
				pin_mask |= 1 << sensor1Right | 1 << sensor4Straight | 1 << sensor4Right | 1 << sensor1Straight;
				asm volatile(
					"or x30, x30, %0\n\t"
					:
					: "r"(pin_mask)
					: "x30"	
				);
				break;
		}

		int iterations = 0;
		while(iterations != 200)
		{
			int count = getValue(sensor1Straight) + getValue(sensor2Straight) + getValue(sensor3Straight) + getValue(sensor4Straight) + getValue(sensor1Right) + getValue(sensor2Right) + getValue(sensor3Right) + getValue(sensor4Right);
			
			if(count != 0)
			{
				if(on)
				{
					turnOffPriorityLight(red1Straight, yellow1Straight, green1Straight);
					on = 0;
				}
				if(count == 4 || count == 3)
				{
					if(open == 0)
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right); 
					else
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
					
					open = (open + 2) % 4;	
					
					if(open == 0)
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right); 
					else
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
					
					open = (open + 2) % 4;
				}
				else if(count == 2 || count == 1)
				{
					if(open == 0 && getValue(sensor1Straight) || getValue(sensor1Right) || getValue(sensor2Straight) || getValue(sensor2Right))
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right);
					
					else if(getValue(sensor3Straight) || getValue(sensor3Right) || getValue(sensor4Straight) || getValue(sensor4Right))
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
						
					open = (open + 2) % 4;
					
					if(open == 0 && getValue(sensor1Straight) || getValue(sensor1Right) || getValue(sensor2Straight) || getValue(sensor2Right))
					{
						OnLimit(sensor1Straight, sensor1Right, sensor2Straight, sensor2Right, red1Straight, red2Straight, red1Right, red2Right, yellow1Straight, yellow2Straight, yellow1Right, yellow2Right, green1Straight, green2Straight, green1Right, green2Right);
						open = (open + 2) % 4;
					}
					
					else if(getValue(sensor3Straight) || getValue(sensor3Right) || getValue(sensor4Straight) || getValue(sensor4Right))
					{
						OnLimit(sensor3Straight, sensor3Right, sensor4Straight, sensor4Right, red3Straight, red4Straight, red3Right, red4Right, yellow3Straight, yellow4Straight, yellow3Right, yellow4Right, green3Straight, green4Straight, green3Right, green4Right);
						open = (open + 2) % 4;
					}	
				}
			}
			else
			{
				if(!on)
				{
					turnOff(red1Straight);
					turnOn(green1Straight);
					on = 1;
				}
			}
			printRegister();
			iterations++;
		}
    return 0;
}
```
### Spike Simulations
Test Case 1 : No traffic on any lanes.

Expected Output 1: Only green light of priority lane (default side 1) would be turned on. 

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/145079379/c6ef9c6e-39e9-4a0e-b2aa-30735940e491)

Test Case 2 : Cars wanting to go straight and to the right in lane 1, 4

Expected Output 2: Green lights for those lanes at different times.

![image](https://github.com/AryanAAB/Automatic-Traffic-Light/assets/145079379/e862c867-24f1-4662-962a-38e3e2577193)

### Testcases 
|lane1   |lane1_right   |lane2   |lane2_right   |lane3   |lane3_right   |lane4   |lane4_right|
|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|:--------------:|
|0	|0	|0	|0	|0	|0	|0	|0
|0	|0	|0	|0	|0	|0	|0	|1
|0	|0	|0	|0	|0	|0	|1	|0
|0	|0	|0	|0	|0	|0	|1	|1
|0	|0	|0	|0	|0	|1	|0	|0
|0	|0	|0	|0	|0	|1	|0	|1
|0	|0	|0	|0	|0	|1	|1	|0
|0	|0	|0	|0	|0	|1	|1	|1
|0	|0	|0	|0	|1	|0	|0	|0
|0	|0	|0	|0	|1	|0	|0	|1
|0	|0	|0	|0	|1	|0	|1	|0
|0	|0	|0	|0	|1	|0	|1	|1
|0	|0	|0	|0	|1	|1	|0	|0
|0	|0	|0	|0	|1	|1	|0	|1
|0	|0	|0	|0	|1	|1	|1	|0
|0	|0	|0	|0	|1	|1	|1	|1
|0	|0	|0	|1	|0	|0	|0	|0
|0	|0	|0	|1	|0	|0	|0	|1
|0	|0	|0	|1	|0	|0	|1	|0
|0	|0	|0	|1	|0	|0	|1	|1
|0	|0	|0	|1	|0	|1	|0	|0
|0	|0	|0	|1	|0	|1	|0	|1
|0	|0	|0	|1	|0	|1	|1	|0
|0	|0	|0	|1	|0	|1	|1	|1
|0	|0	|0	|1	|1	|0	|0	|0
|0	|0	|0	|1	|1	|0	|0	|1
|0	|0	|0	|1	|1	|0	|1	|0
|0	|0	|0	|1	|1	|0	|1	|1
|0	|0	|0	|1	|1	|1	|0	|0
|0	|0	|0	|1	|1	|1	|0	|1
|0	|0	|0	|1	|1	|1	|1	|0
|0	|0	|0	|1	|1	|1	|1	|1
|0	|0	|1	|0	|0	|0	|0	|0
|0	|0	|1	|0	|0	|0	|0	|1
|0	|0	|1	|0	|0	|0	|1	|0
|0	|0	|1	|0	|0	|0	|1	|1
|0	|0	|1	|0	|0	|1	|0	|0
|0	|0	|1	|0	|0	|1	|0	|1
|0	|0	|1	|0	|0	|1	|1	|0
|0	|0	|1	|0	|0	|1	|1	|1
|0	|0	|1	|0	|1	|0	|0	|0
|0	|0	|1	|0	|1	|0	|0	|1
|0	|0	|1	|0	|1	|0	|1	|0
|0	|0	|1	|0	|1	|0	|1	|1
|0	|0	|1	|0	|1	|1	|0	|0
|0	|0	|1	|0	|1	|1	|0	|1
|0	|0	|1	|0	|1	|1	|1	|0
|0	|0	|1	|0	|1	|1	|1	|1
|0	|0	|1	|1	|0	|0	|0	|0
|0	|0	|1	|1	|0	|0	|0	|1
|0	|0	|1	|1	|0	|0	|1	|0
|0	|0	|1	|1	|0	|0	|1	|1
|0	|0	|1	|1	|0	|1	|0	|0
|0	|0	|1	|1	|0	|1	|0	|1
|0	|0	|1	|1	|0	|1	|1	|0
|0	|0	|1	|1	|0	|1	|1	|1
|0	|0	|1	|1	|1	|0	|0	|0
|0	|0	|1	|1	|1	|0	|0	|1
|0	|0	|1	|1	|1	|0	|1	|0
|0	|0	|1	|1	|1	|0	|1	|1
|0	|0	|1	|1	|1	|1	|0	|0
|0	|0	|1	|1	|1	|1	|0	|1
|0	|0	|1	|1	|1	|1	|1	|0
|0	|0	|1	|1	|1	|1	|1	|1
|0	|1	|0	|0	|0	|0	|0	|0
|0	|1	|0	|0	|0	|0	|0	|1
|0	|1	|0	|0	|0	|0	|1	|0
|0	|1	|0	|0	|0	|0	|1	|1
|0	|1	|0	|0	|0	|1	|0	|0
|0	|1	|0	|0	|0	|1	|0	|1
|0	|1	|0	|0	|0	|1	|1	|0
|0	|1	|0	|0	|0	|1	|1	|1
|0	|1	|0	|0	|1	|0	|0	|0
|0	|1	|0	|0	|1	|0	|0	|1
|0	|1	|0	|0	|1	|0	|1	|0
|0	|1	|0	|0	|1	|0	|1	|1
|0	|1	|0	|0	|1	|1	|0	|0
|0	|1	|0	|0	|1	|1	|0	|1
|0	|1	|0	|0	|1	|1	|1	|0
|0	|1	|0	|0	|1	|1	|1	|1
|0	|1	|0	|1	|0	|0	|0	|0
|0	|1	|0	|1	|0	|0	|0	|1
|0	|1	|0	|1	|0	|0	|1	|0
|0	|1	|0	|1	|0	|0	|1	|1
|0	|1	|0	|1	|0	|1	|0	|0
|0	|1	|0	|1	|0	|1	|0	|1
|0	|1	|0	|1	|0	|1	|1	|0
|0	|1	|0	|1	|0	|1	|1	|1
|0	|1	|0	|1	|1	|0	|0	|0
|0	|1	|0	|1	|1	|0	|0	|1
|0	|1	|0	|1	|1	|0	|1	|0
|0	|1	|0	|1	|1	|0	|1	|1
|0	|1	|0	|1	|1	|1	|0	|0
|0	|1	|0	|1	|1	|1	|0	|1
|0	|1	|0	|1	|1	|1	|1	|0
|0	|1	|0	|1	|1	|1	|1	|1
|0	|1	|1	|0	|0	|0	|0	|0
|0	|1	|1	|0	|0	|0	|0	|1
|0	|1	|1	|0	|0	|0	|1	|0
|0	|1	|1	|0	|0	|0	|1	|1
|0	|1	|1	|0	|0	|1	|0	|0
|0	|1	|1	|0	|0	|1	|0	|1
|0	|1	|1	|0	|0	|1	|1	|0
|0	|1	|1	|0	|0	|1	|1	|1
|0	|1	|1	|0	|1	|0	|0	|0
|0	|1	|1	|0	|1	|0	|0	|1
|0	|1	|1	|0	|1	|0	|1	|0
|0	|1	|1	|0	|1	|0	|1	|1
|0	|1	|1	|0	|1	|1	|0	|0
|0	|1	|1	|0	|1	|1	|0	|1
|0	|1	|1	|0	|1	|1	|1	|0
|0	|1	|1	|0	|1	|1	|1	|1
|0	|1	|1	|1	|0	|0	|0	|0
|0	|1	|1	|1	|0	|0	|0	|1
|0	|1	|1	|1	|0	|0	|1	|0
|0	|1	|1	|1	|0	|0	|1	|1
|0	|1	|1	|1	|0	|1	|0	|0
|0	|1	|1	|1	|0	|1	|0	|1
|0	|1	|1	|1	|0	|1	|1	|0
|0	|1	|1	|1	|0	|1	|1	|1
|0	|1	|1	|1	|1	|0	|0	|0
|0	|1	|1	|1	|1	|0	|0	|1
|0	|1	|1	|1	|1	|0	|1	|0
|0	|1	|1	|1	|1	|0	|1	|1
|0	|1	|1	|1	|1	|1	|0	|0
|0	|1	|1	|1	|1	|1	|0	|1
|0	|1	|1	|1	|1	|1	|1	|0
|0	|1	|1	|1	|1	|1	|1	|1
|1	|0	|0	|0	|0	|0	|0	|0
|1	|0	|0	|0	|0	|0	|0	|1
|1	|0	|0	|0	|0	|0	|1	|0
|1	|0	|0	|0	|0	|0	|1	|1
|1	|0	|0	|0	|0	|1	|0	|0
|1	|0	|0	|0	|0	|1	|0	|1
|1	|0	|0	|0	|0	|1	|1	|0
|1	|0	|0	|0	|0	|1	|1	|1
|1	|0	|0	|0	|1	|0	|0	|0
|1	|0	|0	|0	|1	|0	|0	|1
|1	|0	|0	|0	|1	|0	|1	|0
|1	|0	|0	|0	|1	|0	|1	|1
|1	|0	|0	|0	|1	|1	|0	|0
|1	|0	|0	|0	|1	|1	|0	|1
|1	|0	|0	|0	|1	|1	|1	|0
|1	|0	|0	|0	|1	|1	|1	|1
|1	|0	|0	|1	|0	|0	|0	|0
|1	|0	|0	|1	|0	|0	|0	|1
|1	|0	|0	|1	|0	|0	|1	|0
|1	|0	|0	|1	|0	|0	|1	|1
|1	|0	|0	|1	|0	|1	|0	|0
|1	|0	|0	|1	|0	|1	|0	|1
|1	|0	|0	|1	|0	|1	|1	|0
|1	|0	|0	|1	|0	|1	|1	|1
|1	|0	|0	|1	|1	|0	|0	|0
|1	|0	|0	|1	|1	|0	|0	|1
|1	|0	|0	|1	|1	|0	|1	|0
|1	|0	|0	|1	|1	|0	|1	|1
|1	|0	|0	|1	|1	|1	|0	|0
|1	|0	|0	|1	|1	|1	|0	|1
|1	|0	|0	|1	|1	|1	|1	|0
|1	|0	|0	|1	|1	|1	|1	|1
|1	|0	|1	|0	|0	|0	|0	|0
|1	|0	|1	|0	|0	|0	|0	|1
|1	|0	|1	|0	|0	|0	|1	|0
|1	|0	|1	|0	|0	|0	|1	|1
|1	|0	|1	|0	|0	|1	|0	|0
|1	|0	|1	|0	|0	|1	|0	|1
|1	|0	|1	|0	|0	|1	|1	|0
|1	|0	|1	|0	|0	|1	|1	|1
|1	|0	|1	|0	|1	|0	|0	|0
|1	|0	|1	|0	|1	|0	|0	|1
|1	|0	|1	|0	|1	|0	|1	|0
|1	|0	|1	|0	|1	|0	|1	|1
|1	|0	|1	|0	|1	|1	|0	|0
|1	|0	|1	|0	|1	|1	|0	|1
|1	|0	|1	|0	|1	|1	|1	|0
|1	|0	|1	|0	|1	|1	|1	|1
|1	|0	|1	|1	|0	|0	|0	|0
|1	|0	|1	|1	|0	|0	|0	|1
|1	|0	|1	|1	|0	|0	|1	|0
|1	|0	|1	|1	|0	|0	|1	|1
|1	|0	|1	|1	|0	|1	|0	|0
|1	|0	|1	|1	|0	|1	|0	|1
|1	|0	|1	|1	|0	|1	|1	|0
|1	|0	|1	|1	|0	|1	|1	|1
|1	|0	|1	|1	|1	|0	|0	|0
|1	|0	|1	|1	|1	|0	|0	|1
|1	|0	|1	|1	|1	|0	|1	|0
|1	|0	|1	|1	|1	|0	|1	|1
|1	|0	|1	|1	|1	|1	|0	|0
|1	|0	|1	|1	|1	|1	|0	|1
|1	|0	|1	|1	|1	|1	|1	|0
|1	|0	|1	|1	|1	|1	|1	|1
|1	|1	|0	|0	|0	|0	|0	|0
|1	|1	|0	|0	|0	|0	|0	|1
|1	|1	|0	|0	|0	|0	|1	|0
|1	|1	|0	|0	|0	|0	|1	|1
|1	|1	|0	|0	|0	|1	|0	|0
|1	|1	|0	|0	|0	|1	|0	|1
|1	|1	|0	|0	|0	|1	|1	|0
|1	|1	|0	|0	|0	|1	|1	|1
|1	|1	|0	|0	|1	|0	|0	|0
|1	|1	|0	|0	|1	|0	|0	|1
|1	|1	|0	|0	|1	|0	|1	|0
|1	|1	|0	|0	|1	|0	|1	|1
|1	|1	|0	|0	|1	|1	|0	|0
|1	|1	|0	|0	|1	|1	|0	|1
|1	|1	|0	|0	|1	|1	|1	|0
|1	|1	|0	|0	|1	|1	|1	|1
|1	|1	|0	|1	|0	|0	|0	|0
|1	|1	|0	|1	|0	|0	|0	|1
|1	|1	|0	|1	|0	|0	|1	|0
|1	|1	|0	|1	|0	|0	|1	|1
|1	|1	|0	|1	|0	|1	|0	|0
|1	|1	|0	|1	|0	|1	|0	|1
|1	|1	|0	|1	|0	|1	|1	|0
|1	|1	|0	|1	|0	|1	|1	|1
|1	|1	|0	|1	|1	|0	|0	|0
|1	|1	|0	|1	|1	|0	|0	|1
|1	|1	|0	|1	|1	|0	|1	|0
|1	|1	|0	|1	|1	|0	|1	|1
|1	|1	|0	|1	|1	|1	|0	|0
|1	|1	|0	|1	|1	|1	|0	|1
|1	|1	|0	|1	|1	|1	|1	|0
|1	|1	|0	|1	|1	|1	|1	|1
|1	|1	|1	|0	|0	|0	|0	|0
|1	|1	|1	|0	|0	|0	|0	|1
|1	|1	|1	|0	|0	|0	|1	|0
|1	|1	|1	|0	|0	|0	|1	|1
|1	|1	|1	|0	|0	|1	|0	|0
|1	|1	|1	|0	|0	|1	|0	|1
|1	|1	|1	|0	|0	|1	|1	|0
|1	|1	|1	|0	|0	|1	|1	|1
|1	|1	|1	|0	|1	|0	|0	|0
|1	|1	|1	|0	|1	|0	|0	|1
|1	|1	|1	|0	|1	|0	|1	|0
|1	|1	|1	|0	|1	|0	|1	|1
|1	|1	|1	|0	|1	|1	|0	|0
|1	|1	|1	|0	|1	|1	|0	|1
|1	|1	|1	|0	|1	|1	|1	|0
|1	|1	|1	|0	|1	|1	|1	|1
|1	|1	|1	|1	|0	|0	|0	|0
|1	|1	|1	|1	|0	|0	|0	|1
|1	|1	|1	|1	|0	|0	|1	|0
|1	|1	|1	|1	|0	|0	|1	|1
|1	|1	|1	|1	|0	|1	|0	|0
|1	|1	|1	|1	|0	|1	|0	|1
|1	|1	|1	|1	|0	|1	|1	|0
|1	|1	|1	|1	|0	|1	|1	|1
|1	|1	|1	|1	|1	|0	|0	|0
|1	|1	|1	|1	|1	|0	|0	|1
|1	|1	|1	|1	|1	|0	|1	|0
|1	|1	|1	|1	|1	|0	|1	|1
|1	|1	|1	|1	|1	|1	|0	|0
|1	|1	|1	|1	|1	|1	|0	|1
|1	|1	|1	|1	|1	|1	|1	|0
|1	|1	|1	|1	|1	|1	|1	|1



### Citations

1) _Infrared (IR) Sensor Module with Arduino_. Solarduino. 12 Jan. 2020. [encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU](encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSKL49Fuzyarn4NJ6680l6UARhih-H7ZjiCjVlIlieX474dQUyhHMPB3w-tkls-Jas0f68&;usqp=CAU). Accessed 30 Oct. 2023.
2) _IR Sensor Working_. Robocraze. [robocraze.com/blogs/post/ir-sensor-working](robocraze.com/blogs/post/ir-sensor-working). Accessed 30 Oct. 2023.
3) KanisshR1. "RISC-V-Automatic-Sanitizer-Dispenser." _RISC-Automatic-Sanitizer-Dispenser_. Github. 31 Oct. 2023. [https://github.com/KanishR1/RISCV_Automatic-Sanitizer-Dispenser]
   (https://github.com/KanishR1/RISCV_Automatic-Sanitizer-Dispenser). Accessed 10 Nov. 2023.
4) Iswaryallanchezhiyan. "RISC-V-Digital-Alarm-Clock." _RISC-V-Digital-Alarm-Clock_. Github. 1 Nov. 2023. [https://github.com/IswaryaIlanchezhiyan/RISC-V-Digital-Alarm-Clock](https://github.com/IswaryaIlanchezhiyan/RISC-V-Digital-Alarm-Clock). Accessed 10 Nov. 2023.
5 Nancy0192. "RISC-V-Blind-Sight-Aid." _RISC-V-Blind-Sight-Aid_. Github. 2 Nov. 2023. [https://github.com/Nancy0192/BlindSight_Aid](https://github.com/Nancy0192/BlindSight_Aid). Accessed 10 Nov. 2023.
6) Shivangi2207. "RISC-V-Fire-Detector." _RISC-V-Fire-Detector_. Github. 2 Nov. 2023. [https://github.com/Shivangi2207/Fire_detector_RISCV.git](https://github.com/Shivangi2207/Fire_detector_RISCV.git). Accessed 10 Nov. 2023.
7) ShubhamGitHub528. “Automatic Garage Door System.” _Home Automation System_. Github. 28 Oct. 2023. [github.com/ShubhamGitHub528/Home-Automation-System](github.com/ShubhamGitHub528/Home-Automation-System). Accessed 30 Oct. 2023.
8) Y09mogal. "RISC-V-Heart-Rate-Monitor." _RISC-V-Heart-Rate-Monitor_. Github. 12 Oct. 2023. [github.com/ShubhamGitHub528/Home-Automation-System](https://github.com/Y09mogal/RISCV_Heart_Rate_Monitor). Accessed 10 Nov. 2023.
