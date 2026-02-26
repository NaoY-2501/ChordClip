from io import BytesIO
from typing import List

import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


def generate_midi(notes: List[int], bpm: int, tick: int) -> MidiFile:
    """
    Generate a MIDI file from the notes
    Args:
        notes: List[int] - The notes to generate a MIDI file from
        bpm: int - The tempo of the MIDI file
        length: int - The length of the MIDI file
    Returns:
        MidiFile - The MIDI file
    """
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm))) 

    for note in notes:
        track.append(Message('note_on', note=note, velocity=120, time=0))
    
    # ノートオフ（最後の1音にだけ time を持たせる）
    for i, note in enumerate(notes):
        track.append(
            Message(
                'note_off',
                note=note,
                velocity=60,
                time=tick if i == 0 else 0
            )
        )
    buf = BytesIO()
    mid.save(file=buf)
    buf.seek(0)
    return buf.getvalue()