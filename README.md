# The Hunt for the Pirate coins
I made this event for my daughters 8:th birthday. The concept is copied from the theme of "Pirates of the Caribbean - The Cruise of the Black Perl". Basically the party guests have to find 100 [Pirate coins](https://www.thingiverse.com/thing:2936980)" to be able to "unlock" the Treasure Chest (containing candy).

Background story: During the summer, we had our yard dig up to add pluming to a new building. This lead to some strange finds in the ground. Among them where an old "chimney". So, I will use this memory to trigger some suspense when I give them a key "to something" that I found in the ground when we dug.
The key is for a small padlock that keeps the chest locked.

This is the plan:
The locked chest (locked with the padlock, they now have the key for) is setup in my office at home, I have prepared it so it will look really messy, paper-boxes everywhere, dirt on the floor and the chest will be chained to the wall so it can not be taken out of the room.

The door to the office will be closed and locked (it's usually open). But nothing suspicious will show from the "outside". 

when it's time for the hunt to begin, I start the start.py script on the raspberry pi installed inside the "Chest" (using SSH from my phone).
The script first "locks" the chest from the inside (using the servo that hatches on to the latch), starts the warm up of the smoke machine, pulls down the blinds over the window, sets the lighting to a prepared setting (turning on the "fire-like" lamps and lowering the ceiling light so that it shimmers), when the smoke machine is warm it fills the room with smoke and then changes the appearance of our [MagicMirror](https://forum.magicmirror.builders/topic/4563/snilles-magic-mirror-project?_=1603825886962) to a special "Treasure Hunt" profile and sets the text "The hunt for the pirate coins has begun!".

Then a preset playlist will be started on the SONOS player in the office at a specific volume level. This playlist just have one [track](https://www.youtube.com/watch?v=aylZ5naovxY) with the sounds of a wooden ship on the sea. You can also hear someone walking around.
While this is playing, from time to time, a laugh will be heard (played by the script). Hopefully after a while, the guests will start to noticing the sounds coming from the room. The problem is that it's locked.

They will of course ask for a key to the door, but I will just look surprised and say that the door should not be locked... Then give them the idea to "maybe" push a paper "under" the door and then use a stick (that I happens to have) to push the key out from the lock so that it falls down on the paper and they can pull it out from under the door using the paper. :)

When they manage to get in to the room, they are walking in to a room that is filled with smoke (I hacked the [smoke machine](https://www.kjell.com/se/produkter/hem-kontor-fritid/party-karaoke/rokmaskiner/rokmaskin-400-w-p22223) a bit to be able to control it with the Raspberry Pi from the script) and the lights are dimmed. Every time the random laugh is played a puff of smoke is produced. I also replaced the "on/off" switch on the wall with a "dummy" cover, so they can not change the lights. The "Ship sound" and the laughs are played pretty loud to make it more intimidating.

The treasure chest is placed on the flor and the "firey lights" are places beside the chest to make it look more "piraty" :), when they unlock the padlock and try to open the chest, a voice will say "To unlock the chest, you have to push at least 100 pirate coins in to the slot that opens up when trying to open the lid!". Now they will have to rummage through the card board boxes in the room to find all the coins. Every time they open (and close) the lid, the voice will tell how many coins they have found so far and the Magic Mirror will also display how many coins they have collected. A bit of smoke will be puffed out at every laugh when the lid closes.

When they finally have pushed all 100 coins in the chest, the lid will unlock (the servo will unlatch) and the lid can be opened. A message will be played saying "Congratulations!! You have found the 100 pirate coins, the chest is unlocked. I hope the candy is good!" and the room will then be "restored" to an office. Lights dims up to a normal and the blind is pulled back up (smoke will still be there of course... :)

This is the chest and the printed pirate coins:

![Treasure Chest](/Pictures/Kista-01-small.jpg)
![Treasure Chest](/Pictures/Kista-02-small.jpg)
![Pireate Coins](/Pictures/potcc-small.jpg)


The electronics:

![Electronics](/Pictures/Electronics.png)


This is the inside. The "outer" shelf is attached to the load cell and weigh the coins when they are pushed in from the front and the sides.

![Inside Back](/Pictures/Backside-Inside.png)
![Inside Frpnt](/Pictures/Frontside-Inside.png)


![Open](/Pictures/Kista-04-small.png)
![Electronics inside](/Pictures/Kista-03-small.png)

It's built around a 5kg "[Load Cell](https://www.ebay.co.uk/itm/Electronic-Balance-Weighing-Load-Cell-Sensor-5Kg-with-HX711-Module/162241279056?hash=item25c6557450:g:l7gAAOSwh2xYAwSK)" with a HX711 module a "[Treasure Chest](https://fyndgiganten.se/produkt/vidaxl-forvaringslada-i-atervunnet-tra/)" and the Pirates of the Caribbean treasure [Coin](https://www.thingiverse.com/thing:2936980).

When they lift and close the lid the first time the "Explain-01.wav" and then "Haha-01.wav" files are played. It continues to play even if the lid is opened and closed over and over until it's played in full. Then if they lift and close again the "Explain-02.wav" and "Haha-02.wav" are played the same way and if they lift and close a third time the "Explain-03.wav" and "Haha-03.wav" are played. Then it loops back to the first and so on, after every lift and close until some one starts to add in coins.

The participants has to find all the 100 (definable) pirate coins and push them in to the chest (lifting the lid the 15mm to get them in). Every time the lid closes the "Count-01.wav", "XX.wav" (depending of the number of coins added) and "Count-02.wav" will be played.


This will continue to happen until all coins inserted.


When the correct amount of coins are inserted, the chest will unlock (the servo moves so the latch gets unhooked) and the last "Done-01.wav" will be played and the chest can now be opened.


PS: There is also a "secret" unlock button that can be hold to open the chest if needed. But it's of course only for testing and emergency's. :)
