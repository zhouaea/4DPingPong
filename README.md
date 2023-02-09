# 4D-Ping-Pong: Augmenting Sports With A Digital Audience
*In the past couple of decades we've seen developers bring sports to video games, but what if we brought video games to sports?*

I set out to design a program that could monitor a ping pong game in real time and augment the physical ping pong experience. For example, if a shot reached a certain high speed, strategically placed electric fans could blow on the receiver to make them feel the raw power of their opponent's attack. This project was inspired by Tangible Computer Interface Research, specifically [PingPongPlus](https://tangible.media.mit.edu/project/pingpongplus/) and [PingPongPlusPlus](https://tangible.media.mit.edu/project/pingpongplusplus/), as well as [4DX movie technology](https://www.cj4dx.com/aboutus/aboutus.php). 

## Monitoring the game
The PingPongPlus and PingPongPlusPlus projects required custom hardware that was difficult for anyone without an electrical engineering background to make. I wanted to create a set up that anyone with a computer and a phone could use. Instead of using sound trackers placed under a table, I opted to record gameplay with my phone, connect the live footage to my laptop, and have the laptop perform an object detection algorithm on it. 

Unfortunately, I had a problem with speed. Put away shots in ping pong happen often and move so fast that a 30 frame per second camera can't capture its movement accurately. This meant that my laptop had to get 60 images every second: a lot of images to process in a short amount of time. A machine learning approach ended up being too slow on my 5 year old gaming laptop. 

I opted for a much simpler color filtering method, which mostly worked. There were two main problems with this approach: the ball had to be a distinctly different color from its surroundings, and even in 60 fps, a really fast ball would create motion blur in the image that would literally change its color. Once I could kind of track the ball, I wrote some code to calculate statistics like ball speed and determine events like ball bounces, ball hits, and net passes.

To follow the flow of the game (ex: who's serving? who hit the ball? who just won/lost the point? how many points does each person have?), I implemented a ping pong state machine algorithm mostly based on what was done by some [grad students at Cornell](http://people.ece.cornell.edu/land/courses/ece5760/FinalProjects/s2015/ttt/ttt/ttt/index.html). With ball tracking and game state tracking out of the way, I could finally make ping pong "4D"!

![ping pong demo](https://user-images.githubusercontent.com/75145715/217930320-cd5a3613-3a3e-434f-88ac-e7876c0962bf.gif)

## Augmenting the game
My first instinct was to do the electric fan idea described above, but since I didn't actually own any fans, I decided to start small and add interactive sound effects like you might see in a video game. Below is an example of some events I coded, using the nostalgic sound design of Wii Sports:
- startMenuMusic(): Wii Fitness - Test OST | Wii Sports
- startBackgroundMusic(): Tennis - Select Position OST | Wii Sports
- startMatchPointMusic(): Wii Sports Music - Tennis Training
- startVictoryMusic(): Wii Sports - Music - Tennis Results
- playSoundGameEnds() - text to speech program (tts): Wii Tennis Sample 23, then Wii Crowd Slow Clap
- playSoundPreServe() - tts
- playSoundServeWarning() - tts
- playSoundServeApproved(): Wii Golf Sample 47
- playSoundFast(): Golf announcer nice shot
- playSoundSave(): WOAH
- playSoundAfterGoodPoint(): Wii Sports Crowd Slow Clap

The goal of these sound effects were to incentivize a specific kind of play. For example, the clapping sound effect doesn't happen after a point unless at some point the ball was hit really hard and didn't miss the table. Whoever was able to do that would be rewarded with a "nice shot" sound effect in real time while they were playing. 

## Results
I tried this program with friends and family and it actually made playing more fun. My laptop was acting as an active audience hyping players up. My code worked less than flawlessly, with the biggest problem being ball tracking (for the reasons described earlier) and game state logic. My game state logic was not fault tolerant, so the ball tracking and how players showed the ball to the camera really had to be flawless or else the code would be wildly off on what was happening.

I only spent three weeks on this over the summer for fun, but I can see this technology having serious potential. As personal computers become more powerful, and with some professional polish, a 4d ping pong application could become a reality for consumers.

-Neo Zhou, Boston College Class of 2024
