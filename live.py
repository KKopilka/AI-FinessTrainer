import streamlit as st
import av
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder
from exercise_analyzer import ExerciseAnalyzer

st.title('Fitness Intelligent Assistant')

mode = st.radio('Select Exercise', ['Front Squat', 'Push Up'], index=0)

if mode == 'Front Squat':
    analyzer = ExerciseAnalyzer('front_squat')
elif mode == 'Push Up':
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
    media_stream_constraints={"video": {"width": {'min':800, 'ideal':650}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False)
    # out_recorder_factory=out_recorder_factory
)
