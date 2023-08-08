import speechmatics
from httpx import HTTPStatusError
import asyncio
import pyaudio
import winsound
import time

API_KEY = "pK4jrLchh4YCBrK2aKrJymAlqtdIU6BW"
LANGUAGE = "en"
CONNECTION_URL = f"wss://eu2.rt.speechmatics.com/v2/{LANGUAGE}"
DEVICE_INDEX = -1
CHUNK_SIZE = 1024


class AudioProcessor:
    def __init__(self):
        self.wave_data = bytearray()
        self.read_offset = 0

    async def read(self, chunk_size):
        while self.read_offset + chunk_size > len(self.wave_data):
            await asyncio.sleep(0.001)
        new_offset = self.read_offset + chunk_size
        data = self.wave_data[self.read_offset:new_offset]
        self.read_offset = new_offset
        return data

    def write_audio(self, data):
        self.wave_data.extend(data)
        return


audio_processor = AudioProcessor()


def stream_callback(in_data, frame_count, time_info, status):
    audio_processor.write_audio(in_data)
    return in_data, pyaudio.paContinue



p = pyaudio.PyAudio()
if DEVICE_INDEX == -1:
    DEVICE_INDEX = p.get_default_input_device_info()['index']
    device_name = p.get_default_input_device_info()['name']
    DEF_SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
    device_seen = set()
    for i in range(p.get_device_count()):
        if p.get_device_info_by_index(i)['name'] not in device_seen:
            device_seen.add(p.get_device_info_by_index(i)['name'])
            try:
                supports_input = p.is_format_supported(DEF_SAMPLE_RATE, input_device=i, input_channels=1, input_format=pyaudio.paFloat32)
            except Exception:
                supports_input = False
            if supports_input:
                print(f"-- To use << {p.get_device_info_by_index(i)['name']} >>, set DEVICE_INDEX to {i}")
    print("***\n")

SAMPLE_RATE = int(p.get_device_info_by_index(DEVICE_INDEX)['defaultSampleRate'])
device_name = p.get_device_info_by_index(DEVICE_INDEX)['name']

print(f"\nUsing << {device_name} >> which is DEVICE_INDEX {DEVICE_INDEX}")

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=DEVICE_INDEX,
                stream_callback=stream_callback
)



conn = speechmatics.models.ConnectionSettings(
    url=CONNECTION_URL,
    auth_token=API_KEY,
    generate_temp_token=True,
)



ws = speechmatics.client.WebsocketClient(conn)



conf = speechmatics.models.TranscriptionConfig(
    language=LANGUAGE,
    enable_partials=True,
    max_delay=2,
)



OBSCENE_WORDS = ['dark', 'follow', 'satellites', 'color', 'blood', 'love', 'amity', 'asus', 'macbook air']

def detect_obscene_words(transcript):
    detected_obscene_words = [word for word in OBSCENE_WORDS if word in transcript.lower()]
    return detected_obscene_words




def save_transcript_to_file(transcript, file_path):
    with open(file_path, 'a') as file:
        file.write(transcript + '\n')




def print_partial_transcript(msg):
    transcript=msg['metadata']['transcript']
    print(f"[partial] {msg['metadata']['transcript']}")



    detected_obscene_words = detect_obscene_words(transcript)
    if detected_obscene_words:
        mute_sound_for_1_second()
        print(f"Detected obscene words: {', '.join(detected_obscene_words)}")
        save_transcript_to_file(f" {detected_obscene_words}", "bad-transcript.txt")



def print_transcript(msg):
    transcript=msg['metadata']['transcript']
    print(f"[  FINAL] {msg['metadata']['transcript']}")

    detected_obscene_words = detect_obscene_words(transcript)
    if detected_obscene_words:
        print(f"Detected obscene words: {', '.join(detected_obscene_words)}")
        save_transcript_to_file(f" {detected_obscene_words}", "bad-transcript.txt")



def mute_sound_for_1_second():
    winsound.Beep(3500,1500)



ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddPartialTranscript,
    event_handler=print_partial_transcript,
)



ws.add_event_handler(
    event_name=speechmatics.models.ServerMessageType.AddTranscript,
    event_handler=print_transcript,
)



settings = speechmatics.models.AudioSettings()
settings.encoding = "pcm_f32le"
settings.sample_rate = SAMPLE_RATE
settings.chunk_size = CHUNK_SIZE

print("Starting transcription (type Ctrl-C to stop):")
try:
    ws.run_synchronously(audio_processor, conf, settings)
except KeyboardInterrupt:
    print("\nTranscription stopped.")
except HTTPStatusError as e:
    if e.response.status_code == 401:
        print('Invalid API key - Check your API_KEY at the top of the code!')
    else:
        raise e

