import json
import utils as ut
import streamlit as st
import pyperclip
from time import perf_counter


def update_value(value):
    st.session_state.settings[value] = st.session_state[value+'_input']

def settings_management():

    with st.expander("Settings"):
        initial_prompt_col, english_check_col = st.columns([4, 1], vertical_alignment="center")

        with initial_prompt_col:
            st.text_area("Initial Prompt", value=st.session_state["settings"]["initial_prompt"], placeholder="Instructions for Transcribing the file.", height=60, key="initial_prompt_input", on_change=update_value, args=["initial_prompt"])

        with english_check_col:
            st.checkbox("Only English Mode", value=st.session_state.settings["english_mode"], key="english_mode_input", on_change=update_value, args=["english_mode"])

        whisper_model_col, delete_all_models_col = st.columns([2, 1], vertical_alignment="center")

        with whisper_model_col:
            models =  ['turbo', 'large-v3', 'distil-large-v3', 'large', 'medium', 'small', 'base', 'tiny']
            st.selectbox("Select Faster Whisper Model", models, index = models.index(st.session_state.settings['transcribe_model']) , key="transcribe_model_input", on_change=update_value, args=["transcribe_model"])
            st.caption("First run may be slow due to model being downloaded")

        with delete_all_models_col:
            st.button("Delete All Models", on_click=ut.delete_all_models, args=[st.toast], help="All Models in model directory get deleted", type="primary", width='stretch')

        with st.container(horizontal=True, horizontal_alignment='left'):
            if st.button("Save Settings"):
                with open("settings.json", "w") as f:
                    json.dump(st.session_state.settings, f, indent=2)

            if st.button("Set to Default Settings"):
                with open("default_settings.json", "r") as f:
                    default_settings = json.load(f)

                with open("settings.json", "w") as f:
                    json.dump(default_settings, f, indent=2)
                    st.session_state.settings = default_settings
                st.rerun()

def display_transcribing(uploaded_file):

    start_time = perf_counter()
    with st.spinner("Transcribing...", show_time=True):
        result = ut.transcribe_audio(uploaded_file, st.session_state.settings["transcribe_model"],
                                     language="en" if st.session_state.settings["english_mode"] else None,
                                     initial_prompt=st.session_state.settings["initial_prompt"])
    end_time = perf_counter()
    time_taken = f'{(end_time - start_time):.2f}'

    return result, time_taken

def display_result(result, time_taken):

    with st.container(border=True):
        text_tab, timestamps_tab, timestamps_word_tab = st.tabs(['Transcribe', 'Timestamps', 'Word Timestamps'])

        def display_tab(text, key, download_button_label, download_file_name, download_file_mime, font_size_rem='1.2'):
            rendered_text = lambda text, font_size_rem: f"<div style='font-size: {font_size_rem}rem; padding-top:1rem; padding-bottom:1rem;'>" + text.replace("\n", "<br>") + "</div>"

            with st.container(horizontal=True, horizontal_alignment='left'):
                st.button("Copy", on_click=pyperclip.copy, args=[text], key=key + "_copy_button")
                st.download_button(label=download_button_label, data=text.encode("utf-8"), file_name=download_file_name,
                                   mime=download_file_mime, icon=":material/download:", on_click="ignore",
                                   key=key + "_download_button")

            st.markdown(rendered_text(text, font_size_rem), unsafe_allow_html=True)

        with text_tab:
            display_tab(result['text'], "text", "Download as TXT", "transcribe.txt", "text/plain")

        with timestamps_tab:
            display_tab(result['timestamps'], "timestamps", "Download as SRT", "timestamps.srt", "text/plain", "1")

        with timestamps_word_tab:
            display_tab(result['timestamps_word'], "timestamps_word", "Download as SRT", "timestamps_word.srt","text/plain", "1")

    st.markdown(f"**Transcribed in {time_taken} seconds**")
    st.divider()

def main():

    if "settings" not in st.session_state:
        with open("settings.json", "r") as file:
            st.session_state["settings"] = json.load(file)

    st.set_page_config("Transcribot", page_icon="🔉")

    st.title("Transcribot")
    st.write("Upload an audio or video file to transcribe")
    uploaded_file = st.file_uploader("Upload File", type=["m4a", "mp3", "wav", "mp4", "mov", "avi", "mkv"])
    do_transcribe = st.button("Transcribe")

    st.divider()

    if 'transcribe_text' in st.session_state and not do_transcribe:
        display_result(st.session_state.transcribe_text, st.session_state.time_taken)

    if uploaded_file is not None and do_transcribe:

        st.session_state.transcribe_text, st.session_state.time_taken = display_transcribing(uploaded_file)
        display_result(st.session_state.transcribe_text, st.session_state.time_taken)


    settings_management()

main()
