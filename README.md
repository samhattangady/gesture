Completed as final project of CS50x.
Youtube link: https://www.youtube.com/watch?v=0hp-6y0bo_Q

# gesture

We watch Minority Report and wish that we could make the objects on our screen move with just movements of our fingers, without ever realizing that one piece of hardware that is really needed to make that happens comes preinstalled in almost every single computer and laptop. 
So here I am, trying to make you feel like you are in the future by tapping into your webcam.

We use OpenCV for image processing and pygame in the final game that we implement.

File listing and some instructions:

1. colourPicker.py
This is used to isolate colours. In this system, we use highly contrasting objects, and attach them to our fingertips. So we need the HSV threshhold values.
So open this script, and you will have two windows. In the mask window, you will see the result of moving the trackbars present in the other window. What you want to do is isolate your object and note down the HSV upper and lower limits. This must then be inputted into the colours.py file
  TODO: Allow direct recording into file with button.

2. fingerTrack.py
This is used to check what the camera is actually tracking. So you can use this to test whether the background is interfering etc. It doesn't import the track.py file, but the algorithm is essentially identical.

3. dots.py
This is the most basic barebones structure of what we are trying to accomplish. If you want to build your own games/apps using this concept, this will be your foundation

4. game.py
This is my implementation of a very simple game where you can pick up and move a box. It may be updated in the future, but it gives a good idea of how to use OpenCV and pygame together to create something.

This is a work in progress. But this should get you started. The helper files are quite self explanatory.
Do feel free to use this to create your own awesome stuff. Have fun.
