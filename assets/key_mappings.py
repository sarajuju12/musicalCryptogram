C_G_Am_F = {
    "a": ["G6"], "b": ["C3"], "c": ["D3"], "d": ["E3"], "e": ["F3"], "f": ["G3"], "g": ["A3"], "h": ["B3"],
    "i": ["C4"], "j": ["D4"], "k": ["E4"], "l": ["F4"], "m": ["G4"], "n": ["A4"], "o": ["B4"], "p": ["C5"],
    "q": ["D5"], "r": ["E5"], "s": ["F5"], "t": ["G5"], "u": ["A5"], "v": ["B5"], "w": ["C6"], "x": ["D6"],
    "y": ["E6"], "z": ["F6"], " ": [" "]
}

C_F_G_E = {
    "a": ["G4"], "b": ["C4"], "c": ["E5"], "d": ["A5"], "e": ["G3"], "f": ["D4"], "g": ["E3"], "h": ["Ab4"],
    "i": ["B4"], "j": ["F3"], "k": ["C3"], "l": ["D3"], "m": ["B5"], "n": ["Ab5"], "o": ["F4"], "p": ["G5"],
    "q": ["B6"], "r": ["G6"], "s": ["C5"], "t": ["E4"], "u": ["F5"], "v": ["D5"], "w": ["A4"], "x": ["E6"],
    "y": ["F6"], "z": ["C6"], " ": [" "]
}

Cm_Gm_Dm_Am = {
    "a": ["D4"], "b": ["Bb6"], "c": ["Eb5"], "d": ["F4"], "e": ["E3"], "f": ["C4"], "g": ["D5"], "h": ["Bb5"],
    "i": ["G5"], "j": ["A6"], "k": ["E4"], "l": ["F5"], "m": ["F6"], "n": ["D6"], "o": ["C5"], "p": ["Eb6"],
    "q": ["Eb3"], "r": ["G4"], "s": ["A5"], "t": ["E5"], "u": ["C6"], "v": ["A4"], "w": ["C3"], "x": ["Bb4"],
    "y": ["G3"], "z": ["Eb4"], " ": [" "]
}

Chord_1 = {
    "a": ["C3", "E3", "G3"],  # C Major Chord
    "b": ["D3", "G4", "B4"],  # G Major Chord
    "c": ["A3", "C4", "E4"],  # A Minor Chord
    "d": ["F3", "A3", "C4"],  # F Major Chord
    "e": ["G3", "C4", "E4"],  # C Major Chord
    "f": ["B3", "D4", "G4"],  # G Major Chord
    "g": ["E3", "A4", "C4"],  # A Minor Chord
    "h": ["C4", "E4", "G4"],  # C Major Chord
    "i": ["D4", "G4", "B4"],  # G Major Chord
    "j": ["A4", "C5", "E5"],  # A Minor Chord
    "k": ["F4", "A4", "C5"],  # F Major Chord
    "l": ["G4", "C5", "E5"],  # C Major Chord
    "m": ["B4", "D5", "G5"],  # G Major Chord
    "n": ["E4", "A4", "C5"],  # A Minor Chord
    "o": ["C5", "E5", "G5"],  # C Major Chord
    "p": ["D5", "G5", "B5"],  # G Major Chord
    "q": ["A5", "C6", "E6"],  # A Minor Chord
    "r": ["F5", "A5", "C6"],  # F Major Chord
    "s": ["G5", "C6", "E6"],  # C Major Chord
    "t": ["B5", "D6", "G6"],  # G Major Chord
    "u": ["E5", "A5", "C6"],  # A Minor Chord
    "v": ["C6", "E6", "G6"],  # C Major Chord
    "w": ["D6", "G6", "B6"],  # G Major Chord
    "x": ["A6", "C7", "E7"],  # A Minor Chord
    "y": ["F6", "A6", "C7"],  # F Major Chord
    "z": ["F2", "A2", "C3"],  # F Major Chord
    " ": [" "]
}

Chord_2 = { 
    "a": ["C4", "E4", "G4"],
    "b": ["E5", "Ab5", "B5"],
    "c": ["A5", "C6", "F6"],
    "d": ["G3", "B3", "D4"],
    "e": ["D4", "G4", "B4"],
    "f": ["E3", "Ab3", "B3"],
    "g": ["Ab4", "B4", "E5"],
    "h": ["B4", "D5", "G5"],
    "i": ["F3", "A3", "C4"],
    "j": ["C3", "F3", "A3"],
    "k": ["D3", "G3", "B3"],
    "l": ["B5", "E6", "Ab6"],
    "m": ["Ab5", "B5", "E6"],
    "n": ["F4", "A4", "C5"],
    "o": ["G5", "C6", "E6"],
    "p": ["B3", "D4", "G4"],
    "q": ["D6", "G6", "B6"],
    "r": ["C5", "E5", "G5"],
    "s": ["E4", "G4", "C5"],
    "t": ["F5", "A5", "C6"],
    "u": ["D5", "G5", "B5"],
    "v": ["A4", "C6", "F6"],
    "w": ["E6", "Ab6", "B6"],
    "x": ["A3", "C4", "F4"],
    "y": ["C6", "E6", "G6"],
    "z": ["G4", "B4", "D5"],
    " ": [" "]
}

# combination of notes and chords?

# Chord_template = {
#     "a": [], 
#     "b": [],  
#     "c": [], 
#     "d": [], 
#     "e": [], 
#     "f": [],  
#     "g": [],  
#     "h": [],  
#     "i": [],  
#     "j": [],  
#     "k": [],
#     "l": [], 
#     "m": [],  
#     "n": [], 
#     "o": [],  
#     "p": [], 
#     "q": [], 
#     "r": [],  
#     "s": [],  
#     "t": [],
#     "u": [],  
#     "v": [],  
#     "w": [],  
#     "x": [],  
#     "y": [],  
#     "z": [], 
# }

key_mappings = {
    "C-G-Am-F": C_G_Am_F,
    "C-F-G-E": C_F_G_E,
    "Cm-Gm-Dm-Am": Cm_Gm_Dm_Am,
    "Chord_1": Chord_1,
    "Chord_2": Chord_2
}