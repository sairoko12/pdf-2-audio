import os
import re

import PyPDF2
import pyttsx3
from pydub import AudioSegment


def clean_text(text):
    text = re.sub(r'[^\w\s\.,;:!?()\[\]{}\'"áéíóúÁÉÍÓÚñÑüÜ]', '', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        if re.match(r'^\d+\.\s', line.strip()):
            cleaned_lines.append(line.strip())
        elif re.match(r'^•\s', line.strip()) or re.match(r'^-\s', line.strip()):
            continue
        else:
            cleaned_lines.append(line.strip())

    cleaned_text = []
    for line in cleaned_lines:
        if re.match(r'^[\W_]+$', line):
            continue
        cleaned_text.append(line)

    return '\n'.join(cleaned_text)


def save_text_in_chunks(
    text,
    chunk_size=1000,
    output_dir='audio_parts',
    language='default',
    rate=165,
    volume=0.9,
):
    engine = pyttsx3.init(
        driverName='nsss',
        debug=True,
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f'Directory created: {output_dir}')

    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    if language != 'default':
        voices = engine.getProperty('voices')
        for voice in voices:
            if language in voice.languages:
                engine.setProperty('voice', voice.id)
                break

    audio_files = []
    for i, chunk in enumerate(text_chunks):
        temp_file = os.path.join(output_dir, f'part_{i}.wav')
        engine.save_to_file(clean_text(chunk), temp_file)
        engine.runAndWait()
        audio_files.append(temp_file)
        print(f'Saved: {temp_file}')

    return audio_files

def concatenate_audio_files(audio_files, output_file):
    combined = AudioSegment.empty()

    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined += audio

    combined.export(output_file, format='mp3')
    print(f'Combined audio file saved as: {output_file}')

def read_pdf_file(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()

        return text

def clean_temp_audios(audio_files):
    for file in audio_files:
        os.remove(file)
        print(f'Removed: {file}')

def convert_pdf_to_audio(
    pdf_file,
    output_file_name,
    language='default',
    rate=165,
    volume=0.9,
):
    try:
        pdf_content = read_pdf_file(pdf_file)
    except Exception as error:
        print('Error reading PDF content')
        print(error)
        return

    try:
        audio_parts = save_text_in_chunks(
            text=pdf_content,
            language=language,
            rate=rate,
            volume=volume,
        )
    except Exception as error:
        print('Error saving text to audio parts')
        print(error)
        return

    try:
        concatenate_audio_files(audio_parts, output_file_name)
    except Exception as error:
        print('Error concatenating audio parts')
        print(error)

    clean_temp_audios(audio_parts)


if __name__ == '__main__':
    pdf_file = 'path/to/pdf_file.pdf'
    audio_file = 'path/to/audio_output.mp3'

    print('Starting conversion...')
    convert_pdf_to_audio(pdf_file, audio_file)
    print('Conversion completed.')
