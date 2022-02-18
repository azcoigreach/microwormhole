from skippytel.cli import pass_environment
import click
import time
import busio
import digitalio
import board
import adafruit_ssd1306
import adafruit_rfm9x
import os
import psutil



@click.command("node2", short_help="Node packet updater")
@pass_environment
def cli(ctx):
    """
    Transmit Node information and stats 
    """

    ctx.log(click.style("Launching Microwormhole", fg="cyan"))
    ctx.vlog(click.style("Debug", fg="red"))

    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    # 128x32 OLED Display
    reset_pin = digitalio.DigitalInOut(board.D4)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
    # Clear the display.
    display.fill(0)
    display.show()
    width = display.width
    height = display.height

    
    # Define radio parameters.
    RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
    # module! Can be a value like 915.0, 433.0, etc.

    # Define pins connected to the chip.
    # set GPIO pins as necessary - this example is for Raspberry Pi
    CS = digitalio.DigitalInOut(board.CE1)
    RESET = digitalio.DigitalInOut(board.D25)

    # Initialize SPI bus.
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    # Initialze RFM radio

    # Attempt to set up the rfm9x Module
    try:
        rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
        display.text("rfm9x: Detected", 0, 0, 1)
    except RuntimeError:
        # Thrown on version mismatch
        display.text("rfm9x: ERROR", 0, 0, 1)

    display.show()


    # set delay before transmitting ACK (seconds)
    rfm9x.ack_delay = 0.1
    # set node addresses
    rfm9x.node = 2
    rfm9x.destination = 1
    # initialize counter
    counter = 0
    ack_failed_counter = 0

    # Wait to receive packets.
    print("Waiting for packets...")
    while True:
        # Look for a new packet: only accept if addresses to my_node
        packet = rfm9x.receive(with_ack=True, with_header=True)
        # If no packet was received during the timeout then None is returned.
        if packet is not None:
            # Received a packet!
            # Print out the raw bytes of the packet:
            print("Received (raw header):", [hex(x) for x in packet[0:4]])
            print("Received (raw payload): {0}".format(packet[4:]))
            print("RSSI: {0}".format(rfm9x.last_rssi))

            display.fill(0)
            # display.text("Received (raw header):", [hex(x) for x in packet[0:4]], width - 1, height - 1, 1)
            display.text("Received (raw payload): {0}".format(packet[4:]), 1, 1, 1)
            display.text("RSSI: {0}".format(rfm9x.last_rssi), 1, 10, 1)
            display.show()

            # send response 2 sec after any packet received
            time.sleep(2)
            counter += 1
            # send a  mesage to destination_node from my_node
            if not rfm9x.send_with_ack(
                bytes("response from node {} {}".format(rfm9x.node, counter), "UTF-8")
            ):
                ack_failed_counter += 1
                print(" No Ack: ", counter, ack_failed_counter)



        

