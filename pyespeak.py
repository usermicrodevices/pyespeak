# Copyright(c) Maxim Kolosov 2011-2013 pyirrlicht@gmail.com
# http://pyespeak.sf.net
# BSD license

__version__ = pyespeak_version = '0.2'
__versionTime__ = '2013-11-26'
__author__ = 'Maxim Kolosov <pyirrlicht@gmail.com>'
__doc__ = '''
pyespeak - Python ctypes module for eSpeak.
eSpeak is a compact, multi-language, open source
text-to-speech synthesizer (http://espeak.sourceforge.net).
'''

LANG_ENCODING = 'cp1251'

ESPEAK_API_REVISION = 6

# values for 'value' in espeak_SetParameter(espeakRATE, value, 0), nominally in words-per-minute
espeakRATE_MINIMUM = 80
espeakRATE_MAXIMUM = 450
espeakRATE_NORMAL = 175

espeak_EVENT_TYPE = 0
espeakEVENT_LIST_TERMINATED = 0 # Retrieval mode: terminates the event list.
espeakEVENT_WORD = 1            # Start of word
espeakEVENT_SENTENCE = 2        # Start of sentence
espeakEVENT_MARK = 3            # Mark
espeakEVENT_PLAY = 4            # Audio element
espeakEVENT_END = 5             # End of sentence or clause
espeakEVENT_MSG_TERMINATED = 6  # End of message
espeakEVENT_PHONEME = 7         # Phoneme, if enabled in espeak_Initialize()
espeakEVENT_SAMPLERATE = 8      # internal use, set sample rate

espeak_POSITION_TYPE = 0
POS_CHARACTER = 1
POS_WORD = 2
POS_SENTENCE = 3

espeak_AUDIO_OUTPUT = 0
AUDIO_OUTPUT_PLAYBACK = 0       # PLAYBACK mode: plays the audio data, supplies events to the calling program
AUDIO_OUTPUT_RETRIEVAL = 1      # RETRIEVAL mode: supplies audio data and events to the calling program
AUDIO_OUTPUT_SYNCHRONOUS = 2    # SYNCHRONOUS mode: as RETRIEVAL but doesn't return until synthesis is completed
AUDIO_OUTPUT_SYNCH_PLAYBACK = 3 # Synchronous playback

espeak_ERROR = 0
EE_OK = 0
EE_INTERNAL_ERROR = -1
EE_BUFFER_FULL = 1
EE_NOT_FOUND = 2

espeakCHARS_AUTO  = 0
espeakCHARS_UTF8  = 1
espeakCHARS_8BIT  = 2
espeakCHARS_WCHAR = 3
espeakCHARS_16BIT = 4

espeakSSML          = 0x10
espeakPHONEMES      = 0x100
espeakENDPAUSE      = 0x1000
espeakKEEP_NAMEDATA = 0x2000

espeak_PARAMETER = 0
espeakSILENCE = 0 # internal use
espeakRATE = 1
espeakVOLUME = 2
espeakPITCH = 3
espeakRANGE = 4
espeakPUNCTUATION = 5
espeakCAPITALS = 6
espeakWORDGAP = 7
espeakOPTIONS = 8   # reserved for misc. options.  not yet used
espeakINTONATION = 9
espeakRESERVED1 = 10
espeakRESERVED2 = 11
espeakEMPHASIS = 12   # internal use
espeakLINELENGTH = 13 # internal use
espeakVOICETYPE = 14  # internal, 1=mbrola
N_SPEECH_PARAM = 15    # last enum

espeak_PUNCT_TYPE = 0
espeakPUNCT_NONE = 0
espeakPUNCT_ALL = 1
espeakPUNCT_SOME = 2

import ctypes
from sys import hexversion, platform

class FILE(ctypes.Structure):
	pass
FILE_ptr = ctypes.POINTER(FILE)
if hexversion >= 0x03000000:
	PyFile_FromFile = ctypes.pythonapi.PyFile_FromFd
	PyFile_AsFile = ctypes.pythonapi.PyObject_AsFileDescriptor
	type_str = bytes
	type_unicode = str
else:
	PyFile_FromFile = ctypes.pythonapi.PyFile_FromFile
	PyFile_AsFile = ctypes.pythonapi.PyFile_AsFile
	type_str = str
	type_unicode = unicode
PyFile_FromFile.restype = ctypes.py_object
PyFile_FromFile.argtypes = [FILE_ptr, ctypes.c_char_p, ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int, FILE_ptr)]
PyFile_AsFile.restype = FILE_ptr
PyFile_AsFile.argtypes = [ctypes.py_object]

func_type = ctypes.CFUNCTYPE

c_module = None
try:
	c_module = ctypes.CDLL('espeak_lib')
	#~ c_module = ctypes.CDLL('espeak_lib_d')
except:
	c_module = ctypes.CDLL('espeak_sapi')

class espeak_ID(ctypes.Union):
	_fields_ = [('number', ctypes.c_int),
				('name', ctypes.c_char_p),
				('string', ctypes.c_char * 8)
				]

class espeak_EVENT(ctypes.Structure):
	_fields_ = [('type', ctypes.c_int),
				('unique_identifier', ctypes.c_uint),
				('text_position', ctypes.c_int),
				('length', ctypes.c_int),
				('audio_position', ctypes.c_int),
				('sample', ctypes.c_int),
				('user_data', ctypes.c_void_p),
				('id', espeak_ID)
				]
	#~ _anonymous_ = ('id',)

class espeak_VOICE(ctypes.Structure):
	_fields_ = [('name', ctypes.c_char_p),
				('languages', ctypes.c_char_p),
				('identifier', ctypes.c_char_p),
				('gender', ctypes.c_ubyte),
				('age', ctypes.c_ubyte),
				('variant', ctypes.c_ubyte),
				('xx1', ctypes.c_ubyte),
				('score', ctypes.c_int),
				('spare', ctypes.c_void_p)
				]

# ESPEAK_API int espeak_Initialize(espeak_AUDIO_OUTPUT output, int buflength, const char *path, int options);
espeak_Initialize = func_type(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)(('espeak_Initialize', c_module))

# typedef int (t_espeak_callback)(short*, int, espeak_EVENT*);
t_espeak_callback = func_type(ctypes.c_int, ctypes.POINTER(ctypes.c_short), ctypes.c_int, ctypes.POINTER(espeak_EVENT))
#~ t_espeak_callback = func_type(ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(espeak_EVENT))
#~ t_espeak_callback = func_type(ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)

# ESPEAK_API void espeak_SetSynthCallback(t_espeak_callback* SynthCallback);
espeak_SetSynthCallback = func_type(None, t_espeak_callback)(('espeak_SetSynthCallback', c_module))

# ESPEAK_API void espeak_SetUriCallback(int (*UriCallback)(int, const char*, const char*));
UriCallback = func_type(ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)
espeak_SetUriCallback = func_type(None, UriCallback)(('espeak_SetUriCallback', c_module))

# ESPEAK_API espeak_ERROR espeak_Synth(const void *text, size_t size, unsigned int position, espeak_POSITION_TYPE position_type, unsigned int end_position, unsigned int flags, unsigned int* unique_identifier, void* user_data);
espeak_Synth = func_type(ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p)(('espeak_Synth', c_module))
#~ espeak_Synth = func_type(ctypes.c_int, ctypes.c_char_p, ctypes.c_size_t, ctypes.c_uint, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p)(('espeak_Synth', c_module))

# ESPEAK_API espeak_ERROR espeak_Synth_Mark(const void *text, size_t size, const char *index_mark, unsigned int end_position, unsigned int flags, unsigned int* unique_identifier, void* user_data);
espeak_Synth_Mark = func_type(ctypes.c_int, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p)(('espeak_Synth_Mark', c_module))

# ESPEAK_API espeak_ERROR espeak_Key(const char *key_name);
espeak_Key = func_type(ctypes.c_int, ctypes.c_char_p)(('espeak_Key', c_module))

# ESPEAK_API espeak_ERROR espeak_Char(wchar_t character);
espeak_Char = func_type(ctypes.c_int, ctypes.c_wchar)(('espeak_Char', c_module))

# ESPEAK_API espeak_ERROR espeak_SetParameter(espeak_PARAMETER parameter, int value, int relative);
espeak_SetParameter = func_type(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)(('espeak_SetParameter', c_module))

# ESPEAK_API int espeak_GetParameter(espeak_PARAMETER parameter, int current);
espeak_GetParameter = func_type(ctypes.c_int, ctypes.c_int, ctypes.c_int)(('espeak_GetParameter', c_module))

# ESPEAK_API espeak_ERROR espeak_SetPunctuationList(const wchar_t *punctlist);
espeak_SetPunctuationList = func_type(ctypes.c_int, ctypes.c_wchar_p)(('espeak_SetPunctuationList', c_module))

# ESPEAK_API void espeak_SetPhonemeTrace(int value, FILE *stream);
espeak_SetPhonemeTrace = func_type(None, ctypes.c_int, FILE_ptr)(('espeak_SetPhonemeTrace', c_module))

# ESPEAK_API void espeak_CompileDictionary(const char *path, FILE *log, int flags);
espeak_CompileDictionary = func_type(None, ctypes.c_char_p, FILE_ptr, ctypes.c_int)(('espeak_CompileDictionary', c_module))

# ESPEAK_API const espeak_VOICE **espeak_ListVoices(espeak_VOICE *voice_spec);
espeak_ListVoices = func_type(ctypes.POINTER(ctypes.POINTER(espeak_VOICE)), ctypes.POINTER(espeak_VOICE))(('espeak_ListVoices', c_module))

# ESPEAK_API espeak_ERROR espeak_SetVoiceByName(const char *name);
espeak_SetVoiceByName = func_type(ctypes.c_int, ctypes.c_char_p)(('espeak_SetVoiceByName', c_module))

# ESPEAK_API espeak_ERROR espeak_SetVoiceByProperties(espeak_VOICE *voice_spec);
espeak_SetVoiceByProperties = func_type(ctypes.c_int, ctypes.POINTER(espeak_VOICE))(('espeak_SetVoiceByProperties', c_module))

# ESPEAK_API espeak_VOICE *espeak_GetCurrentVoice(void);
espeak_GetCurrentVoice = func_type(ctypes.POINTER(espeak_VOICE))(('espeak_GetCurrentVoice', c_module))

# ESPEAK_API espeak_ERROR espeak_Cancel(void);
espeak_Cancel = func_type(ctypes.c_int)(('espeak_Cancel', c_module))

# ESPEAK_API int espeak_IsPlaying(void);
espeak_IsPlaying = func_type(ctypes.c_int)(('espeak_IsPlaying', c_module))

# ESPEAK_API espeak_ERROR espeak_Synchronize(void);
espeak_Synchronize = func_type(ctypes.c_int)(('espeak_Synchronize', c_module))

# ESPEAK_API espeak_ERROR espeak_Terminate(void);
espeak_Terminate = func_type(ctypes.c_int)(('espeak_Terminate', c_module))

# ESPEAK_API const char *espeak_Info(const char **path_data);
_espeak_Info_ = func_type(ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p))(('espeak_Info', c_module))
def espeak_Info():
	path_data = ctypes.c_char_p()
	version = _espeak_Info_(ctypes.byref(path_data))
	return (version, path_data.value)

def as_ansi(value, encoding = LANG_ENCODING):
	if hexversion >= 0x03020000:
		return bytes(value, encoding)
	else:
		return value


if __name__ == "__main__":
	#~ output = AUDIO_OUTPUT_PLAYBACK
	#~ output = AUDIO_OUTPUT_SYNCHRONOUS
	output = AUDIO_OUTPUT_SYNCH_PLAYBACK
	print('pyespeak version %s eSpeak library %s' % (pyespeak_version, repr(c_module)))
	result = espeak_Initialize(output, 0, '.', 0)
	if result == EE_INTERNAL_ERROR:
		print('ERROR Initialize eSpeak')
	else:
		print('sample rate in Hz %d' % result)
		print('eSpeak version %s' % repr(espeak_Info()))
		if output in (AUDIO_OUTPUT_SYNCHRONOUS, AUDIO_OUTPUT_SYNCH_PLAYBACK):
			def espeak_callback(wav, numsamples, events):
				'''int SynthCallback(short *wav, int numsamples, espeak_EVENT *events)
				wav:  is the speech sound data which has been produced.
					NULL indicates that the synthesis has been completed.
				numsamples: is the number of entries in wav.  This number may vary, may be less than
					the value implied by the buflength parameter given in espeak_Initialize, and may
					sometimes be zero (which does NOT indicate end of synthesis).
				events: an array of espeak_EVENT items which indicate word and sentence events, and
					also the occurance if <mark> and <audio> elements within the text.  The list of
					events is terminated by an event of type = 0.
				Callback returns: 0=continue synthesis,  1=abort synthesis'''
				# print(espeak_callback.__doc__)
				print('=== espeak_callback %s' % repr((wav, numsamples, events)))
				return 0
			SynthCallback = t_espeak_callback(espeak_callback)
			print('espeak_SetSynthCallback', espeak_SetSynthCallback(SynthCallback))
		print('espeak_SetVoiceByName %d' % espeak_SetVoiceByName('default'))
		print('espeak_Char %d' % espeak_Char(u'a'))
		#~ print('espeak_Char', espeak_Char(u'a'))
		synth_flags = espeakCHARS_AUTO | espeakPHONEMES | espeakENDPAUSE
		#~ synth_flags = espeakCHARS_8BIT | espeakPHONEMES | espeakENDPAUSE
		pytext = 'Hello world!'
		text = ctypes.create_string_buffer(pytext, len(pytext))
		print('espeak_Synth %d' % espeak_Synth(text, ctypes.sizeof(text)+1, 0, POS_CHARACTER, 0, synth_flags, None, None))
		#~ print('espeak_Synth', espeak_Synth(pytext, len(pytext)+1, 0, POS_WORD, 0, synth_flags, None, 0))
		#~ print('espeak_Synth', espeak_Synth(pytext, len(pytext)+1, 0, POS_SENTENCE, 0, synth_flags, None, 0))
		print('espeak_Synchronize %d' % espeak_Synchronize())
		print('espeak_Terminate %d' % espeak_Terminate())
