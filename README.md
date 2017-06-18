# plus1
Interactive art to connect people. The way the display works is by using OpenCV to recognize people as they walk by the display. After recognizing two different indivdiuals crossing paths the entire display lights up and simulates a heart beating. This is to catch peoples attention and promote conversation between them!
</br>
![alt text](https://github.com/syk435/plus1/blob/master/images/20170617_211141.jpg)

## HOW THE ARDUINO DRIVER WORKS
So you send a command to the Arduino via serial Bluetooth (COM#) and make sure it reads every 50 milliseconds. The command is  in the following SYNTAX. This is with 1-6 being the strips, 7 being the entire display, 8 being the right half and 9 being the left half.

# Configuration
STRIP - CUBE NUMBER IN STRIP - COLOR TO SET/Brightness </br>
1	A-J	r/g/b/w/p	0-9 </br>
2	A-J	r/g/b/w/p	0-9 </br> 
3	A-J	r/g/b/w/p	0-9 </br>
4	A-J	r/g/b/w/p	0-9 </br>
5	A-J	r/g/b/w/p	0-9 </br>
6	A-J	r/g/b/w/p	0-9 </br>
7	NA	r/g/b/w/p	0-9 </br>
8	NA	r/g/b/w/p	0-9 </br>
9	NA	r/g/b/w/p	0-9 </br>
0	NA	NA			NA  </br>
1-6 X   r/g/b/w/p  	0-9 </br>
# Example commands:
1Ag5 = would set the "A" Led in strip 1 to Green. Brightness at 50% </br> 
5Jw2 = would set the "J" Led in strip 5 to White. Brightness at 20% </br>
7Ar3= woulld set the entire display to red. Brightness at 30% </br>
7Jp9 = would set the entire display to purple. Brightness at 90% </br>
7Bb10 = would set the entire display to blue. Brightness at 10% </br>
8Ar8 = would set the right side of the display (1-3) to red. Brightness at 80% </br>
8Fg3 = would set the right side of the display(1-3) to green. Brightness at 30% </br>
9Fg4 = would set the left side of the display (4-6) to green. Brightness at 40% </br>
9Ab3 = would set the right side of the display (4-6) to blue. Brightness at 30% </br>
0Cr6 = sets the entire display off </br>
0Fb4 = turns the entire display off </br>
0Zz3 = turns the entire display off </br>
1Xr3 = turns the entire 1st strip to red. Brightness at 30% </br>
5Xg8 = turns the entire 5th strip to green. Brightness at 80% </br>
3Xw5 = turns the entire 3rd strip to white. Brightness at 50% </br>
