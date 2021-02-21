# Chat-Zone
Simple Python based Chatting Software. It can run on local machine server or from different devices connected to the same server (example: WiFi).

# How to run

The project can be run by two means: IDE or CMD.

For PyCharm (or any IDE):
Open the ChatZone folder as the PyCharm project.

GUI based:
Run `serverGUI.py` for tkinter GUI based interface. When the black window with the message *Waiting for connection...* appears, minimize it and run `clientGUI.py`. Make sure that for `clientGUI.py` **Allow run in parallel** checkbox is checked (for PyCharm users it is present under **Edit** tab in configurations).
Enter your name in the `clientGUI.py` window and minimize it. Now run `clientGUI.py` again and enter name.

By default the server and client will run on the same computer under the host IP: 127.0.0.1   For using different devices first connect to the same network (like WiFi) from the devices then in `main()` of `serverGUI.py` set the `host` parameter of `CZServer()` to `''` and `port=80` (change port only if it doesn't work by default). Similarly in `clientGUI.py` provide the IP address of the connected network to `host` in `CZClient()` in `main()`. 
