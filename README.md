# Elderly-Fallers-Prediction

## Aim of project
This project aims to make a prediction model that will classify healthy elder people and fallers

## Source of project
Data were found and downloaded from Long Term Movement Monitoring Database in physionet.org

## Citation
Goldberger, A., Amaral, L., Glass, L., Hausdorff, J., Ivanov, P. C., Mark, R., ... & Stanley, H. E. (2000). PhysioBank, PhysioToolkit, and PhysioNet: Components of a new research resource for complex physiologic signals. Circulation [Online]. 101 (23), pp. e215–e220.

## Project Description
Falls is a major problem because it increases mortality and reduces life quality in the elderly and adds a substantial economic burden on healthcare systems too. Identifying elder individuals at risk and interfering on time with appropriate modalities may help in reducing falls incidence. This dataset contains demographic data from 71 elder adults (fallers and non-fallers), as well as timeseries accelerometer data during 1 minute self paced walking trial from each subject. During walking the accelerometer sensor was worn on lower back. The dataset contains two subjects in the controls (1 and 24) with too many N/A, thus we dropped these instances. Because there were also other N/A in some variables, MissForest algorithm was applied to impute missing data. Fallers were set subjects with at least one self reported fall the year before testing. Initially the goal was to make a step counter from accelerometer data and construct new gait variables from stride times. However after testing the step counter, it didn't perform the same on different testing subjects and further analysis on stride times would require that they would be accurate. Instead using the step counter, sample entropy and power spectral analysis was used on accelerometer timeseries data. The goal of using sample entropy was to test if it can addup as predictor in the machine learning models, rather than interpreting it's meaning or potential differences between fallers and non fallers.

## Project Limitations
* Sample size is small, so it is difficult for ml models to learn and train from the existing data. This may be reflected in models accuracy instability during crossvalidation.
* Year falls data were based on subjects' self reported number of falls in the previous year.
* MissForest algorithm may have biased a slightly increased accuracy in some tree based machine learning models used.
* Although some ml models result in a decent accuracy, we have no information regarding causality on the predictor features used. Specifically we cannot be confident that some of the features used, were responsible for inducing the falls or that these features changed because of the fall. Thus it is not yet known if some of the ml models trained can indeed have a practical use.
