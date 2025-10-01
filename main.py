from me import Me
from resume import load_resume
import gradio as gr


def main():
    print("Hello from agentic-resume!")

    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()

if __name__ == "__main__":
    main()
