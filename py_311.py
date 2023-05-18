import streamlit as st
import os

def update_pip():
    os.popen('python -m pip install --upgrade pip')

def check_requirements(file):
    with open(file.name, 'wb') as f:
        f.write(file.getbuffer())
    return os.popen('pip install -r requirements.txt --dry-run').read()

file = st.file_uploader("Upload a file", type=("txt"))

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
