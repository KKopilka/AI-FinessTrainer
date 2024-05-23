import streamlit as st
import time
import av
from streamlit_webrtc import VideoHTMLAttributes, WebRtcMode, webrtc_streamer
# from streamlit_option_menu import option_menu
import sys
import cv2
st.set_page_config(page_title="AI-FitnessTrainer", page_icon=":basketball:", layout="wide")
import numpy as np

sys.path.append('/streamlit')
from exercise_analyzer import ExerciseAnalyzer
from constants import _TEXT_BICEPS, _TEXT_PUSH_UP, _TEXT_REVERSE_PUSH_UP, _TEXT_SQUAT

def video_frame_callback(frame: av.VideoFrame):
    fr = frame.to_ndarray(format="rgb24") 
    try:
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
        frame, correctCount, incorrectCount = analyzer.analyze_video(fr) 
        fr = frame
        
        # print()
    except Exception as err:
        print(f"Error while proccessing frame. {err}")
        frame = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY)
        frame = cv2.Canny(frame,100,200)
        fr = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    try:
        out = av.VideoFrame.from_ndarray(fr, format="rgb24")
    except Exception as err:
        print(f"Error on output")
        return av.VideoFrame.from_ndarray(np.zeros((420,420,3), np.uint8), format="rgb24")
    #     #frame = cv2.Canny(frame,100,200)
    #     #frame, correctCount, incorrectCount = analyzer.analyze_video(frame) 
    # except Exception as b:
    #     print("Error while proccessing frame", b)

    return out

if 'init' not in st.session_state:
    st.session_state['init'] = True
    st.session_state['exercise'] = None

def choose_exercise(exercise_key):
    st.session_state['exercise'] = exercise_key

if st.session_state['exercise'] is None:
    st.header('Интеллектуальный помощник по фитнесу :rocket:')
    st.subheader('Добро пожаловать в AI-FitnessTrainer!')
    st.write('''
    В этом приложении вы можете выбрать различные упражнения для анализа вашей техники и получения обратной связи в реальном времени.
    Просто выберите упражнение из списка, и наш искусственный интеллект начнет анализировать ваше выполнение в реальном времени.
    ''')

    exercise_options = {
        'Фронтальные приседания': 'front_squat',
        'Отжимания с широкой постановкой рук': 'push_up',
        'Упражнение с гантелями на бицепс': 'biceps',
        'Обратные отжимания': 'reverse_push_up'
    }

    for key, value in exercise_options.items():
        st.button(key, on_click=choose_exercise, args=(value,))

else:
    left_column, right_column = st.columns(2)

    if st.session_state['exercise'] == 'front_squat':
        with left_column:
            st.header('Фронтальные приседания')
            st.image("./assets/frontalniye-prisedaniya.jpeg", width=400)
        with right_column:
            st.write(_TEXT_SQUAT)
            # st.write_stream(stream_data(_TEXT_SQUAT))
            analyzer = ExerciseAnalyzer('front_squat')

    elif st.session_state['exercise'] == 'push_up':
        with left_column:
            st.header('Отжимания с широкой постановкой рук')
            st.image("./assets/push_up.jpg", width=400)
        with right_column:
            # st.write_stream(stream_data(_TEXT_PUSH_UP))
            st.write(_TEXT_PUSH_UP)
            analyzer = ExerciseAnalyzer('push_up')

    elif st.session_state['exercise'] == 'biceps':
        with left_column:
            st.header('Упражнение с гантелями на бицепс')
            st.image("./assets/biceps.jpg", width=400)
        with right_column:
            # st.write_stream(stream_data(_TEXT_BICEPS))
            st.write(_TEXT_BICEPS)
            analyzer = ExerciseAnalyzer('biceps')

    elif st.session_state['exercise'] == 'reverse_push_up':
        with left_column:
            st.header('Обратные отжимания')
            st.image("./assets/reverse_push_up.jpg", width=450)
        with right_column:
            # st.write_stream(_TEXT_REVERSE_PUSH_UP)
            st.write(_TEXT_REVERSE_PUSH_UP)
            analyzer = ExerciseAnalyzer('reverse_push_up')


    if st.button('Вернуться на главную страницу'):
        st.session_state['exercise'] = None

    try:
        ctx = webrtc_streamer(
            key="example",
            video_frame_callback=video_frame_callback,
            # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
            media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
            video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000),
            async_processing=True,
            mode=WebRtcMode.SENDRECV,
            rtc_configuration={
                "iceServers":[{"urls":"stun:stun.relay.metered.ca:80"},{"urls":"turn:global.relay.metered.ca:80","username":"fcb6fee592afde5c56516e8e","credential":"fS7LFEKdFz8vsRJz"},{"urls":"turn:global.relay.metered.ca:80?transport=tcp","username":"fcb6fee592afde5c56516e8e","credential":"fS7LFEKdFz8vsRJz"},{"urls":"turn:global.relay.metered.ca:443","username":"fcb6fee592afde5c56516e8e","credential":"fS7LFEKdFz8vsRJz"},{"urls":"turns:global.relay.metered.ca:443?transport=tcp","username":"fcb6fee592afde5c56516e8e","credential":"fS7LFEKdFz8vsRJz"}]
            },
            # out_recorder_factory=out_recorder_factory
        )
    except Exception as err:
        print("Error on webrtc_streamer init. Error: ", err)

    # def out_recorder_factory() -> MediaRecorder:
    #         return MediaRecorder(output_video_file)
