import pickle
import numpy as np


_OBJECT_PATH = '_obj/'
_A = 'Station_Matrix_A'
_B = 'Confusion_Matrix_B'

class HMM:
    def __init__(self):

        self.pi = np.array([ 0.5, 0.5, 0, 0])  # S, B, M, E
        self.A = np.array([
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ], dtype=np.float) # Station Matrix 
        self.B = {
        } # Confusion Matrix
    
    def load_matrix(self):
        with open(_OBJECT_PATH+_A, 'rb') as fa, open(_OBJECT_PATH+_B, 'rb') as fb:
            self.A = pickle.load(fa)
            self.B = pickle.load(fb)

    def initPi(self, labels):
        self.pi = np.array([0, 0, 0, 0], dtype=np.float)
        for line in labels:
            self.pi[int(line[0])] += 1
        self.pi = self.pi/np.sum(self.pi)

    def buildA(self, labels, is_save=True):
        for line in labels:
            lens = len(line)
            for i in range(lens-1):
                self.A[int(line[i])][int(line[i+1])] += 1
        for i in range(4):
            self.A[i] = self.A[i]/np.sum(self.A[i])
        if is_save:
            with open(_OBJECT_PATH+_A, 'wb') as f:
                pickle.dump(self.A, f)
    
    def buildB(self, labels, texts, is_save=True):
        error = 0
        for label, text in zip(labels, texts):

            text = ''.join(text)
            lens = len(label)

            if lens != len(text):                
                # raise Exception('ERROR: different length in label {} and text {}'.format(lens, len(text)))
                error += 1
                continue
            
            for i in range(lens):
                if text[i] in self.B:
                    self.B[text[i]][int(label[i])] += 1
                else:
                    self.B[text[i]] = np.array([0, 0, 0, 0], dtype=np.float)
                    self.B[text[i]][int(label[i])] += 1
        print('\n* Calculate matrix finished, But {} error lines *\n'.format(error))

        for k in self.B:
            self.B[k] = (self.B[k]+1)/np.sum(self.B[k])
        if is_save:
            with open(_OBJECT_PATH+_B, 'wb') as f:
                pickle.dump(self.B, f)

    def viterbi(self, observation):
        
        def findmax(arr):
            maxcell, maxidx = arr[0], 0
            for i in range(1, len(arr)):
                if arr[i] > maxcell:
                    maxcell, maxidx = arr[i], i
            return maxidx

        res = []
        lens = len(observation)
        
        if lens == 1:
            return '0'

        char = observation[0]
        y1 = self.pi * self.B[char]
        res.append(str(findmax(y1)))
        
        for i in range(1, lens):
            char = observation[i]
            y1 = [max(self.A[i] * y1) for i in range(4)] * self.B[char]
            res.append(str(findmax(y1)))
        return ''.join(res)

