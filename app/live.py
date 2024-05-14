# # import streamlit as st
# # import av
# # from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
# # from streamlit_option_menu import option_menu
# # from aiortc.contrib.media import MediaRecorder
# # import sys
# # sys.path.append('\AI-Trainer')
# # from exercise_analyzer import ExerciseAnalyzer
# # from constants import _TEXT_BICEPS, _TEXT_PUSH_UP, _TEXT_REVERSE_PUSH_UP, _TEXT_SQUAT
# # from ai_trainer.properties import *

# # st.set_page_config(page_title="AI-FitnessTrainer", page_icon=":basketball:",layout="wide")
# # st.header('Интеллектуальный помощник по фитнесу :rocket:', divider='gray')

# # def stream_data_squat():
# #     for word in _TEXT_SQUAT.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)

# # def stream_data_push_up():
# #     for word in _TEXT_PUSH_UP.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)
    
# # def stream_data_biceps():
# #     for word in _TEXT_BICEPS.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)

# # def stream_data_reverse_push_up():
# #     for word in _TEXT_REVERSE_PUSH_UP.split(" "):
# #         yield word + " "
# #         time.sleep(0.02)

# # with st.sidebar:
# #     # mode = st.radio('Выберите упражнение', [':basketball: Фронтальные приседания', 
# #     #                                     ':basketball: Отжимания с широкой постановкой рук',
# #     #                                     ':basketball: Упражнение с гантелями на бицепс',
# #     #                                     ':basketball: Обратные отжимания'], index=None)
# #     mode = option_menu('Выберите упражнение', 
# #                                     ['Фронтальные приседания', 
# #                                     'Отжимания с широкой постановкой рук',
# #                                     'Упражнение с гантелями на бицепс',
# #                                     'Обратные отжимания'], 
# #                                     menu_icon='rocket-takeoff',
# #                                     icons=['arrow-right-short', 'arrow-right-short', 'arrow-right-short', 'arrow-right-short'],
# #                                     # styles={
# #                                     #     "container": {"padding": "0!important", "background-color": "#fafafa"}
# #                                     #     "icon": {"color": "orange", "font-size": "25px"}, 
# #                                     #     "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
# #                                     #     "nav-link-selected": {"background-color": "green"},
# #                                     # },
# #                                     default_index=1)

# # left_column, right_column = st.columns(2)

# # if mode == 'Фронтальные приседания':
# #     with left_column:
# #         st.image("./assets/frontalniye-prisedaniya.jpeg", width=400)
# #     with right_column:
# #         # st.write_stream(stream_data_squat)
# #         st.write(_TEXT_SQUAT)
        
# #     analyzer = ExerciseAnalyzer('front_squat')

# # elif mode == 'Отжимания с широкой постановкой рук':
# #     with left_column:
# #         st.image("./assets/push_up.jpg", width=400)
# #     with right_column:
# #         # st.write_stream(stream_data_push_up)
# #         st.write(_TEXT_PUSH_UP)

# #     analyzer = ExerciseAnalyzer('push_up')

# # elif mode == 'Упражнение с гантелями на бицепс':
# #     with left_column:
# #         st.image("./assets/biceps.jpg", width=400)
# #     with right_column:
# #         # st.write_stream(stream_data_biceps)
# #         st.write(_TEXT_BICEPS)

# #     analyzer = ExerciseAnalyzer('biceps')

# # elif mode == 'Обратные отжимания':
# #     with left_column:
# #         st.image("./assets/reverse_push_up.jpg", width=450)
# #     with right_column:
# #         # st.write_stream(stream_data_reverse_push_up)
# #         st.write(_TEXT_REVERSE_PUSH_UP)

# #     analyzer = ExerciseAnalyzer('reverse_push_up')


# # def video_frame_callback(frame: av.VideoFrame):
# #     frame = frame.to_ndarray(format="rgb24") 
# #     try:
# #         frame, correctCount, incorrectCount = analyzer.analyze_video(frame) 
# #     except BaseException as b:
# #         print(b)
# #     return av.VideoFrame.from_ndarray(frame, format="rgb24")

# # # def out_recorder_factory() -> MediaRecorder:
# # #         return MediaRecorder(output_video_file)


# # ctx = webrtc_streamer(
# #     key="example",
# #     video_frame_callback=video_frame_callback,
# #     # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
# #     media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
# #     video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000)    
# #     # out_recorder_factory=out_recorder_factory
# # )

import streamlit as st
import time
import av
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from streamlit_option_menu import option_menu
import sys
st.set_page_config(page_title="AI-FitnessTrainer", page_icon=":basketball:", layout="wide")
sys.path.append('D:\AI-Trainer')
from exercise_analyzer import ExerciseAnalyzer
from constants import _TEXT_BICEPS, _TEXT_PUSH_UP, _TEXT_REVERSE_PUSH_UP, _TEXT_SQUAT

if 'init' not in st.session_state:
    st.session_state['init'] = True
    st.session_state['exercise'] = None

def choose_exercise(exercise_key):
    st.session_state['exercise'] = exercise_key

if st.session_state['exercise'] is None:
    st.header('Интеллектуальный помощник по фитнесу :rocket:', divider='gray')
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

    cols = st.columns(len(exercise_options))
    for col, (key, value) in zip(cols, exercise_options.items()):
        col.button(key, on_click=choose_exercise, args=(value,))

else:
    if st.session_state['exercise'] == 'front_squat':
        st.header('Фронтальные приседания :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.image("./assets/frontalniye-prisedaniya.jpeg", use_column_width=True)
        with right_column:
            st.write(_TEXT_SQUAT)
            analyzer = ExerciseAnalyzer('front_squat')

    elif st.session_state['exercise'] == 'push_up':
        st.header('Отжимания с широкой постановкой рук :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.image("./assets/push_up.jpg", use_column_width=True)
        with right_column:
            st.write(_TEXT_PUSH_UP)
            analyzer = ExerciseAnalyzer('push_up')

    elif st.session_state['exercise'] == 'biceps':
        st.header('Упражнение с гантелями на бицепс :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
            st.image("./assets/biceps.jpg", use_column_width=True)
        with right_column:
            st.write(_TEXT_BICEPS)
            analyzer = ExerciseAnalyzer('biceps')

    elif st.session_state['exercise'] == 'reverse_push_up':
        st.header('Обратные отжимания :rocket:', divider='gray')
        left_column, right_column = st.columns(2, gap='medium')
        with left_column:
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
        # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
        media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000)    
        # out_recorder_factory=out_recorder_factory
    )
    # def out_recorder_factory() -> MediaRecorder:
    #         return MediaRecorder(output_video_file)


    if st.button('Вернуться на главную страницу'):
        st.session_state['exercise'] = None



# import streamlit as st
# import av
# from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
# from aiortc.contrib.media import MediaRecorder
# import sys
# sys.path.append('\AI-Trainer')
# from exercise_analyzer import ExerciseAnalyzer

# from ai_trainer.properties import *


# st.set_page_config(layout="wide")
# st.header('Интеллектуальный помощник по фитнесу :rocket:', divider='gray')

# mode = st.radio('Выберите упражнение', [':basketball: Фронтальные приседания', 
#                                         ':basketball: Отжимания с широкой постановкой рук',
#                                         ':basketball: Упражнение с гантелями на бицепс',
#                                         ':basketball: Обратные отжимания'], index=None)

# _TEXT_SQUAT = """
#         *Фронтальные приседания* — это упражнение с гантелями или штангой, при котором вы опускаетесь в приседание, удерживая груз перед собой на уровне груди.
#         Оно направлено на развитие силы ног, особенно квадрицепсов, ягодиц и спины. Упражнение также требует хорошей координации и равновесия, что делает его эффективным для функциональной тренировки всего тела.

#         ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
#             1. Ваши ноги должны быть на ширине плеч.\n
#             2. Локти не дожны быть сильно опущены вниз.\n
#             3. Направление коленей во время приседаний должно быть строго по направлению
#                носков.
#     """

# _TEXT_PUSH_UP = """
#         *Отжимания с широкой постановкой рук* — это вариант отжиманий, которые отлично подходят для развития силы грудных мышц и укрепления верхней части тела.
#         Это упражнение также способствует улучшению стабильности и контроля над телом. При правильном выполнении оно может быть эффективным инструментом для укрепления мышц и повышения общей физической формы.

#         ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
#             1. Ваши руки должны располагаться на ширине больше, чем ширина плеч.\n
#             2. Локти не должны быть направлены сильно в стороны.
#                Старайтесь слегка отвести их назад.\n
#             3. Держите спину прямо.
#     """

# _TEXT_BICEPS = """
#         *Упражнение с гантелями на бицепс* — это эффективное упражнение на бицепсы, которое можно выполнять как стоя, так и сидя. Основная цель этого упражнения — укрепление бицепсов и улучшение формы рук.
#         Упражнение выполняется с гантелями, что позволяет работать с каждой рукой отдельно, обеспечивая равномерное развитие мышц и помогая исправлять асимметрию.

#         ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
#             1. Ваши ноги должны быть на ширине плеч.\n
#             2. При подъеме гантели не старайтесь поднять ее засчет маха руки.
#                Старайте поднимать гантель именно бицепсом.\n
#             3. Локти должны быть зафиксированы у тела.\n
#             4. Держите спину прямо и не отводите таз вперед.
#     """

# _TEXT_REVERSE_PUSH_UP = """
#         *Обратные отжимания* — это не только отличное упражнение для формирования выразительных плеч, но и замечательный способ укрепить верхнюю часть спины,
#         сделать её более подтянутой и снизить риск возникновения болей в плечевых суставах.
#         Упражнение выполняется с использованием стула, скамьи или параллельных брусьев, и оно подходит как для начинающих, так и для опытных спортсменов.

#         ❗ Для правильного выполнения упражнения следует соблюдать следующие правила:\n
#             1. При выполнении упражнения не разводите локти слишком сильно в стороны.\n
#             2. Таз должен находиться близко к скамье или стулу.\n
#             3. Руки находнятся примерно на ширине плеч или чуть шире.\n
#             4. Держите спину прямо.
#     """

# def stream_data_squat():
#     for word in _TEXT_SQUAT.split(" "):
#         yield word + " "
#         time.sleep(0.02)

# def stream_data_push_up():
#     for word in _TEXT_PUSH_UP.split(" "):
#         yield word + " "
#         time.sleep(0.02)
    
# def stream_data_biceps():
#     for word in _TEXT_BICEPS.split(" "):
#         yield word + " "
#         time.sleep(0.02)

# def stream_data_reverse_push_up():
#     for word in _TEXT_REVERSE_PUSH_UP.split(" "):
#         yield word + " "
#         time.sleep(0.02)

# left_column, right_column = st.columns(2)

# if mode == ':basketball: Фронтальные приседания':
#     with left_column:
#         st.image("./assets/frontalniye-prisedaniya.jpeg", width=650)
#     with right_column:
#         st.write_stream(stream_data_squat)
        
#     analyzer = ExerciseAnalyzer('front_squat')

# elif mode == ':basketball: Отжимания с широкой постановкой рук':
#     with left_column:
#         st.image("./assets/push_up.jpg", width=650)
#     with right_column:
#         st.write_stream(stream_data_push_up)

#     analyzer = ExerciseAnalyzer('push_up')

# elif mode == ':basketball: Упражнение с гантелями на бицепс':
#     with left_column:
#         st.image("./assets/biceps.jpg", width=650)
#     with right_column:
#         st.write_stream(stream_data_biceps)

#     analyzer = ExerciseAnalyzer('biceps')

# elif mode == ':basketball: Обратные отжимания':
#     with left_column:
#         st.image("./assets/reverse_push_up.jpg", width=650)
#     with right_column:
#         st.write_stream(stream_data_reverse_push_up)

#     analyzer = ExerciseAnalyzer('reverse_push_up')


# def video_frame_callback(frame: av.VideoFrame):
#     frame = frame.to_ndarray(format="rgb24") 
#     try:
#         frame, correctCount, incorrectCount = analyzer.analyze_video(frame) 
#     except BaseException as b:
#         print(b)
#     return av.VideoFrame.from_ndarray(frame, format="rgb24")

# # def out_recorder_factory() -> MediaRecorder:
# #         return MediaRecorder(output_video_file)


# ctx = webrtc_streamer(
#     key="example",
#     video_frame_callback=video_frame_callback,
#     # rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
#     media_stream_constraints={"video": {"width": {'min':480, 'ideal':480}}, "audio": False},
#     video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False, width=1000)    
#     # out_recorder_factory=out_recorder_factory
# )