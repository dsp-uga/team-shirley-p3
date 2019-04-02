# CSCI-8360 Project 3: Neuron Finding
## Team-shirley
### Members 
* Marcus Hill (marcdh@uga.edu)
* Narinder Singh (narindersingh.ghumman@uga.edu)
* Jiahao Xu (jiahaoxu@uga.edu)

## Technology packages
* [keras](https://keras.io/)
* [thunder-python](https://github.com/thunder-project/thunder)
* [thunder-extraction](https://github.com/thunder-project/thunder-extraction)

## Problem overview
The problem here is one of finding neurons in a large time series calcium fluorescence dataset. The problem is fundamentally one of image segmentation. While imaging, as calcium is added, action potential gates are activated, illuminating parts of the image that contain nerurons. This forms the basis for building algorithms or training models for segmentation. A slightly more detailed problem overview can be found [here](https://github.com/dsp-uga/sp19/blob/master/projects/p3/project3.pdf).

## Data
The dataset is time-series obtained through calcium imaging. It can be found [here](gs://uga-dsp/project3). Each folder contains an imaging sample as a series of sequentially numbered image files in TIFF format. There are 28 folders in total: 19 training samples and 9 testing samples. The training labels spicfy the areas in the imaging that contain neurons. 19 training samples mean that there are 19 labels - each label specifying a set of regions in the 2-D plane - essentially drawing 'circles' around the neurons.

The complete dataset can be downloaded by running the following script:
```
$ src/getData.sh
``` 

#### Data exploration
Following are some visualization for 00.00 dataseet 

Rescaled average image            |  Label
:-------------------------:|:-------------------------:
![](https://github.com/dsp-uga/team-shirley-p3/blob/jiahao_develop/visualization/raw0000.png)  |  ![](https://github.com/dsp-uga/team-shirley-p3/blob/jiahao_develop/visualization/label0000.png)

The following animation is a visualization of the data for the ```00.00``` dataset

![](https://github.com/dsp-uga/team-shirley-p3/blob/jiahao_develop/visualization/video.gif)

## Preprocessing
Before feeding the data to the model, we implemented the median fileter and gaussian filter to the data, which could help remove some noise.

## Implementation
### NMF
The NMF implementaion codes are highly inspired by the following links and they deserve exact credits
* https://gist.github.com/freeman-lab/330183fdb0ea7f4103deddc9fae18113
* https://gist.github.com/freeman-lab/3e98ea4ccb96653c8fb085090079ce21

We can run the code by using the following command
```
$ python src/NMF/NMF.py
``` 
where all the parameters can be varied in ```src/NMF/parameters.py``` 
#### Parameters
* **baseDirectory**: the path of the directory of the data
* **datasets**: a list of datasets you are going to run (datasets name are in string format) 
* **medianFilterSize**: linear window size for the preprocessing median filter
* **gaussianFilterSigma**: the standard deviation for the Gaussian kernal for the data preprocessing
* **nmfNumComp**: k number of components to estimate per block
* **nmfMaxIter**: maximum number of algorithm iterations
* **nmfMaxSize**: maximum size of each region
* **nmfMinSize**: minimum size for each region
* **nmfPercent**: value for thresholding (higher means more thresholding)
* **nmfOverlap**: value for determining whether to merge (higher means fewer merges)
* **nmfFitChunkSize**: the size of each chunk in pixels, where a chunk is defined a subset of the image in space, including all time points
* **nmfFitPadding**: the amount by which to pad the chunks in each dimension
* **nmfMergeOverlap**: the value to merge overlapping regions in the model, by greedily comparing nearby regions and merging those that are similar to one another more than the specified value
* **nmfMergeMaxIter**: maximum number of iterations to repeat the greedy merging process
* **nmfMergeKNN**: the number of k_nearest neighbors to speed up computation.

As for the theory of the NMF, please refer to our wiki page.

## Metrics 
Instead of using a simple classification accuracy, this work is tested by the combined score from precision, recall, incluson and exclusion for each of the 9 test sets on AutoLab. (https://github.com/dsp-uga/sp19/blob/master/projects/p3/project3.pdf)
1. **Recall**: Number of matched regions divided by the number of ground-truth regions (i.e., ratio of your correct predictions to the number of actual neurons)
2. **Precision**: Number of matched regions divided by the number of your regions (i.e., ratio of your correct predictions to the total number of neurons you predicted)
3. **Inclusion**: Number of intersecting pixels divided by the number of total pixels in
the ground-truth regions (not posted on AutoLab leaderboard)
4. **Exclusion**: Number of intersecting pixels divided by the number of total pixels in
your regions (not posted on AutoLab leaderboard)

## Results
### NMF
We are tuning the NMF algorithm by varying the chunksize. Our best score for the NMF method is **3.1648**, where the average precision is **0.85672**, the average recall **0.98383**, the average inclusion is **0.56825** and the average exclusion is **0.75600**


## Reference
* https://github.com/codeneuro/neurofinder
* https://gist.github.com/freeman-lab/330183fdb0ea7f4103deddc9fae18113
* https://gist.github.com/freeman-lab/3e98ea4ccb96653c8fb085090079ce21

## License
This project is licensed under the [MIT License](https://github.com/dsp-uga/team-shirley-p3/blob/jiahao_develop/LICENSE)
