sudo docker kill streamlit
sudo docker rm streamlit
# example for mounting source -v /home/mdupont/2024/02/12/streamlit-docker-lang-agent-introspector/:/home/user/app/
sudo docker run --name streamlit  -p 8501:8501 h4ckermike/lang_agent_streamlit_with_data:meta-coq-utils-data-1-2024-02-12
