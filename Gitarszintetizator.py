import numpy as np
import sounddevice as sd
import time

# Paraméterek
SAMPLE_RATE = 44100  # Mintavételezési frekvencia
DURATION = 0.5       # Hang időtartama másodpercben

# Frekvenciák a standard gitárhúrokhoz (EADGBE hangolás)
FREQUENCIES = {
    "E2": 82.41,  # Alsó E húr
    "A2": 110.00, # A húr
    "D3": 146.83, # D húr
    "G3": 196.00, # G húr
    "B3": 246.94, # B húr
    "E4": 329.63  # Felső E húr
}

# Előre meghatározott melódia: [(húr, időtartam)]
MELODY = [
    ("E2", 0.5), ("A2", 0.5), ("D3", 0.5),
    ("G3", 0.5), ("B3", 0.5), ("E4", 0.5),
    ("E4", 0.25), ("B3", 0.25), ("G3", 0.25),
    ("E2", 0.5), ("G3", 0.5), ("B3", 0.5), ("E4", 1.0)
]

def generate_tone(frequencies, duration, sample_rate):
    """
    Több frekvencia szimultán hangjának generálása.
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = sum(0.5 * np.sin(2 * np.pi * f * t) for f in frequencies)
    return wave / len(frequencies)  # Normalizálás

def play_chords(notes):
    """
    Egyszerre több húr hangjának megszólaltatása.
    """
    frequencies = [FREQUENCIES[note] for note in notes if note in FREQUENCIES]
    if frequencies:
        tone = generate_tone(frequencies, DURATION, SAMPLE_RATE)
        sd.play(tone, samplerate=SAMPLE_RATE)
        sd.wait()
    else:
        print(f"Nincsenek érvényes húrok a megadottak között: {notes}")

def play_melody():
    """
    Előre meghatározott melódia lejátszása.
    """
    for note, duration in MELODY:
        if note in FREQUENCIES:
            tone = generate_tone([FREQUENCIES[note]], duration, SAMPLE_RATE)
            sd.play(tone, samplerate=SAMPLE_RATE)
            sd.wait()
        else:
            print(f"Nincs ilyen húr: {note}")

# Interaktív menü
if __name__ == "__main__":
    print("Gitárszintetizátor!")
    print("Elérhető húrok: ", ", ".join(FREQUENCIES.keys()))
    print("Írj be egyszerre több húrt vesszővel elválasztva (pl. E2,A2), vagy 'start'-ot a melódia lejátszásához.")

    while True:
        user_input = input("Húr(ok) vagy parancs ('exit' a kilépéshez): ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'start':
            play_melody()
        else:
            notes = user_input.split(",")
            play_chords([note.strip() for note in notes])
