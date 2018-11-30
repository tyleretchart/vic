# from commands import CommandBuilder
# from speaker import Speaker

# speaker = Speaker(out_loud=False)
# cb = CommandBuilder(speaker=speaker)
# cb.build_command()

from gpiozero import LED

led = LED(18)
led.turn_on()