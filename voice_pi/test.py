from commands import CommandBuilder
from speaker import Speaker

speaker = Speaker(out_loud=False)
cb = CommandBuilder(speaker=speaker)
cb.build_command()