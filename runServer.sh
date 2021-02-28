#!/bin/bash
java -jar ./selenium/selenium-server.jar -host localhost -port 5555 -role node -hub http://localhost:4444/grid/register
