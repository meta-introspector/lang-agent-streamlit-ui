sudo docker kill streamlit
sudo docker rm streamlit 
sudo docker run --name streamlit -v /home/mdupont/2024/02/12/streamlit-docker-lang-agent-introspector/:/home/user/app/ -p 8501:8501 streamlit 
