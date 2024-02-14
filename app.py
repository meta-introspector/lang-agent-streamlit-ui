import streamlit as st
import pandas as pd
import numpy as np
import os
from glob import glob
import subprocess

st.title('Welcome to introspector lang_agent!!')


limit  = st.number_input("limit",value=40)
url  = st.text_input("url",value="http://localhost:11434")
prompt  = st.text_input("prompt",value="Consider this text as a creative writing prompt: ")

source_data = st.selectbox(
    'What data source should we read',
    (
        '/data',
        '/mnt/data1/2024/02/12/meta-coq-common/',
    ))

st.write('You selected:', source_data)

#in python read directory source_data recursivly and print it in select box in streamlit



def get_files(path='.'):
    """Recursive function to find all files in given directory path."""
    files = []
    for item in os.listdir(path):
        fp = os.path.join(path, item)
        if os.path.isdir(fp):
            files.append(fp)
            files += get_files(fp)
    return files

files = get_files(source_data)
if len(files) > limit:
    files = files[0:limit]
#st.write(files)

mode = st.selectbox("mode", [
    "--ollama",
    "--openai",

])
model = st.selectbox("model", ["mistral","mixtral"])

input_dir = st.selectbox("Select a file", files)
st.write(f"You selected file: {input_dir}")

if st.button("Process data"):
    prompt = prompt.replace("\"","\'")
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
        p.stdout.fileno(): sys.stdout.buffer, # log separately
        p.stderr.fileno(): sys.stderr.buffer,
    }
    while readable:
        for fd in select(readable, [], [])[0]:
            data = os.read(fd, 1024) # read available
            if not data: # EOF
                del readable[fd]
            else:
                st.write(data.decode("utf-8"))
                readable[fd].write(data)
                readable[fd].flush()                   

## 
def get_out_files(path='.'):
    """Recursive function to find all files in given directory path."""
    files = []
    for item in os.listdir(path):
        fp = os.path.join(path, item)
        if os.path.isdir(fp):
            files.append(fp)
            files += get_out_files(fp)
        else:
            if fp.endswith(".test"):
                files.append(fp)
                #st.write(fp)
            else:
                #st.write("skip"+fp)
                pass
    return files


if st.button(f"Scan output {input_dir}"):
    st.write('Going to scan')
    outfiles = get_out_files(input_dir)
    if len(outfiles) > limit:
        outfiles = outfiles[0:limit]
        #st.write(outfiles)

        for x in outfiles:
            if os.path.isdir(x):
                pass
            else:
                (p,f) =os.path.split(x)
                with open(x, "r") as fp:
                    btn = st.download_button(
                        label="Download text" + f,
                        data=fp,
                        file_name=f,
                        mime="application/text"
                    )

                    ###

                    def get_out_files(path='.'):
    """Recursive function to find all files in given directory path."""
    files = []
    for item in os.listdir(path):
        fp = os.path.join(path, item)
        if os.path.isdir(fp):
            files.append(fp)
            files += get_out_files(fp)
        else:
            if fp.endswith(".test"):
                files.append(fp)
                #st.write(fp)
            else:
                #st.write("skip"+fp)
                pass
    return files


if st.button(f"Scan output {input_dir}"):
    st.write('Going to scan')
    outfiles = get_out_files(input_dir)
    if len(outfiles) > limit:
        outfiles = outfiles[0:limit]
        #st.write(outfiles)

        for x in outfiles:
            if os.path.isdir(x):
                pass
            else:
                (p,f) =os.path.split(x)
                with open(x, "r") as fp:
                    btn = st.download_button(
                        label="Download text" + f,
                        data=fp,
                        file_name=f,
                        mime="application/text"
                    )
