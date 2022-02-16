from skippytel.cli import pass_environment
import click
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x



@click.command("counter", short_help="TX counter")
@pass_environment
def cli(ctx):
    """
    Transmit counter 
    """

    ctx.log(click.style("Launching Microwormhole", fg="cyan"))
    ctx.vlog(click.style("Debug", fg="red"))

    
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    # 128x32 OLED Display
    reset_pin = DigitalInOut(board.D4)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
    # Clear the display.
    display.fill(0)
    display.show()
    width = display.width
    height = display.height

    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power = 23
    prev_packet = None

    while True:
        display.fill(0)
        for count in range(0,1000,1):
            
            display.text(count, 35, 0, 1)
            count_bytes = bytes(str(count),"utf-8")
            rfm9x.send(count_bytes)
            display.show()
            time.sleep(1)



        

