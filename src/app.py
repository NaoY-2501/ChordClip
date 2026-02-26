import csv
from typing import Dict, List

import streamlit as st

from consts import CHORDS, KEY_DICT, KEY_DICT_INV, SCALES_PATH, TICK_DICT
from midi.generate import generate_midi


def load_scales() -> Dict[str, List[int]]:
    """
    Load scales from scales.csv
    
    Args:
        None
    Returns:
        Dict[str, List[int]] - The scales
    """
    scales = {}
    with SCALES_PATH.open("r") as f:
        fieldnames = ("idx", "scaleName", "notes")
        reader = csv.DictReader(f, fieldnames=fieldnames)
        next(reader)
        for row in reader:
            notes = row["notes"].split(",")
            scales[row["scaleName"]] = [int(note) for note in notes[:-1]]
    return scales


def initialize() -> None:
    """
    Ensure that the scales are loaded into the session state
    """
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.scales = load_scales()


def rotate_scale(scale_pc: List[int], root_pc: int) -> List[int]:
    """
    Rotate the scale to the root note
    Args:
        scale_pc: List[int] - The scale in pitch classes
        root_pc: int - The root note in pitch classes
    Returns:
        List[int] - The rotated scale
    """
    idx = scale_pc.index(root_pc)
    rotated = scale_pc[idx:] + scale_pc[:idx]
    return rotated


def chord_degree_to_pc(scale: List[int], chord_degree: int) -> int:
    """
    Convert a chord degree to a pitch class
    Args:
        scale: List[int] - The scale in pitch classes
        chord_degree: int - The chord degree
    Returns:
        int - The pitch class
    """
    scale_len = len(scale)
    octave = chord_degree // scale_len
    index = chord_degree % scale_len
    return scale[index] + 12 * octave


def get_diatonic_chords(rotated_scale_pc: List[int], scale_len: int, chord_pcs: Dict[str, List[int]]) -> Dict[str, List[int]]:
    """
    Get the diatonic chords from the rotated scale
    Args:
        rotated_scale_pc: List[int] - The rotated scale in pitch classes
        scale_len: int - The length of the scale
    Returns:
        Dict[str, List[int]] - The diatonic chords
    """
    scale_pc_set = {pc % 12 for pc in rotated_scale_pc}

    diatonic_chords = {}
    for chord_name, chord_degrees in chord_pcs.items():
        chord_pc = {
            rotated_scale_pc[i % scale_len] % 12
            for i in chord_degrees
        }
        if chord_pc.issubset(scale_pc_set):
            diatonic_chords[chord_name] = chord_degrees
    return diatonic_chords


def pc_to_midi(pc: int, root_midi: int) -> int:
    """
    Convert a pitch class to a MIDI note number
    Args:
        pc: int - The pitch class
        root_midi: int - The root MIDI note number
    Returns:
        int - The MIDI note number
    """
    base_pc = root_midi % 12
    diff = (pc - base_pc) % 12
    return root_midi + diff


initialize()

st.title("ChordClip")

key_note_name = st.selectbox(
    "Select a key",
    list(KEY_DICT.keys())[:12],
    placeholder="Select a key",
)
scale_name =st.selectbox(
    "Select a scale",
    list(st.session_state.scales.keys()),
    placeholder="Select a scale",
)
bpm = st.slider(
    "Select a BPM",
    min_value=60,
    max_value=240,
    value=120
)
tick_str = st.select_slider("Select a chord length", options=["1/4bar", "1/2bar", "1bar"])
tick = TICK_DICT[tick_str]

scale_pc = st.session_state.scales[scale_name]
key_midi = KEY_DICT[key_note_name]
scale_midi = [pc + key_midi for pc in scale_pc]
scale_note_name = [KEY_DICT_INV[midi_num] for midi_num in scale_midi]
root_note_name = st.radio("Select a root note", scale_note_name, horizontal=True)

root_note_name = root_note_name if root_note_name else ""
root_midi = KEY_DICT[root_note_name]
root_pc = (root_midi - key_midi) % 12

chord_pcs = {}
for chord_name, chord_degrees in CHORDS.items():
    chord_pcs[chord_name] = [chord_degree_to_pc(scale_pc, d) for d in chord_degrees]

rotated_scale_pc = rotate_scale(scale_pc, root_pc)
diatonic_chords = get_diatonic_chords(rotated_scale_pc, len(scale_pc), chord_pcs)
selected_chord_name = st.selectbox("Select a chord", list(diatonic_chords.keys()))
selected_chord_intervals = diatonic_chords[selected_chord_name]

midi_notes = [root_midi + pc for pc in selected_chord_intervals]
midi_bytes = generate_midi(midi_notes, bpm, tick)

st.download_button(
    label="Download MIDI",
    data=midi_bytes,
    file_name=f"{root_note_name}-{selected_chord_name}-{tick_str}.mid",
    mime="audio/midi"
)