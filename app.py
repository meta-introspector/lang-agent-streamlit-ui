import os
import sys
import subprocess
from select import select
import streamlit as st
st.title('Welcome to introspector lang_agent!!')



url = st.text_input("url", value="http://localhost:11434")
prompt = st.text_input(
    "prompt", value="Consider this text as a creative writing prompt: ")

source_data = st.selectbox(
    'What data source should we read',
    (
        '/data',
        '/mnt/data1/2024/02/12/meta-coq-common/',
    ))

st.write('You selected:', source_data)

# in python read directory source_data recursivly and print it in select box in streamlit


def get_files(path='.'):
    """Recursive function to find all files in given directory path."""
    files2 = []
    for item in os.listdir(path):
        fp = os.path.join(path, item)
        if os.path.isdir(fp):
            files2.append(fp)
            files2 += get_files(fp)
    return files2


files = get_files(source_data)
limit = st.number_input("limit number of files show", value=40)
if len(files) > limit:
    files = files[0:limit]
# st.write(files)

mode = st.selectbox("mode", [
    "--ollama",
    "--openai",

])
model = st.selectbox("model", ["mistral", "mixtral"])

input_dir = st.selectbox("Select a directory to process", files)
st.write(f"You selected directory: {input_dir}")

if st.button("Process data", key="process"):
    prompt = prompt.replace("\"", "\'")
    cmd = ["bash",
           "./run_agent.sh",
           input_dir,
           url,
           mode,
           model,
           "\"{prompt}\""]
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         )
    readable = {
        p.stdout.fileno(): sys.stdout.buffer,  # log separately
        p.stderr.fileno(): sys.stderr.buffer,
    }
    while readable:
        for fd in select(readable, [], [])[0]:
            data = os.read(fd, 1024)  # read available
            if not data:  # EOF
                del readable[fd]
            else:
                st.write(data.decode("utf-8"))
                readable[fd].write(data)
                readable[fd].flush()

##


def get_out_files(path='.'):
    """Recursive function to find all files in given directory path."""
    files2 = []
    for item in os.listdir(path):
        fp2 = os.path.join(path, item)
        if os.path.isdir(fp2):
            files2.append(fp2)
            files2 += get_out_files(fp2)
        else:
            if fp2.endswith(".test"):
                files2.append(fp2)
                # st.write(fp)
            else:
                # st.write("skip"+fp)
                pass
    return files2


# scan1
if st.button(f"Scan output {input_dir}", key=input_dir):
    st.write('Going to scan')
    outfiles = get_out_files(input_dir)
    if len(outfiles) > limit:
        outfiles = outfiles[0:limit]
        # st.write(outfiles)

        for x in outfiles:
            if os.path.isdir(x):
                pass
            else:
                (p, f) = os.path.split(x)
                with open(x, "r") as fp2:
                    btn = st.download_button(
                        key=x,
                        label="Download text" + x,
                        data=fp2,
                        file_name=f,
                        mime="application/text"
                    )
