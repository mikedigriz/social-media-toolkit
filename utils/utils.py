from os import name, system

from playsound import playsound


# Имплементация музыкальных сопровождений событий для разных os

def win_beep():
    import winsound
    duration = 300  # милисек
    freq = 165  # Hz
    winsound.Beep(freq, duration)
    winsound.Beep(freq, duration)


def linux_beep():
    """required sudo apt install sox"""
    duration = 0.5  # seconds
    freq = 500  # Hz
    system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


def linux_tts():
    """required sudo apt install speech-dispatcher"""
    system('spd-say "your program has finished"')


def beep():
    print(name)
    if name == 'nt':
        win_beep()
    else:
        linux_beep()


def system_error():
    playsound('utils/other/error.mp3')


def finish():
    playsound('utils/other/finish.mp3')
