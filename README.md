# test-ip-connect

The application was developed 100% using `Python`, also utilizing the local Sqlite3 database.

It consists of a system that performs a ping test on a list with various IP addresses, allowing the addition or removal of more IPs.

The graphical interface was created using the `Tkinter` library, where the screen updates every 3 minutes `180.000ms`, re-executing the ping test. If the IP address is available, it will be colored green; if it is not available, it will be colored red.

Additionally, the screen can be manually refreshed using the button.
