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
			"Your response should ONLY contain runnable python code, nothing else.",
			"Return all the code that should run, including the context code."
			)

		prompt = "\n".join(prompt)
		response = oai_complete(prompt)
		print("{}:\n{}\n\n".format(data, response))
#		memory += "\n#######\n" + response
		memory = response


	# refine
	commands_str = "\n".join(lines)
	prompt2 = "We want to accomplish these goals:\n{}.  This is python code that tries to fulfill these goals.\n\n{}\n\nRewrite this code so it has no errors and correctly fulfills all the goals.  ONLY return runnable python code.  DO NOT return text that is not runnable python code.".format(commands_str, memory)
	refined = oai_complete(prompt2, model="gpt-4")

	if '```python' in refined:
		refined2 = refined.split('```')[1].strip('python\n')


	prompt3 = "remove all non-code text.  Remove all un-asked for examples.  Return only runnable code and python-safe comments\n\n{}".format(refined)
	refined3 = oai_complete(prompt3)

	return refined2


def compile(src, dest, language='python'):
	if language == 'python':
		code = commands_to_python(load(src))
	else:
		raise Exception("Language: {} not supported".format(language))

	with open(dest, 'w') as fh:
		fh.write(code)


compile(path, 'tictactoe.py')
#code1 = commands_to_python(load(path))

#import pdb;pdb.set_trace()

