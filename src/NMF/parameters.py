class Parameters:
    def __init__(self):
        self.baseDirectory = '/Users/jerryhui/Downloads/project3_neurofinder.all.test'
        self.prefix = 'neurofinder.'
        self.datasets = ['00.00']

        self.medianFilterSize = 2
        self.gaussianFilterSigma = 1

        self.nmfNumComp = 5
        self.nmfMaxIter = 20
        self.nmfMaxSize = 'full'
        self.nmfMinSize = 10
        self.nmfPercent = 99
        self.nmfOverlap = 0.1

        self.nmfFitChunkSize = 32
        self.nmfFitPadding = 25

        self.nmfMergeOverlap = 0.1
        self.nmfMergeMaxIter = 20
        self.nmfMergeKNN = 1