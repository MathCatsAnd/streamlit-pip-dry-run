import streamlit as st
from datetime import datetime
import random
import os

with st.sidebar:
    st.markdown('''
    <a href="https://pip-dry-run.streamlit.app/">Python 3.11</a><br/>
    <a href="https://pip-dry-run-py310.streamlit.app/">Python 3.10</a><br/>
    <a href="https://pip-dry-run-py39.streamlit.app/">Python 3.9</a><br/>
    <a href="https://pip-dry-run-py38.streamlit.app/">Python 3.8</a><br/>
    <a href="https://pip-dry-run-py37.streamlit.app/">Python 3.7</a>
    ''', unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state['user'] = datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(1000, 9999))

user = st.session_state.user

def update_pip():
    os.popen('python -m pip install --upgrade pip')

def check_requirements(file):
    with open(user+'requirements.txt', 'wb') as f:
        f.write(file.getbuffer())
    return os.popen(f'pip install -r {user}requirements.txt --dry-run').read()

def clean_up(user):
    os.remove(f'{user}requirements.txt')

if 'version' not in st.session_state:
    st.session_state['version'] = os.popen('python --version').read()

st.title(f'Pip dry-run for {st.session_state["version"]}')

file = st.file_uploader("Upload a file", type="txt")

if file is None:
    st.write('Please Upload a File')
    st.stop()

if file.name != 'requirements.txt':
    st.warning(
        'Your text file should be named "requirements.txt" for Streamlit Cloud '\
        'to install your dependencies correctly. Please rename your file and '\
        're-upload.'
    )
    st.stop()

pip_check = os.popen('pip --version').read()
pip_version = pip_check.split(' ')[1]
pip_version_numbers = pip_version.split('.')
if int(pip_version_numbers[0]) < 23:
    with st.spinner('Updating pip...'):
        update_pip()
    st.experimental_rerun()

with st.spinner('Checking requirements.txt...'):
    result = check_requirements(file)

with st.expander('Complete Output'):
    st.code(result, language=None)

final_line = result.split('\n')[-2]
final_list = final_line.split(' ')
final_list.remove('Would')
final_list.remove('install')
with st.expander('Final Result', expanded=True):
    st.dataframe(final_list)

clean_up(user)