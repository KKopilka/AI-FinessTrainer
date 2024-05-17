import streamlit as st
import time
import av
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer, WebRtcMode
from streamlit_option_menu import option_menu
import sys
st.set_page_config(page_title="AI-FitnessTrainer", page_icon=":basketball:", layout="wide")
sys.path.append('./AI-Trainer')
from exercise_analyzer import ExerciseAnalyzer
from constants import _TEXT_BICEPS, _TEXT_PUSH_UP, _TEXT_REVERSE_PUSH_UP, _TEXT_SQUAT, _MAIN_PAGE_TEXT

if 'init' not in st.session_state:
    st.session_state['init'] = True
    st.session_state['exercise'] = None

def choose_exercise(exercise_key):
    st.session_state['exercise'] = exercise_key

style1 = "<style>h2 {text-align: center;}</style>"
style2 = """
    <style>
        .centered-image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        .centered-image-container img {
            max-width: 100%;
            height: auto;
        }
    </style>
"""

if st.session_state['exercise'] is None:
    st.header('Интеллектуальный помощник по фитнесу :rocket:', divider='gray')
    st.markdown(style1, unsafe_allow_html=True)
    st.subheader('Добро пожаловать в AI-FitnessTrainer!')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(style2, unsafe_allow_html=True)
        st.image('./assets/Tempo-Weight-Lifting.gif', use_column_width=True)  
    with col2:
        st.write(_MAIN_PAGE_TEXT)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.write("Просто выберите упражнение из списка, и наш искусственный интеллект начнет анализировать ваше выполнение в реальном времени 👇")
    exercise_options = {
        'Фронтальные приседания': 'front_squat',
        'Отжимания с широкой постановкой рук': 'push_up',
        'Упражнение с гантелями на бицепс': 'biceps',
        'Обратные отжимания': 'reverse_push_up'
    }
  
    cols = st.columns(len(exercise_options)) 
    for col, (key, value) in zip(cols, exercise_options.items()):
        col.button(key, on_click=choose_exercise, args=(value,))
        

else:
    if st.session_state['exercise'] == 'front_squat':
        st.header('Фронтальные приседания :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.markdown(style2, unsafe_allow_html=True)
            st.image("./assets/frontalniye-prisedaniya.jpeg", use_column_width=True)
        with right_column:
            st.write(_TEXT_SQUAT)
            analyzer = ExerciseAnalyzer('front_squat')

    elif st.session_state['exercise'] == 'push_up':
        st.header('Отжимания с широкой постановкой рук :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.markdown(style2, unsafe_allow_html=True)
            st.image("./assets/push_up.jpg", use_column_width=True)
        with right_column:
            st.write(_TEXT_PUSH_UP)
            analyzer = ExerciseAnalyzer('push_up')

    elif st.session_state['exercise'] == 'biceps':
        st.header('Упражнение с гантелями на бицепс :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.markdown(style2, unsafe_allow_html=True)
            st.image("./assets/biceps.jpg", use_column_width=True)
        with right_column:
            st.write(_TEXT_BICEPS)
            analyzer = ExerciseAnalyzer('biceps')

    elif st.session_state['exercise'] == 'reverse_push_up':
        st.header('Обратные отжимания :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.markdown(style2, unsafe_allow_html=True)
            st.image("./assets/reverse_push_up.jpg", use_column_width=True)
        with right_column:
            st.write(_TEXT_REVERSE_PUSH_UP)
            analyzer = ExerciseAnalyzer('reverse_push_up')


    def video_frame_callback(frame: av.VideoFrame):
        frame = frame.to_ndarray(format="rgb24") 
        try:
            frame, correctCount, incorrectCount = analyzer.analyze_video(frame) 
        except BaseException as b:
            print(b)
        return av.VideoFrame.from_ndarray(frame, format="rgb24")

    ctx = webrtc_streamer(
        key="example",
        video_frame_callback=video_frame_callback,
        media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000),
        async_processing=True,
        mode=WebRtcMode.SENDRECV,
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]} # Add this config

        rtc_configuration={
            "iceServers":[{"urls":"stun:stun.relay.metered.ca:80"},{"urls":"turn:global.relay.metered.ca:80","username":"9c6259b1047fc74abec2ee5d","credential":"PKbEZhnKQACcYO2f"},{"urls":"turn:global.relay.metered.ca:80?transport=tcp","username":"9c6259b1047fc74abec2ee5d","credential":"PKbEZhnKQACcYO2f"},{"urls":"turn:global.relay.metered.ca:443","username":"9c6259b1047fc74abec2ee5d","credential":"PKbEZhnKQACcYO2f"},{"urls":"turns:global.relay.metered.ca:443?transport=tcp","username":"9c6259b1047fc74abec2ee5d","credential":"PKbEZhnKQACcYO2f"}]
        },
        # out_recorder_factory=out_recorder_factory
    )
    # def out_recorder_factory() -> MediaRecorder:
    #         return MediaRecorder(output_video_file)


    if st.button('Вернуться на главную страницу'):
        st.session_state['exercise'] = None