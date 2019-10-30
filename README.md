# Treasure hunt
I made this for my daughters 8:th birthday.


![Treasure Chest](https://github.com/Snille/Treasurehunt/blob/master/Pictures/Kista-01.jpg)
![Pireate Coins](https://github.com/Snille/Treasurehunt/blob/master/Pictures/potcc.jpg)



It's built around a 5kg "[Load Cell](https://www.ebay.co.uk/itm/Electronic-Balance-Weighing-Load-Cell-Sensor-5Kg-with-HX711-Module/162241279056?hash=item25c6557450:g:l7gAAOSwh2xYAwSK)" with a HX711 module a "[Treasure Chest](https://fyndgiganten.se/produkt/vidaxl-forvaringslada-i-atervunnet-tra/)" and the Pirates of the Caribbean treasure [Coin](https://www.thingiverse.com/thing:2936980).


When the members of the birthday party finds the Treasure Chest, they can not open the lid fully. It's locked from the inside and can only be opened about 15mm.


When they lift and close the lid the first time the "Explain-01.wav" and then "Haha-01.wav" files are played. It continues to play even if the lid is closed again. If they lift and close again the "Explain-02.wav" and "Haha-02.wav" are played and if they lift and close a third time the "Explain-03.wav" and "Haha-03.wav" are played. Then it loops back to the first after every lift and close until some one starts to add in coins.


The participants has to find all the 100 (definable) pirate coins and push them in to the chest (lifting the lid to get them in). Every time the lid closes the "Count-01.wav", "XX.wav" (depending of the number of coins added) and "Count-02.wav" will be played.


This will continue to happen until all coins are collected and inserted. 


When the correct amount of coins are inserted, the chest will unlock (the servo moves so the latch gets unhooked) and the last "Done-01.wav" will be played and tce chest can now be opened.



PS: There is also a "secret" unlock button that can be hold to open the chest if needed. But it's of course only for testing and emergency's. :)
