import openai
import pyttsx3
import speech_recognition as sr


class AIAssistant:
    def __init__(self):
        # Set up your OpenAI API key
        openai.api_key = "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"
        self.model_engine = "gpt-4-0314"

        self.sound_engine = pyttsx3.init()
        self.sound_engine.setProperty('rate', 150)

        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        self.chat_history = []
        self.readChat()

    def run(self):
        ans = ''
        while 1:
            try:
                with self.mic as source:
                    print('listing: ')
                    self.recognizer.adjust_for_ambient_noise(source=source, duration=.02)
                    audio = self.recognizer.listen(source)

                ans = self.recognizer.recognize_google(audio)

                if ans in ['q', 'exit', 'ext', 'done']:
                    print('ok bye.')
                    break

            except:
                pass

            print('user:',ans)

            res = self.generate_response(ans)
            print('assassinate:', res)

            self.sound_engine.say(res)
            self.sound_engine.runAndWait()
            print()

        self.saveChat()

    def readChat(self):
        with open('chatHistory.txt', 'r') as dataFile:
            for msg in dataFile.read().split('\n'):
                if len(msg.split(',,')) == 2:
                    self.chat_history.append(
                        {'role': msg.split(',,')[0], 'content': msg.split(',,')[1]}
                    )

    def saveChat(self):
        with open('chatHistory.txt', 'w') as dataFile:
            for msg in self.chat_history:
                if msg['content']:
                    dataFile.write(msg['role'] + ",," + msg['content'] + '\n')

    def generate_response(self, message):
        self.chat_history.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history
        )

        answer = response['choices'][0]['message']['content']
        self.chat_history.append({"role": "assistant", "content": answer})
        return answer
