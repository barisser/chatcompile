import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']


def oai_complete(prompt, model="gpt-3.5-turbo", context="You are a helpful assistant."):
  response = openai.ChatCompletion.create(
    model=model,
    messages=[
          {"role": "system", "content": context},
          {"role": "user", "content": prompt},
      ]
  )
  return response.choices[0]['message']['content']


path = 'demo.chat'

def load(path):
	return open(path, 'r').readlines()


def commands_to_python(commands):
	lines = commands

	memory = ""


	for line in lines:
		data = line.strip('\n')
		
		prompt = (
			"Here is some context for existing code you can use:",
			memory,
			"Now write code that fulfills this command: {}".format(data),
			"Your response should ONLY contain runnable python code, nothing else."
			)

		prompt = "\n".join(prompt)
		response = oai_complete(prompt)
		print("{}:\n{}\n\n".format(data, response))
		memory += "\n#######\n" + response


	# refine
	commands_str = "\n".join(lines)
	prompt2 = "We want to accomplish these goals:\n{}.  This is python code that tries to fulfill these goals.\n\n{}\n\nRewrite this code so it has no errors and correctly fulfills all the goals.  ONLY return runnable python code.  DO NOT return text that is not runnable python code.".format(commands_str, memory)
	refined = oai_complete(prompt2, model="gpt-4")

	if '```python' in refined:
		refined = refined.split('```')[1].strip('python\n')
	return refined


code = commands_to_python(load(path))

import pdb;pdb.set_trace()

