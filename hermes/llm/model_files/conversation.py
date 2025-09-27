import re
from llm.model_files.config import MAX_MESSAGES, MAX_TOKEN_OUTPUT
from llm.model_files.model import llm
from llm.model_files.rag.retriever import retrieve_context


# Adds user's msg to the history
def add_user_message(user_input, conversation_history_list):
    conversation_history_list.append({"role": "user", "content": user_input})
    if len(conversation_history_list) > MAX_MESSAGES:
        conversation_history_list.pop(0)
        
# Builds entire prompt
# def build_prompt(conversation_history_list, app_instructions):
def build_prompt(user_msg, prev_data, app_config):
    
    print(">> >> >> 1 << << <<")

    # Adds initial instructions
    # prompt = app_config["initial_instructions"] + "\n"
    prompt = ""
    if prev_data:
        conv = prev_data["conversation_history_list"]
        
        # asegurar que tenemos una lista
        if not isinstance(prev_data["conversation_history_list"], list):
            conv = []
    # Combines the conversation history. Format: user: ... \n assistant: ...
    # for message in prev_data["conversation_history_list"]:
    #     if message['role'] == 'user':
    #         prompt += f"user: {message['content']}\n"
    #     elif message['role'] == 'assistant':
    #         prompt += f"assistant: {message['content']}\n"

    
    # Adds the last instruction to the assistant, it invites de AI to answer
    # prompt += "assistant:"
    
    # Adds RAG data if it's necessary
    """Genera respuesta del modelo, con o sin RAG"""
    if app_config["rag"]:
        
        # Get the context using RAG
        context = retrieve_context(prompt, app_config["rag"])
        print('CONTEXT OoO')
        print(context)
        print('CONTEXT OoO')
        
        if app_config['lang'] == 'en':
            print(">> >> >> 2 << << <<")
                        
            # Initial Instructions to the System Section
            prompt_system_section = [f"### INSTRUCTIONS:\n{app_config['initial_instructions']}\n\n"]
            prompt_system_section.append(f"### RELEVANT CONTEXT:\n{context}\n\n")
            
            # Add summary (history)
            if prev_data and prev_data['summary']:
                # Title
                prompt_system_section.append(f"### CONVERSATION SUMMARY:: \n\n")
                
                # Summary in the DB
                prompt_system_section.append(f"summary: {prev_data['summary']}")
            
            # Join System msj
            prompt_system_section_string = "\n".join(prompt_system_section)

            # Build the Prompt Array
            prompt_array = [
                {
                    "role": "system",
                    "content": prompt_system_section_string
                }
            ]
            
            # Add previous conversation as context
            if prev_data:
                last_two = conv[-2:]
                
                # Format msgs
                for m in last_two:
                    prompt_array.append({
                        "role": m.get("role", "unknown"),
                        "content": m.get("content", "")
                    })
            
            # Build user msg
            user_msg_obj = {
                "role": "user",
                "content": user_msg
            }
            
            # Add user msg to prompt array
            prompt_array.append(user_msg_obj)
            
            
        elif app_config['lang'] == 'es':
            print(">> >> >> 3 << << <<")
            
            # Initial Instructions to the System Section
            prompt_system_section = [f"### INSTRUCCIONES:\n{app_config['initial_instructions']}\n\n"]
            prompt_system_section.append(f"### CONTEXTO REELEVANTE:\n{context}\n\n")
            
            # Add summary (history)
            if prev_data and prev_data["summary"]:
                # Title    
                prompt_system_section.append(f"### RESUMEN DE LA CONVERSACIÓN:: \n\n")
                
                # Summary in the DB
                prompt_system_section.append(f"summary: {prev_data['summary']}")
            
            # Join System msj
            prompt_system_section_string = "\n".join(prompt_system_section)

            # Build the Prompt Array
            prompt_array = [
                {
                    "role": "system",
                    "content": prompt_system_section_string
                }
            ]
            
            # Add previous conversation as context
            if prev_data:
                last_two = conv[-2:]
                
                # Format msgs
                for m in last_two:
                    prompt_array.append({
                        "role": m.get("role", "unknown"),
                        "content": m.get("content", "")
                    })
            
            # Build user msg
            user_msg_obj = {
                "role": "user",
                "content": user_msg
            }
            
            # Add user msg to prompt array
            prompt_array.append(user_msg_obj)
            
    else:

        # Initial Instructions to the System Section
        prompt_system_section = [f"### INSTRUCCIONES:\n{app_config['initial_instructions']}\n\n"]
        # prompt_system_section.append(f"### CONTEXTO REELEVANTE: \n\n") # No hay
        
        # Add summary (history)
        if prev_data and prev_data["summary"]:
            # Title    
            prompt_system_section.append(f"### RESUMEN DE LA CONVERSACIÓN:: \n\n")
            
            # Summary in the DB
            prompt_system_section.append(f"summary: {prev_data['summary']}")
        
        # Join System msj
        prompt_system_section_string = "\n".join(prompt_system_section)

        # Build the Prompt Array
        prompt_array = [
            {
                "role": "system",
                "content": prompt_system_section_string
            }
        ]
        
        # Add previous conversation as context
        if prev_data:
            last_two = conv[-2:]
            
            # Format msgs
            for m in last_two:
                prompt_array.append({
                    "role": m.get("role", "unknown"),
                    "content": m.get("content", "")
                })
        
        # Build user msg
        user_msg_obj = {
            "role": "user",
            "content": user_msg
        }
        
        # Add user msg to prompt array
        prompt_array.append(user_msg_obj)

        
    return prompt_array

# Calls AI model
def generate_response(prompt):
    
    print('----- ----- ---')
    print('PROMPT, INPUT AL MODELO')
    print(prompt)
    print('----- ----- ---')

    
    outputs = llm.create_chat_completion(
        prompt,
        max_tokens=MAX_TOKEN_OUTPUT,
        temperature=0.7
    )
    

    # generated_text = outputs["choices"][0]["text"]
    generated_text = outputs["choices"][0]["message"]["content"]
    
    print('----- ----- ---')
    print('RESPUESTA, OUTPUT DEL MODELO')
    print(generated_text)
    print('----- ----- ---')
    
    # Looks for the last prefix "assistant:" in the last answer. It prevents a wrong format
    response_start_index = generated_text.rfind("assistant:")
    
    if response_start_index == -1:
        return generated_text.strip()
    
    # Extracs the text after the prefix "assistant:"
    response_text = generated_text[response_start_index + len("assistant:"):].strip()
    
    # Looks for the next user line to cut the answer, it prevents that the model continues the conversation on user's role
    end_of_response_index = response_text.find("user:")
    
    if end_of_response_index != -1:
        response_text = response_text[:end_of_response_index].strip()
        
    return response_text

# Cleans the answer
def cleaning_response(text):
    # Checks if the text finishes with any punctuation mark (. ! ?)
    if re.search(r'[.!?]\s*$', text):
        return text.strip() # If it's complete, it answers without modifying

    # If it isn't complete, it looks for the other senteces with punctuation marks
    sentences = re.findall(r'[^.!?]*[.!?]', text, re.DOTALL)
    
    if sentences:
        # Returns the last completed sentence
        # return sentences[-1].strip()
        
        # Returns all the text without the last incompleted sentence
        return " ".join(sentences).strip()
    else:
        # If there aren't completed sentences, it returns the original text
        return text.strip()

# Adds model's msg to the history
def add_assistant_message(response, conversation_history_list):
    conversation_history_list.append({"role": "assistant", "content": response})
    