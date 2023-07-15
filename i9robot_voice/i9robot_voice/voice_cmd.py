#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import openai
import os
import datetime

# Set OpenAI API key
openai.organization = "org-BTdJvqLmEcoQ7m6h8fFWQd1V"
openai.api_key = os.environ["OPENAI_API_KEY"] #make sure to set your OpenAI account key in bashrc --> export OPENAI_API_KEY = <your private key>
#OPENAI_LN_API_KEY = os.environ["OPEN_API_KET"]
start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

class VoiceCommandNode(Node):
    def __init__(self):
        super().__init__("voice_command_node")
        self.subscription = self.create_subscription(String, "/voice_cmd", self.callback, 50)
        self.publisher = self.create_publisher(String, "/voice_tts", 10)

    # check for specific voice commands, else assume that its a standard voice request to GPT-3
    def callback(self, msg):       
        prompt = msg.data   # get the voice command message into text format
        #self.get_logger().info(prompt)
        if 'apple' in prompt.lower():
            time_text = self.calc_time()
            self.send_voice_tts('the time is ' + time_text)
        elif 'date' in prompt.lower():
            date_text = self.calc_date()
            self.send_voice_tts('the date is ' + date_text)
        elif 'name' in prompt.lower():
            name_text='I dont have a name as yet. I have a wake word. i am an AI robot created by Mr Logan'
            self.send_voice_tts(name_text)
        elif 'move' in prompt.lower():
            name_text='ok. i am moving.'
            self.send_voice_tts(name_text)
        elif 'time' in prompt.lower():
            gpt_output = self.get_chat_gpt3_response(prompt)
            #gpt_output = self.get_gpt_response(prompt)
            self.send_voice_tts(gpt_output)
        else:
            name_text='Please say that again.'
            self.send_voice_tts(name_text)
    
    # send the message to convert text to voice via the /voice_tts topic
    def send_voice_tts(self, text):
        tts_msg = String()
        tts_msg.data = text
        self.get_logger().info(text)
        self.publisher.publish(tts_msg)


    def calc_time(self):
        text_time = datetime.datetime.now().strftime("%H:%M:%S") # Hour = I, Min = M, Sec = S
        return text_time
    
    def calc_date(self):
        text_date = datetime.datetime.now().strftime("%d:%B:%Y")
        return text_date
    
    def get_chat_gpt3_response(self, prompt):
        response = openai.Completion.create(
            #model="gpt-3.5-turbo",
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )
        return response.choices[0].text
    
    # def get_gpt_response(self, prompt, api_key=OPENAI_LN_API_KEY, engine="text-davinci-003", max_tokens=100):
    #     openai.api_key = api_key

    #     try:
    #         # Make a request to the API
    #         response = openai.Completion.create(
    #             engine=engine,
    #             prompt=prompt,
    #             max_tokens=max_tokens
    #         )
    #         return response.choices[0].text.strip()
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return None
        

def main(args=None):
    rclpy.init(args=args)
    voice_command_node = VoiceCommandNode()
    rclpy.spin(voice_command_node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
