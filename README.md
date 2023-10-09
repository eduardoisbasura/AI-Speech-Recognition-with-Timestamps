# [Speech-Recognition-using-WhisperAI](https://github.com/eduardoisbasura/Speech-Recognition-using-WhisperAI)

Speech-Recognition-using-WhisperAI is a Python script utilizing [Whisper](https://github.com/openai/whisper) and [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) to automatically transcribe and output a .TextGrid file with timestamps of each word from the start and the end of each word. Supports any language model that Whisper has.

## Installation

### First Installation
Requirements:
- `python3` (version higher or equal to 3.7, at least 3.9 is recommended)
- `ffmpeg` (see instructions for installation on the [whisper repository](https://github.com/openai/whisper))

Installation of `whisper-timestamped` with pip:

```
pip3 install git+https://github.com/linto-ai/whisper-timestamped
```
or clone repository and running installation
```
git clone https://github.com/linto-ai/whisper-timestamped
cd whisper-timestamped/
python3 setup.py install
```

#### [Additional Packages that might be needed (Depends on usage)](https://github.com/linto-ai/whisper-timestamped#additional-packages-that-might-be-needed)

## Usage
### Python

In Python, you can use the function `whisper_timestamped.transcribe()`, which is similar to the function `whisper.transcribe()`:
```python
import whisper_timestamped
help(whisper_timestamped.transcribe)
```
The main difference with `whisper.transcribe()` is that the output will include a key `"words"` for all segments, with the word start and end position. Note that the word will include punctuation. See the example [below](#example-output).

Besides, the default decoding options are different to favour efficient decoding (greedy decoding instead of beam search, and no temperature sampling fallback). To have same default as in `whisper`, use ```beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)```.

There are also additional options related to word alignement.

In general, if you import `whisper_timestamped` instead of `whisper` in your Python script and use `transcribe(model, ...)` instead of `model.transcribe(...)`, it should do the job:
```
import whisper_timestamped as whisper

audio = whisper.load_audio("AUDIO.wav")

model = whisper.load_model("tiny", device="cpu")

result = whisper.transcribe(model, audio, language="fr")

import json
print(json.dumps(result, indent = 2, ensure_ascii = False))
```

Note that you can use a finetuned Whisper model from HuggingFace or a local folder by using the `load_model` method of `whisper_timestamped`. For instance, if you want to use [whisper-large-v2-nob](https://huggingface.co/NbAiLab/whisper-large-v2-nob), you can simply do the following:
```
import whisper_timestamped as whisper

model = whisper.load_model("NbAiLab/whisper-large-v2-nob", device="cpu")

# ...
```

### Command line

You can also use `whisper_timestamped` on the command line, similarly to `whisper`. See help with:
```bash
whisper_timestamped --help
```

The main differences with `whisper` CLI are:
* Output files:
  * The output JSON contains word timestamps and confidence scores. See example [below](#example-output).
  * There is an additional CSV output format.
  * For SRT, VTT, TSV formats, there will be additional files saved with word timestamps.
* Some default options are different:
  * By default, no output folder is set: Use `--output_dir .` for Whisper default.
  * By default, there is no verbose: Use `--verbose True` for Whisper default.
  * By default, beam search decoding and temperature sampling fallback are disabled, to favour an efficient decoding.
    To set the same as Whisper default, you can use `--accurate` (which is an alias for ```--beam_size 5 --temperature_increment_on_fallback 0.2 --best_of 5```).
* There are some additional specific options:
  <!-- * `--efficient` to use a faster greedy decoding (without beam search neither several sampling at each step),
  which enables a special path where word timestamps are computed on the fly (no need to run inference twice).
  Note that transcription results might be significantly worse on challenging audios with this option. -->
  * `--compute_confidence` to enable/disable the computation of confidence scores for each word.
  * `--punctuations_with_words` to decide whether punctuation marks should be included or not with preceding words.

An example command to process several files using the `tiny` model and output the results in the current folder, as would be done by default with whisper, is as follows:
```
whisper_timestamped audio1.flac audio2.mp3 audio3.wav --model tiny --output_dir .
```

Note that you can use a fine-tuned Whisper model from HuggingFace or a local folder. For instance, if you want to use the [whisper-large-v2-nob](https://huggingface.co/NbAiLab/whisper-large-v2-nob) model, you can simply do the following:
```
whisper_timestamped --model NbAiLab/whisper-large-v2-nob <...>
```

### Plot of word alignment

Note that you can use the `plot_word_alignment` option of the `whisper_timestamped.transcribe()` Python function or the `--plot` option of the `whisper_timestamped` CLI to see the word alignment for each segment.

![Example alignement](figs/example_alignement_plot.png)

* The upper plot represents the transformation of cross-attention weights used for alignment with Dynamic Time Warping. The abscissa represents time, and the ordinate represents the predicted tokens, with special timestamp tokens at the beginning and end, and (sub)words and punctuation in the middle.
* The lower plot is an MFCC representation of the input signal (features used by Whisper, based on Mel-frequency cepstrum).
* The vertical dotted red lines show where the word boundaries are found (with punctuation marks "glued" to the previous word).

### Example output

Here is an example output of the `whisper_timestamped.transcribe()` function, which can be viewed by using the CLI:
```bash
whisper_timestamped AUDIO_FILE.wav --model tiny --language fr
```
```json
{
  "text": " Bonjour! Est-ce que vous allez bien?",
  "segments": [
    {
      "id": 0,
      "seek": 0,
      "start": 0.5,
      "end": 1.2,
      "text": " Bonjour!",
      "tokens": [ 25431, 2298 ],
      "temperature": 0.0,
      "avg_logprob": -0.6674491882324218,
      "compression_ratio": 0.8181818181818182,
      "no_speech_prob": 0.10241222381591797,
      "confidence": 0.51,
      "words": [
        {
          "text": "Bonjour!",
          "start": 0.5,
          "end": 1.2,
          "confidence": 0.51
        }
      ]
    },
    {
      "id": 1,
      "seek": 200,
      "start": 2.02,
      "end": 4.48,
      "text": " Est-ce que vous allez bien?",
      "tokens": [ 50364, 4410, 12, 384, 631, 2630, 18146, 3610, 2506, 50464 ],
      "temperature": 0.0,
      "avg_logprob": -0.43492694334550336,
      "compression_ratio": 0.7714285714285715,
      "no_speech_prob": 0.06502953916788101,
      "confidence": 0.595,
      "words": [
        {
          "text": "Est-ce",
          "start": 2.02,
          "end": 3.78,
          "confidence": 0.441
        },
        {
          "text": "que",
          "start": 3.78,
          "end": 3.84,
          "confidence": 0.948
        },
        {
          "text": "vous",
          "start": 3.84,
          "end": 4.0,
          "confidence": 0.935
        },
        {
          "text": "allez",
          "start": 4.0,
          "end": 4.14,
          "confidence": 0.347
        },
        {
          "text": "bien?",
          "start": 4.14,
          "end": 4.48,
          "confidence": 0.998
        }
      ]
    }
  ],
  "language": "fr"
}
```

### Options that may improve results

Here are some options that are not enabled by default but might improve results.

#### Accurate Whisper transcription

As mentioned earlier, some decoding options are disabled by default to offer better efficiency. However, this can impact the quality of the transcription. To run with the options that have the best chance of providing a good transcription, use the following options.
* In Python:
```python
results = whisper_timestamped.transcribe(model, audio, beam_size=5, best_of=5, temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0), ...)
```
* On the command line:
```bash
whisper_timestamped --accurate ...
```

#### Running Voice Activity Detection (VAD) before sending to Whisper

Whisper models can "hallucinate" text when given a segment without speech. This can be avoided by running VAD and gluing speech segments together before transcribing with the Whisper model. This is possible with `whisper-timestamped`.
* In Python:
```python
results = whisper_timestamped.transcribe(model, audio, vad=True, ...)
```
* On the command line:
```bash
whisper_timestamped --vad True ...
```

#### Detecting disfluencies

Whisper models tend to remove speech disfluencies (filler words, hesitations, repetitions, etc.). Without precautions, the disfluencies that are not transcribed will affect the timestamp of the following word: the timestamp of the beginning of the word will actually be the timestamp of the beginning of the disfluencies. `whisper-timestamped` can have some heuristics to avoid this.
* In Python:
```python
results = whisper_timestamped.transcribe(model, audio, detect_disfluencies=True, ...)
```
* On the command line:
```bash
whisper_timestamped --detect_disfluencies True ...
```
**Important:** Note that when using these options, possible disfluencies will appear in the transcription as a special "`[*]`" word.


## Acknowlegment
* [whisper](https://github.com/openai/whisper): Whisper speech recognition (License MIT).
* [dtw-python](https://pypi.org/project/dtw-python): Dynamic Time Warping (License GPL v3).
* [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped/tree/master): Multilingual Automatic Speech Recognition (License AGPL-3.0).