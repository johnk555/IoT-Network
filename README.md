//This is a script to measure data from 3 sensors and shows them

// BME // VIN -> 3V // GND -> GND // SCK -> SCL // SDI -> SDA

// TCS34725 // 3V3 -> 3V // GND -> GND // SCK -> SCL // SDI -> SDA // LED THAT IDENTIFIES THE LIGHT // 1 -> 13 // 2(BIG) -> 3V // 3 -> 11 // 4 -> 9

// PIR // 1(RED) -> 3V // 2(YELLOW) -> 12 // 3(BLACK) -> GND //LED // 1 -> GND // 2 -> 10


# Enable MQTT
command ipconfig
Go to file mosquitto
run command mosquitto
mosquitto_pub -h 192.168.88.220 -t home/room/led -m "OFF"   
mosquitto_pub -h 192.168.88.220 -t home/room/led -m "ON"
mosquitto_sub -h 192.168.88.220 -t test_topic  // to another cmd
