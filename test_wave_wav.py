import wave
from pyespeak import *

global f_wavfile, samples_total, samples_split_seconds, wavefile_count
file_name = 'test'
file_type = 'wav'

def OpenWavFile(path, frame_rate, sample_width):
	global f_wavfile
	f_wavfile = wave.open(path, 'wb')
	if f_wavfile:
		f_wavfile.setnchannels(1)
		if frame_rate <= 0:
			f_wavfile.setframerate(22050)
		else:
			f_wavfile.setframerate(frame_rate)
		if sample_width < 1 or sample_width > 4:
			f_wavfile.setsampwidth(2)
		else:
			f_wavfile.setsampwidth(sample_width)
		#~ f_wavfile.setnframes(100)
	else:
		print("Can't create: '%s'" % path)
		return False
	return True

def CloseWavFile():
	global f_wavfile
	if not f_wavfile:
		return
	f_wavfile.close()
	f_wavfile = None

def espeak_callback(wav, numsamples, events):
	global f_wavfile, samples_total, samples_split_seconds, wavefile_count
	if wav is None:
		CloseWavFile()
		return 0
	events_index = 0
	samples_split = 0
	samplerate = 0
	while events[events_index].type != 0:
		if events[events_index].type == espeakEVENT_SAMPLERATE:
			samplerate = events[events_index].id.number
			samples_split = samples_split_seconds * samplerate
		elif events[events_index].type == espeakEVENT_SENTENCE:
			if (samples_split > 0) or (samples_total > samples_split):
				CloseWavFile()
				samples_total = 0
				wavefile_count += 1
		events_index += 1
	if not f_wavfile:
		fname = "%s_%.2d.%s" % (file_name, wavefile_count+1, file_type)
		if not OpenWavFile(fname, samplerate, numsamples):
			return 1
	if f_wavfile and numsamples > 0:
		samples_total += numsamples
		f_wavfile.writeframes(ctypes.string_at(wav, numsamples*2))
	return 0

if __name__ == "__main__":
	global f_wavfile, samples_total, samples_split_seconds, wavefile_count
	f_wavfile = None
	samples_total = 0
	samples_split_seconds = 0
	wavefile_count = 0
	#~ output = AUDIO_OUTPUT_PLAYBACK
	output = AUDIO_OUTPUT_SYNCHRONOUS
	#~ output = AUDIO_OUTPUT_SYNCH_PLAYBACK
	print('pyespeak version %s eSpeak library %s' % (pyespeak_version, repr(c_module)))
	result = espeak_Initialize(output, 0, '.', 0)
	if result == EE_INTERNAL_ERROR:
		print('ERROR Initialize eSpeak')
	else:
		print('sample rate in Hz %d' % result)
		print('eSpeak version %s' % repr(espeak_Info()))
		if output in (AUDIO_OUTPUT_SYNCHRONOUS, AUDIO_OUTPUT_SYNCH_PLAYBACK):
			SynthCallback = t_espeak_callback(espeak_callback)
			print('espeak_SetSynthCallback', espeak_SetSynthCallback(SynthCallback))
		print('espeak_SetVoiceByName %d' % espeak_SetVoiceByName('default'))
		print('espeak_Char %d' % espeak_Char(u'a'))
		synth_flags = espeakCHARS_AUTO | espeakPHONEMES | espeakENDPAUSE
		#~ synth_flags = espeakCHARS_8BIT | espeakPHONEMES | espeakENDPAUSE
		pytext = 'Hello world!'
		text = ctypes.create_string_buffer(pytext, len(pytext))
		print('espeak_Synth %d' % espeak_Synth(text, ctypes.sizeof(text)+1, 0, POS_CHARACTER, 0, synth_flags, None, None))
		#~ print('espeak_Synth', espeak_Synth(pytext, len(pytext)+1, 0, POS_WORD, 0, synth_flags, None, 0))
		#~ print('espeak_Synth', espeak_Synth(pytext, len(pytext)+1, 0, POS_SENTENCE, 0, synth_flags, None, 0))
		print('espeak_Synchronize %d' % espeak_Synchronize())
		print('espeak_Terminate %d' % espeak_Terminate())
