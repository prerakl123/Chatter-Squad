# Chatter-Squad
Simple Python based Chatting Software. It can run on local machine server or from different devices connected to the same server (example: WiFi).

# How to run

The project can be run by two means: GUI or CMD.

For PyCharm (or any IDE):
Open the ChatZone folder as the PyCharm project.

_**GUI based**_:
Run `serverGUI.py` for tkinter GUI based interface. When the black window with the message *Waiting for connection...* appears, minimize it and run `clientGUI.py`. Make sure that for `clientGUI.py` **Allow run in parallel** checkbox is checked (for PyCharm users it is present under **Edit** tab in configurations).
Enter your name in the `clientGUI.py` window and minimize it. Now run `clientGUI.py` again and enter name.

By default the server and client will run on the same computer under the host IP: 127.0.0.1 and port: 330000. For using different devices first connect to the same network (like WiFi) from the devices then in `main()` of `serverGUI.py` set the `host` parameter of `CZServer()` to `''` and `port=80` (change port only if it doesn't work by default). Similarly in `clientGUI.py` provide the IP address of the connected network to `host` in `CZClient()` in `main()` and keep the port same as in `serverGUI.py` (if not changed in server, don't change in client).


_**CMD based**_:
Run `serverCMD.py`. By default, just as in `serverGUI.py`, _HOST_ and _PORT_ will be 127.0.0.1 and 33000, respectively, and can be changed according to network as described above. Similar applications are for `clientCMD.py`.

Here several Command Line windows have to be opened in order to run server and client on the same machine.

> Server Logs will be saved in `server_logs.json`, which contains information about who joined and left, and when.

Here are some screenshots:

serverGUI:

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/serverSS.png?raw=true)

clientGUI:

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/clientSS.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS1.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS2.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS3.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS4.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS5.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS6.png?raw=true)

![](https://github.com/prerakl123/Chat-Zone/blob/main/screenshots/SS7.png?raw=true)
