//This code is not a assembly structure
//This code can be run to check whether the code is required
//outputs according to the given inputs.

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

//This function will print the Side/Lane number along with the direction i.e. Straight or Right if the LED for those Sideis on.
void print(){
    for(int i = 8, j = 1; i <= 11; i++, j++){
	    if(hardware[i]){
		    printf("Red light straight at side %d is on\n", j);
		}
    }
    for(int i = 12, j = 1; i <= 15; i++, j++){
	    if(hardware[i]){
		    printf("%d Red light right at side %d\n", hardware[i], j);
	    }
    }
    for(int i = 16, j = 1; i <= 19; i++, j++){
	    if(hardware[i]){
		    printf("%d Yellow light straight at side %d\n", hardware[i], j);
	    }
    }
    for(int i = 20, j = 1; i <= 23; i++, j++){
	    if(hardware[i]){
		    printf("%d Yellow light right at side %d\n", hardware[i], j);
	    }
    }
    for(int i = 24, j = 1; i <= 27; i++, j++){
	    if(hardware[i]){
		    printf("%d Green light straight at side %d\n", hardware[i], j);
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
