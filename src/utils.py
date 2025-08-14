from faster_whisper import WhisperModel
import warnings
import os
import shutil
from rich.traceback import install

install()


def transcribe_audio(audio, model='turbo', language=None, initial_prompt=""):

    # Available models:
    # - turbo: Best combo of speed and accuracy
    # - large-v3: Most accurate but slower
    # - distil-large-v3: English only, highest speed
    # - Other sizes: tiny, base, small, medium, large

    warnings.simplefilter("ignore")
    
    if language in ['en', 'english'] and model in ['tiny', 'base', 'small', 'medium']:
        model = model + '.en'

    whisper_model = WhisperModel(model, download_root="models/")
    segments, info = whisper_model.transcribe(
        audio=audio, 
        word_timestamps=True, 
        language=language if language is not False else None,
        initial_prompt=initial_prompt
    )
    
    segments_list = list(segments)
    full_text = " ".join(segment.text.strip() for segment in segments_list)
    
    return {
        "text": full_text,
        "timestamps": _generate_segment_srt(segments_list),
        "timestamps_word": _generate_word_srt(segments_list)
    }


def _format_timestamp(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    int_seconds = int(seconds)
    hours, remainder = divmod(int_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    milliseconds = int((seconds - int_seconds) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def _generate_segment_srt(segments):
    """Generate SRT format for segment-level timestamps"""
    return "\n\n".join(
        f"{i}\n{_format_timestamp(segment.start)} --> {_format_timestamp(segment.end)}\n{segment.text.strip()}"
        for i, segment in enumerate(segments, 1)
    )


def _generate_word_srt(segments):
    """Generate SRT format for word-level timestamps"""
    word_counter = 1
    parts = []
    
    for segment in segments:
        if segment.words:
            for word in segment.words:
                parts.append(f"{word_counter}\n{_format_timestamp(word.start)} --> {_format_timestamp(word.end)}\n{word.word.strip()}")
                word_counter += 1
    
    return "\n\n".join(parts)

def delete_all_models(display_func):

    models_path = r"models/"
    try:
        if os.path.exists(models_path):
            shutil.rmtree(models_path)
            display_func("Successfully Deleted")

    except:
        display_func("Failed to Delete")

