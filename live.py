import streamlit as st
import av
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder
from exercise_analyzer import ExerciseAnalyzer
from ai_trainer.properties import *

st.title('Интеллектуальный помощник по фитнесу :rocket:')

mode = st.radio('Select Exercise', [':basketball: Front Squat', ':basketball: Push Up'], index=0)


# if st.button("Start Exercise"):
#     if mode == 'Front Squat':
#         illustrate_exercise("assets/frontalniye-prisedaniya.jpeg")
#         exercise_name = 'front_squat'
#         analyzer = ExerciseAnalyzer(exercise_name)
#     elif mode == 'Push Up':
#         # You can uncomment this line if you have an image for push-up
#         # illustrate_exercise("other_exercise_image.jpeg")
#         exercise_name = 'push_up'
#         analyzer = ExerciseAnalyzer(exercise_name)
#     else:
#         st.error("Invalid exercise name provided.")
#         st.stop()

if mode == ':basketball: Front Squat':
    if st.button("Exercise technique"):
        st.session_state.show_image = True
        st.image("assets/frontalniye-prisedaniya.jpeg", width=500)
    else:
        st.session_state.show_image = False
    # illustrate_exercise("assets/frontalniye-prisedaniya.jpeg")
    analyzer = ExerciseAnalyzer('front_squat')
elif mode == ':basketball: Push Up':
    analyzer = ExerciseAnalyzer('push_up')


def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    frame, count = analyzer.analyze_video(frame)  # Process frame
    return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return BGR frame

# def out_recorder_factory() -> MediaRecorder:
#         return MediaRecorder(output_video_file)


ctx = webrtc_streamer(
    key="example",
    video_frame_callback=video_frame_callback,
    # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
    media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False)
    # out_recorder_factory=out_recorder_factory
)
