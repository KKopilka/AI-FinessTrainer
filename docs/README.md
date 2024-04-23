# Less Pain, More Gain. Lift Weights With Your AI Trainer 🏋️📈

[Read complete Medium article](https://medium.com/@loboateresa/less-pain-more-gain-3737fe287079)

<p align="center">
<img src="assets/Tempo-Weight-Lifting.gif"
    alt="ai_trainer"
    width=550 />
</p>

## 🪧 Description

Weightlifting is a popular form of exercise that can help you lose fat, increase your strength and muscle tone, and improve your bone density. You don't have to be a bodybuilder or professional athlete to reap the benefits of weightlifting, but you do need to be aware that **if done incorrectly, weightlifting carries a risk of injury, especially if you don't use the correct form.**

This repository presents a set of tools to help you improve your weightlifting form. It does so by analyzing a video of your workout, estimating your pose with a AI model ([mediapipe-blazepose](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)) and giving you feedback on your form. 

Although the repository is designed to be used with any weightlifting exercise, it currently only supports the front squat exercise. However we are working on adding more exercises to the repository. See [Project Roadmap](#-project-roadmap) for more information.

## 📝 Table of Contents
- [Less Pain, More Gain. Lift Weights With Your AI Trainer 🏋️📈](#less-pain-more-gain-lift-weights-with-your-ai-trainer-️)
  - [🪧 Description](#-description)
  - [📝 Table of Contents](#-table-of-contents)
  - [🚀 Usage](#-usage)
  - [⚙️ About The Pose Estimation Model](#️-about-the-pose-estimation-model)
  - [🩺 Project Roadmap](#-project-roadmap)
  - [👥  Acknowledgements](#--acknowledgements)

## 🚀 Usage
1. Clone this repository.
```
git clone https://github.com/LoboaTeresa/AI-Trainer.git
```
2. Install the requirements.
```
pip install -r requirements.txt
```
3. Run the script 
```
python3 main.py --input_video <input_video>
```

For more information, check out the [documentation](docs/tutorial_front_squat.ipynb).

## ⚙️ About The Pose Estimation Model

For this project we use the Mediapipe Blazepose full model. This model is a pose detection model that infers 33 3D landmarks or keypoints on the full body (ckeck figure below). It is based on the BlazePose paper, which you can find [here](https://arxiv.org/abs/2006.10204).


<p align="center">
<img src="assets/kp_format.png"
    alt="kps_format"
    width=550 />
</p>

The specifications of the model are gathered in the [model card](docs/Model_Card_BlazePose_GHUM_3D.pdf).

## 🩺 Project Roadmap
[Back to Top](#️-less-pain-more-gain-lift-weights-with-your-ai-trainer-️️)

Although this repository is designed to be used with any weightlifting exercise, it currently only supports the front squat exercise. However we are working on adding more exercises to the repository.

Some ideas on how to improve this project are:
- [ ] Add more exercises. E.g. deadlift, bench press, etc.
- [ ] Add automatic rep counting.
- [ ] Add exercise classification/identification.
- [ ] Add a web/mobile app to make it more user friendly.
- [ ] Analyze the the position of the barbell.

## 👥  Acknowledgements
[Back to Top](#️-less-pain-more-gain-lift-weights-with-your-ai-trainer-️️)

I would like to thank [Sngular](https://ai.sngular.com/) ([Github](https://github.com/sngular)) for the green space they gave me to develop this project. I would also like to thank my college (and unofficial mentor), [Mate](https://www.linkedin.com/in/aimatesanz/), for some code snippets as well as his motivation and knowledge pills he shares daily. Love working with you, mate! (pun intended😉). Check out [his Github](https://github.com/Matesanz), he has some amazing CV and MLOps projects.
