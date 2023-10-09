import whisper_timestamped as whisper
import tgt
import json
import glob
import wave

audio_file = glob.glob("FOLDER TO AUDIO FILES HERE")

for audio_file in audio_file:
    try:
        print(f"\n\nProcessing {audio_file}...\n\n")

        audio = whisper.load_audio(audio_file)

        model = whisper.load_model("NAME OF MODEL HERE")

        result = whisper.transcribe(model, audio,)

        # Parse the JSON
        data = json.loads(json.dumps(result))

        # Access the "words" key within the "segments" list
        words = data['segments'][0]['words']

        # Iterate over the words and extract the information
        for word in words:
            text = word['text']
            start = word['start']
            end = word['end']
            confidence = word['confidence']

            #remove capitalization
            text = text.lower()
            #remove periods
            text = text.replace('.', '')

            print(f"Word: {text}\tStart: {start}\tEnd: {end}\tConfidence: {confidence}")

        # Create a TextGrid object
        tg = tgt.core.TextGrid()
        tg.name = audio_file
        tier = tgt.core.IntervalTier(name='inst')
        for word in words:
            tier.add_interval(tgt.core.Interval(word['start'], word['end'], word['text']))
        
        # add final interval from end of last word to end of audio
        final_start = words[-1]['end']

        wf = wave.open(audio_file, 'rb')
        final_end = wf.getnframes() / wf.getframerate()
        wf.close()

        if final_start > final_end:
            final_start = final_end

        if final_start == final_end:
            final_end = final_start + 0.01

        tier.add_interval(tgt.core.Interval(final_start, final_end, ''))
        tg.add_tier(tier)

        audio_file = audio_file.split('.')[0]
        tgt.io.write_to_file(tg, f'{audio_file}.TextGrid', format='long')

        print(f"\n\nFinished processing {audio_file}.\n\n")

    except Exception as e:
        # handle the exception here
        print(f'Error occurred: {e}')

print("Done!")