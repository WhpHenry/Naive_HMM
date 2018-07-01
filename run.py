from model import HMM
from preprocess import load_data, label_data, segment


trainD = list(load_data('_data/msr_training.utf8'))
labelD = list(label_data(trainD))



def main():
    model = HMM()
    # model.initPi(labelD)
    # model.buildA(labelD)
    # model.buildB(labelD, trainD)
    model.load_matrix()

    sentence = '往常排队又累又急'
    seg = model.viterbi(sentence)
    print(segment(seg, sentence))

if __name__ == '__main__':
    main()