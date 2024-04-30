import streamlit as st
import av
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder
from exercise_analyzer import ExerciseAnalyzer
from ai_trainer.properties import *


st.set_page_config(layout="wide")
st.header('Интеллектуальный помощник по фитнесу :rocket:', divider='gray')

mode = st.radio('Выберите упражнение', [':basketball: Фронтальные приседания', 
                                        ':basketball: Отжимания с широкой постановкой рук',
                                        ':basketball: Упражнение с гантелями на бицепс'], index=None)

_TEXT_SQUAT = """
        *Фронтальные приседания* — это упражнение с гантелями или штангой, при котором вы опускаетесь в приседание, удерживая груз перед собой на уровне груди.
        Оно направлено на развитие силы ног, особенно квадрицепсов, ягодиц и спины. Упражнение также требует хорошей координации и равновесия, что делает его эффективным для функциональной тренировки всего тела.

        ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
            1. Ваши ноги должны быть на ширине плеч.\n
            2. Локти не дожны быть сильно опущены вниз.\n
            3. Направление коленей во время приседаний должно быть строго по направлению
               носков.
    """

_TEXT_PUSH_UP = """
        *Отжимания с широкой постановкой рук* — это вариант отжиманий, которые отлично подходят для развития силы грудных мышц и укрепления верхней части тела.
        Это упражнение также способствует улучшению стабильности и контроля над телом. При правильном выполнении оно может быть эффективным инструментом для укрепления мышц и повышения общей физической формы.

        ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
            1. Ваши руки должны располагаться на ширине больше, чем ширина плеч.\n
            2. Локти не должны быть направлены сильно в стороны.
               Старайтесь слегка отвести их назад.\n
            3. Держите спину прямо.
    """
_TEXT_BICEPS = """
        *Упражнение с гантелями на бицепс* — это эффективное упражнение на бицепсы, которое можно выполнять как стоя, так и сидя. Основная цель этого упражнения — укрепление бицепсов и улучшение формы рук.
        Упражнение выполняется с гантелями, что позволяет работать с каждой рукой отдельно, обеспечивая равномерное развитие мышц и помогая исправлять асимметрию.

        ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
            1. Ваши ноги должны быть на ширине плеч.\n
            2. При подъеме гантели не старайтесь поднять ее засчет маха руки.
               Старайте поднимать гантель именно бицепсом.\n
            3. Локти должны быть зафиксированы у тела.\n
            4. Держите спину прямо и не отводите таз вперед.
    """
def stream_data_squat():
    for word in _TEXT_SQUAT.split(" "):
        yield word + " "
        time.sleep(0.02)

def stream_data_push_up():
    for word in _TEXT_PUSH_UP.split(" "):
        yield word + " "
        time.sleep(0.02)
    
def stream_data_biceps():
    for word in _TEXT_BICEPS.split(" "):
        yield word + " "
        time.sleep(0.02)

left_column, right_column = st.columns(2)
if mode == ':basketball: Фронтальные приседания':
    with left_column:
        st.image("assets/frontalniye-prisedaniya.jpeg", width=650)
    with right_column:
        st.write_stream(stream_data_squat)
        
    analyzer = ExerciseAnalyzer('front_squat')

elif mode == ':basketball: Отжимания с широкой постановкой рук':
    with left_column:
        st.image("assets/push_up.jpg", width=650)
    with right_column:
        st.write_stream(stream_data_push_up)

    analyzer = ExerciseAnalyzer('push_up')

elif mode == ':basketball: Упражнение с гантелями на бицепс':
    with left_column:
        st.image("assets/biceps.jpg", width=650)
    with right_column:
        st.write_stream(stream_data_biceps)

    analyzer = ExerciseAnalyzer('biceps')


def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    frame, count, dirr = analyzer.analyze_video(frame)  # Process frame
    return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return BGR frame

# def out_recorder_factory() -> MediaRecorder:
#         return MediaRecorder(output_video_file)


ctx = webrtc_streamer(
    key="example",
    video_frame_callback=video_frame_callback,
    # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
    media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000)    
    # out_recorder_factory=out_recorder_factory
)
