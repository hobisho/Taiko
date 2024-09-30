from orange import taiko
import tensorflow as tf

song = taiko('../song/astral ability/astral ability.tja')
labal=[int(c) for c in "".join(song.sheets[0].noteList)]
