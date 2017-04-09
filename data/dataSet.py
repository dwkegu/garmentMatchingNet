import csv
import io
import os

debug = True
class dataSets:
    def __init__(self, rate=0.6):
        self._dataSets_training_input = []
        self._dataSets_training_output = []
        self._dataSets_test_input = []
        self._dataSets_test_output = []
        self.start = 0
        self.testStart = 0
        self.trainingSize = 0
        self.testSize = 0   #testset size
        rowNum = 0
        module_path = os.path.dirname(__file__)
        filename = module_path + '/data.csv'
        with open(filename, 'r') as f:
            self.tatolSize = len(f.readlines())
            self.trainingSize = int(self.tatolSize * rate)
            self.testSize = self.tatolSize - self.trainingSize
            f.seek(0, io.SEEK_SET)
            f_csv = csv.reader(f)
            for row in f_csv:
                if rowNum < self.trainingSize:
                    rowNum = rowNum + 1
                    temp_row = []
                    for i in range(len(row) - 1):
                        temp_row.append(row[i])
                    #print(temp_row, row[-1], end='\n')
                    self._dataSets_training_output.append(row[-1])
                    self._dataSets_training_input.append(temp_row)
                else:
                    temp_row = []
                    for i in range(len(row) - 1):
                        temp_row.append(row[i])
                    #print(temp_row, row[-1], end='\n')
                    self._dataSets_test_output.append(row[-1])
                    self._dataSets_test_input.append(temp_row)
        #print(self._dataSets_training_input,self._dataSets_training_output,end='\n')
        #print(self._dataSets_test_input, self._dataSets_test_output, end='\n')
        #print(self.trainingSize)

    def getTrainingNextBatch(self, batchSize=20):
        if batchSize > self.trainingSize:
            raise AttributeError('batch size is to large\n')
        if self.start + batchSize < self.trainingSize:
            tInput, tOutput = self._dataSets_training_input[self.start:self.start + batchSize], self._dataSets_training_output[
                                                                                       self.start:self.start + batchSize]
            self.start = self.start + batchSize
        else:
            tInput, tOutput = self._dataSets_training_input[self.start:], self._dataSets_training_output[self.start:]
            batchSize = batchSize - (self.trainingSize - self.start)
            self.start = 0
            ttInput = (self._dataSets_training_input[self.start:(self.start + batchSize)])
            ttOutput = (self._dataSets_training_output[self.start:(self.start + batchSize)])
            for row1, row2  in zip(ttInput, ttOutput):
                tInput.append(row1)
                tOutput.append(row2)
            self.start = self.start + batchSize
        #print(tInput,tOutput)
        return tInput, tOutput

    def getTestNextBatch(self, batchSize =20):
        if batchSize > self.testSize:
            raise AttributeError('batch size is to large\n')
        if self.testStart + batchSize < self.testSize:
            tInput, tOutput = self._dataSets_test_input[self.testStart:self.testStart + batchSize], self._dataSets_test_output[
                                                                                       self.testStart:self.testStart + batchSize]
            self.testStart = self.testStart + batchSize
        else:
            tInput, tOutput = self._dataSets_test_input[self.testStart:], self._dataSets_test_output[self.testStart:]
            batchSize = batchSize - (self.testSize - self.testStart)
            self.testStart = 0
            ttInput = (self._dataSets_test_input[self.testStart:(self.testStart + batchSize)])
            ttOutput = (self._dataSets_test_output[self.testStart:(self.testStart + batchSize)])
            for row1, row2  in zip(ttInput, ttOutput):
                tInput.append(row1)
                tOutput.append(row2)
            self.testStart = self.testStart + batchSize
        #print(tInput,tOutput)
        return tInput, tOutput

def getDataSets():
    """
    get training data include input, output:\n
    input:human body data and the garment data of all size,\n
    output:the garment that fits the human (1,2,3,4)\n
    return input, output\n
    """

    datasets = dataSets()
    return datasets


# debug info
if debug and __name__ == '__main__':
    res = getDataSets()
    #data_input, data_output = res.getTrainingNextBatch()
    for i in range(4):
        x, y = res.getTrainingNextBatch(40)
        print(len(x))
