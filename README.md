# plus1
Interactive art to connect people

## HOW THE ARDUINO DRIVER WORKS
So you send a command to the Arduino via serial Bluetooth (COM#) and make sure it reads every 50 milliseconds. The command is  in the following SYNTAX. This is with 1-6 being the strips, 7 being the entire display, 8 being the right half and 9 being the left half.

# Configuration
STRIP - CUBE NUMBER IN STRIP - COLOR TO SET/Brightness
1	A-J	r/g/b/w/p	0-9
2	A-J	r/g/b/w/p	0-9
3	A-J	r/g/b/w/p	0-9
4	A-J	r/g/b/w/p	0-9
5	A-J	r/g/b/w/p	0-9
6	A-J	r/g/b/w/p	0-9
7	NA	r/g/b/w/p	0-9
8	NA	r/g/b/w/p	0-9
9	NA	r/g/b/w/p	0-9
0	NA	NA			NA
1-6 X   r/g/b/w/p  	0-9
# Example commands:
1Ag5 = would set the "A" Led in strip 1 to Green. Brightness at 50%
5Jw2 = would set the "J" Led in strip 5 to White. Brightness at 20%
7Ar3= woulld set the entire display to red. Brightness at 30%
7Jp9 = would set the entire display to purple. Brightness at 90%
7Bb10 = would set the entire display to blue. Brightness at 10%
8Ar8 = would set the right side of the display (1-3) to red. Brightness at 80%
8Fg3 = would set the right side of the display(1-3) to green. Brightness at 30%
9Fg4 = would set the left side of the display (4-6) to green. Brightness at 40%
9Ab3 = would set the right side of the display (4-6) to blue. Brightness at 30%
0Cr6 = sets the entire display off
0Fb4 = turns the entire display off
0Zz3 = turns the entire display off
1Xr3 = turns the entire 1st strip to red. Brightness at 30%
5Xg8 = turns the entire 5th strip to green. Brightness at 80%
3Xw5 = turns the entire 3rd strip to white. Brightness at 50%