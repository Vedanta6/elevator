# elevator

The program simulates the elevator

Input parameters:

		- the number of stories in the building (from 5 to 20)
		- the height of one story
		- the elevator rate (meters per sec)
		- the time delay between opening and closing the doors
		
As an example, you can run a program:
		
		> python elevator.py 5 2.5 1.6 10
		
You will see the hint:

	Enter "i<story>" to press the button with the number of a story inside the elevator or "o<story>" to press the button on a story
	
For example:
To press the button "3" inside the elevator you need to type a command: 
	
	i3		
	
To call the elevator on the 5th story: 
	
	o5
	
You will see the messages each time the elevator: 

	- change a story 
	- open the doors 
	- close the doors
