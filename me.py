import json
from resume import load_resume
from openai import OpenAI

from tool_schema import RECORD_UNKNOWN_QUESTION_JSON, RECORD_USER_DETAILS_JSON
from tools import handle_tool_call


class Me:
    def __init__(self):
        self.name = "André Lucas"
        self.role = "Software Engineer"
        self.linkedin = load_resume("me/Profile.pdf", "me/linkedin.txt")
        self.medium = load_resume("me/medium.pdf", "me/medium.txt")
        self.openai = OpenAI()
        self.tools = [
            {"type": "function", "function": RECORD_USER_DETAILS_JSON}, 
            {"type": "function", "function": RECORD_UNKNOWN_QUESTION_JSON}
            ]
    
    def system_prompt(self):
        system_prompt = f"""
        "You are acting as {self.name}. You are answering questions on {self.name}'s  profissional life, \
        particularly questions related to {self.name}'s career, background, skills and experience. \
        Your responsibility is to represent {self.name} for interactions with potential employers, clients and partners. \
        You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
        If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
        If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        You have the following resume:
        {self.linkedin}
        {self.medium}
        """
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False

        while not done:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools
            )

            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True

        return response.choices[0].message.content
        