# AI-FitnessTrainer using YOLOv8-pose 🏋️

<p align="center">
<img src="docs/ai-trainer.jpg"
    alt="ai_trainer"
    width=550 />
</p>

In today's world, a healthy lifestyle is becoming increasingly relevant, and with it, interest in sports activities is growing. However, gaining experience and knowledge in this field can be a challenging task for many people. In this context, the application of artificial intelligence (AI) in the sports sector becomes a key element of successful training, analysis, and development of sports teams and individual athletes.

This repository provides a set of tools to help you improve your technique for the following exercises: **front squats, wide-arm push-ups, biceps push-ups, reverse push-ups**. This intelligent assistant analyzes your technique in real time, evaluates your posture using an AI model ([yolov8-pose](https://docs.ultralytics.com/tasks/pose/)) and gives you feedback on your form.

A counter for correctly completed sets and so-called attempts to perform the exercise correctly has also been added. This will help you better understand your exercise statistics.

## About the pose estimation model and the dataset used ⚙️

This project uses a trained YOLOv8m-pose model. However, you can use the weights of 2 other trained models: YOLOv8n-pose and YOLOv8s-pose located in the ```models/yolo``` and ```models/yolo2``` folders respectively, but these results are worse than YOLOv8m-pose.

These models are pose detection models that are trained on COCO-pose typed data. This dataset includes 17 keypoints. For clarity, below is a markup image.

<p align="center">
<img src="docs/coco-pose.jpg"
    alt="coco-pose"
    width=550 />
</p>

More information on the dataset can be found here: [COCO-Human-Pose](https://github.com/robertklee/COCO-Human-Pose/blob/main/README.md) and [Ultralytics: COCO-Pose Dataset](https://docs.ultralytics.com/datasets/pose/coco/).

## How to use ✔️
1. Clone repository.
```
git clone https://github.com/KKopilka/AI-FinessTrainer.git
```
2. Install the requirements.
```
pip install -r requirements.txt
```
3. Run the script.
```
python manual.py <exercise_name>
```
4. It is possible to run the project with streamlit.
```
streamlit run app/live.py 
```
5. If you want to run the project through docker. Documentation 👉 [Deploy Streamlit using Docker](https://docs.streamlit.io/deploy/tutorials/docker).
```
docker build -t streamlit .
```
```
docker-compose up -d
```

## Project roadmap 📝

- [x] Train a model for human pose estimation.

- [x] Integration of the model into the project, processing of key points.

- [x] Add exercises for major muscle groups.

- [x] Add a counter for approaches and attempts.

- [x] Run locally or through a browser (streamlit).

- [x] Launching via Docker.

## Some ideas 📝
This project is not a fully finished version, so it can still be finalized.

Here are some ideas on how to improve this project are as follows:
- Add more exercises.
- Add more statistics to the program.
- Add a web/mobile app.
- Add sound accompaniment.
- Convert the project to an .exe file.