# Custom Super Tux Kart

This project is an academic project for the course of Modelisation, Conception and ergonomy of
interactive systems. The goal of this project is to create custom inputs for the game [SuperTuxKart](https://supertuxkart.net/Main_Page).

[SuperTuxKart](https://supertuxkart.net/Main_Page) is a free and open-source kart racing game, distributed under the GNU General Public License (GPL) and available on Windows, macOS, and Linux.

We use the android application MultiSenseOSC to send the data from the smartphone to the computer.

The script [InputOrientation.py]() recieve those data and treat them to convert them to keyboard input. It sends those keyboard equivalents to a server
hosted by [STK_input_server.py]() which convert it to real keyboard input that the game interprets.

