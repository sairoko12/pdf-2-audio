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

    return "\n".join(cleaned_text)


def save_text_in_chunks(text, chunk_size=1000, output_dir='audio_parts'):
    engine = pyttsx3.init(
        driverName='nsss',
        debug=True,
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f'Directorio creado: {output_dir}')

    text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    engine.setProperty('rate', 165)
    engine.setProperty('volume', 0.9)
    engine.setProperty('voice', 'com.apple.voice.compact.es-MX.Paulina')

    audio_files = []
    for i, chunk in enumerate(text_chunks):
        temp_file = os.path.join(output_dir, f'part_{i}.wav')
        engine.save_to_file(clean_text(chunk), temp_file)
        engine.runAndWait()
        audio_files.append(temp_file)
        print(f'Guardado {temp_file}')

    return audio_files

def concatenate_audio_files(audio_files, output_file):
    combined = AudioSegment.empty()

    for file in audio_files:
        audio = AudioSegment.from_file(file)
        combined += audio

    combined.export(output_file, format='mp3')
    print(f'Archivo de audio combinado guardado como {output_file}')

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
        print(f'Eliminado {file}')

def convert_pdf_to_audio(pdf_file, audio_file_name):
    try:
        pdf_content = read_pdf_file(pdf_file)
    except Exception as error:
        print('Error on reading pdf content')
        print(error)
        return

    try:
        audio_parts = save_text_in_chunks(pdf_content)
    except Exception as error:
        print('Error on saving text to audio parts')
        print(error)
        return

    try:
        concatenate_audio_files(audio_parts, audio_file_name)
    except Exception as error:
        print('Error on concatenate audio parts')
        print(error)

    clean_temp_audios(audio_parts)


if __name__ == '__main__':
    pdf_file = 'pdfs/guia_dos.pdf'
    audio_file = 'audios/guia_dos.mp3'

    print('Start convertion...')
    convert_pdf_to_audio(pdf_file, audio_file)
    print('End of convertion')
