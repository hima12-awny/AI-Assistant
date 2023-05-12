import openai
import pyttsx3
import speech_recognition as sr


class AIAssistant:
    def __init__(self):
        # Initialize OpenAI API key and GPT language model
        openai.api_key = "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"
        self.model_engine = "gpt-4-0314"

        # Initialize text-to-speech engine and set properties
        self.sound_engine = pyttsx3.init()
        self.sound_engine.setProperty('rate', 150)

        # Initialize speech recognition engine and microphone
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

        # Initialize chat history list
        self.chat_history = []

        # Load chat history from file
        self.readChat()

    def run(self):
        ans = ''
        while 1:
            try:
                # Listen to user input through microphone
                with self.mic as source:
                    print('listening: ')
                    self.recognizer.adjust_for_ambient_noise(source=source, duration=.02)
                    audio = self.recognizer.listen(source)

                # Convert user input to text using Google Speech Recognition API
                ans = self.recognizer.recognize_google(audio)

                # If user says "q", "exit", "ext", or "done", exit the loop
                if ans in ['q', 'exit', 'ext', 'done']:
                    print('ok bye.')
                    break

            except:
                pass

            # Print user input
            print('user:',ans)

            # Generate response using GPT language model
            res = self.generate_response(ans)

            # Print response
            print('assistant:', res)

            # Speak response using text-to-speech engine
            self.sound_engine.say(res)
            self.sound_engine.runAndWait()

            # Add user input and response to chat history
            self.chat_history.append({"role": "user", "content": ans})
            self.chat_history.append({"role": "assistant", "content": res})

            # Print newline for formatting
            print()

        # Save chat history to file
        self.saveChat()

    def readChat(self):
        # Read chat history from file and populate chat history list
        with open('chatHistory.txt', 'r') as dataFile:
            for msg in dataFile.read().split('\n'):
                if len(msg.split(',,')) == 2:
                    self.chat_history.append(
                        {'role': msg.split(',,')[0], 'content': msg.split(',,')[1]}
                    )

    def saveChat(self):
        # Save chat history list to file
        with open('chatHistory.txt', 'w') as dataFile:
            for msg in self.chat_history:
                if msg['content']:
                    dataFile.write(msg['role'] + ",," + msg['content'] + '\n')

    def generate_response(self, message):
        # Add user input to chat history
        self.chat_history.append({"role": "user", "content": message})

        # Generate response using GPT language model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history
        )

        # Get response from GPT language model and add to chat history
        answer = response['choices'][0]['message']['content']
        self.chat_history.append({"role": "assistant", "content": answer})

        # Return response
        return answer
