import numpy as n
from scipy.io import wavfile
from .functions import *
def H(*args):
    return n.hstack(args)
def V(*args):
    return n.vstack(args)
def db2Amp(db_difference):
    """Receives difference in decibels, returns amplitude proportion"""
    return 10.**(db_difference/20.)
def amp2Db(amp_difference):
    """Receives amplitude proportion, returns decibel difference"""
    return 20.*n.log10(amp_difference)
def hz2Midi(self, hz_val):
    """Receives Herz value and returns midi note value"""
    return 69+12*n.log2(hz_val/440)
def midi2Hz(midi_val):
    """Receives midi note value and returns corresponding Herz frequency"""
    #return 440*n.log2((69+midi_val)/69)
    return 440*2**((midi_val-69)/12.)
def midi2HzInterval(midi_interval):
    return 2**(midi_interval/12)
def p2f(f0=220.,semitones=[0,7,7,4,7,0]):
    return [f0*2**(i/12) for i in semitones]

def normalize(vector):
    vector=vector.astype(n.float64)
    return -1+2*(vector-vector.min())/(vector.max()-vector.min())
normalize_=normalize
def normalizeRows(vector):
    """Normalize each row of a bidimensional vector to [0,1]"""
    vector=vector.astype(n.float64)
    vector=((n.subtract(self.vector.T,self.vector.min(1)) / (self.vector.max(1)-self.vector.min(1))).T)
    return vector
def write(sonic_vector,filename="sound_music_name.wav", normalize=True,samplerate=44100):
    if normalize:
        sonic_vector=normalize_(sonic_vector)
    sonic_vector_ = n.int16(sonic_vector * float(2**15-1))
    wavfile.write(filename,samplerate, sonic_vector_) # escrita do som
def mix(self,list1,list2):
    l1=len(list1); l2=len(list2)
    if l1<l2:
        sound=n.zeros(l2)
        sound+=list2
        sound[:l1]+=list1
    else:
        sound=n.zeros(l1)
        sound+=list1
        sound[:l2]+=list2
    return sound
def mixS(l1, l2=[], end=False):
    if len(l1) != 2:
        l1 = n.array((l1, l1))
    if len(l2) != 2:
        l2 = n.array((l2, l2))
    if len(l1[0]) > len(l2[0]):
        if not end:
            l2_ = H( l2, n.zeros(( 2, len(l1[0])-len(l2[0]) )) )
        else:
            l2_ = H( n.zeros(( 2, len(l1[0])-len(l2[0]) )), l2 )
        l1_ = l1
    else:
        if not end:
            l1_ = H( l1, n.zeros(( 2, len(l2[0])-len(l1[0]) )) )
        else:
            l1_ = H( n.zeros(( 2, len(l2[0])-len(l1[0]) )), l1 )
        l2_ = l2
    return l1_+l2_


