#include <stdio.h>

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
		if(green1 && goStraight == 1 && (getValue(sensor1Straight) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Straight, yellow1Straight, &yellow1);
			
		else if(green1 && goStraight == 0 && (getValue(sensor1Right) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green1, green1Right, yellow1Right, &yellow1);
			
		
		if(green2 && goStraight == 1 && (getValue(sensor2Straight) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Straight, yellow2Straight, &yellow2);
		
		else if(green2 && goStraight == 0 && (getValue(sensor2Right) == 0 || counter >= LIMIT * 1000))
			turnOnYellow(&green2, green2Right, yellow2Right, &yellow2);

		if(yellow1 && goStraight == 1 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Straight, red1Straight, &red1);
		
		else if(yellow1 && goStraight == 0 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Right, red1Right, &red1);
		
		
		if(yellow1 && goStraight == 1 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Straight, red1Straight, &red1);
		
		else if(yellow1 && goStraight == 0 && yellowCounter1 >= 1 * 1000)
			turnOffLight(&yellow1, yellow1Right, red1Right, &red1);
			
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
			printf("%d is on", &index);
		result >>= 1; 
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
		
		int testCase = 0;
		scanf("%d", &testCase);
		
		switch(testCase)
		{
			case 0:
				//No light on 
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
