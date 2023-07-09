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


path = 'examples/tictactoe/tictactoe.chat'

def load(path):
	return open(path, 'r').readlines()


def commands_to_language(commands, language):
	lines = commands

	memory = ""

	for line in lines:
		data = line.strip('\n')
		
		prompt = (
			"Here is some context for existing code you can use:",
			memory,
			"Now write code that fulfills this command: {}".format(data),
			"Your response should ONLY contain runnable {} code, nothing else.".format(language),
			"Return all the code that should run, including the context code."
			)

		prompt = "\n".join(prompt)
		response = oai_complete(prompt)
		print("#########\n\nProcessed command: {}".format(data))
		print("#########\n\n{}:\n{}\n\n".format(data, response))
		memory = response


	print("#########\n\nRefining code:\n\n{}".format(memory))
	# refine
	commands_str = "\n".join(lines)
	prompt2 = f"We want to accomplish these goals:\n{commands_str}.  This is {language} code that tries to fulfill these goals.\n\n{memory}\n\nRewrite this code so it has no errors and correctly fulfills all the goals.  ONLY return runnable {language} code.  DO NOT return text that is not runnable {language} code."
	refined = oai_complete(prompt2, model="gpt-4")

	if f'```{language}' in refined:
		refined = refined.split('```')[1].strip(f'{language}\n')

	print("#########\n\nRefined code into:\n\n{}".format(memory))
	return refined


def build_plan(code, path, language):
	resp = oai_complete("Give a bash command that compiles the {} file at {}.  For context, the file contains this code {}.  Specify which code is runnable bash with ```bash".format(language, path, code))
	resp2 = resp.split('```bash')[1].split('```')[0].strip()
	return resp2


def compile(src, dest, language):
	code = commands_to_language(open(src), language)

	with open(dest, 'w') as fh:
		fh.write(code)

	compileplan = build_plan(code, dest, language)

	planpath = dest.split('.')[0] + '.sh'
	with open(planpath, 'w') as fh:
		fh.write(compileplan)

	os.system('sh {}'.format(planpath))


compile(path, 'tictactoe.cpp', 'c++')
