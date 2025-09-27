import json
import queue
import threading
import logging
from django.utils import timezone
from datetime import timedelta
from chat.models import ConversationHistory
from llm.model_files.conversation import (
    add_user_message, build_prompt,
    generate_response, cleaning_response,
    add_assistant_message
)

# Maximum number of model executions running at the same time
MAX_WORKERS = 1

# Log's configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Init queue
task_queue = queue.Queue()

def worker():
    while True:
        func, args, kwargs, result_holder = task_queue.get()
        try:
            result = func(*args, **kwargs)
            result_holder["result"] = result
        except Exception as e:
            logging.exception("Error en worker")
            result_holder["error"] = str(e)
        finally:
            task_queue.task_done()

# Creates the workers at the beginning
for _ in range(MAX_WORKERS):
    threading.Thread(target=worker, daemon=True).start()

# Adds to queue and init the execution
def enqueue_task(func, *args, wait=True, **kwargs):
    result_holder = {}
    task_queue.put((func, args, kwargs, result_holder))
    logging.info(f"Nueva tarea encolada. Estado: {queue_status()}")  # log

    if wait:  # solo esperar si se necesita el resultado
        task_queue.join()
        if "error" in result_holder:
            raise RuntimeError(f"Tarea falló: {result_holder['error']}")
        return result_holder["result"]

    return None  # no bloquea




# Returns the queue status
def queue_status():
    return {
        "in_queue": task_queue.qsize(),
        "unfinished": task_queue.unfinished_tasks,
        "workers": MAX_WORKERS,
    }

def remove_old_conversations():
    # 1 hour
    limit = timezone.now() - timedelta(hours=1)
    
    # remove conversations
    ConversationHistory.objects.filter(updated_at__lt = limit, user = None).delete()
    
        
# Create summary
def generate_summary(ai_response):
    prev_data = ai_response["prev_data"]
    
    if prev_data:
                
        promp_system_section = {
            "role": "system",
            "content": "### Eres un asistente que únicamente genera resúmenes en 4 o menos oraciones. No respondas como en una conversación"
        }
                
        last_four = prev_data["conversation_history_list"][-4:]
        
        prev_chat = {
            "role": "user",
            "content": f"### RESUMEN HASTA AHORA:\n{prev_data['summary']}\n\n"
                    "### ÚLTIMOS MENSAJES:\n"
                    + "\n".join([f"_: {m['content']}" for m in last_four])
        }

        prompt_array = [promp_system_section, prev_chat]
    
        print("---- Prompt para SUMMARY 444 ----")
        print("---- ----")
        print(prompt_array)
        print("---- ----")

        # Calls AI model
        summary = generate_response(prompt_array)
        
        conversation_history = prev_data["prev_history"]
        conversation_history.summary_text = summary
        conversation_history.save()

# Calls to the model
def invoke_alma(user_msg, token, app_config, user_id = None):
    
    # Remove old conversations
    remove_old_conversations()
    
    # Conversation history
    conversation_history_list = []
    
    prev_data = None
    
    # Look for the history
    prev_history = ConversationHistory.objects.filter(token = token, deleted_at = None).first()
    
    if prev_history:
        conversation_history_list = json.loads(prev_history.content)
        
        
        
        prev_data = {
            "conversation_history_list": conversation_history_list,
            "summary": prev_history.summary_text,
            "prev_history": prev_history
        }

    ## Convertir el json (historial) en la base de datos en un objeto role/content
    
    ## Recuperar últimos dos mensajes intactos
    
    ## Recuperar summary para pasar al modelo
    
    ## Si el historial tiene más de 2 mensajes se crea un summary
    
    ## Crear summary a partir del historial
    
    ## El summary se genera con todos los mensajes
    
    ## Al modelo se le pasan los últimos 2 mensajes intactos + summary
    
    
    # Builds prompt
    prompt = build_prompt(user_msg, prev_data, app_config)
    
    print('----> PROMPT QUE VOY A PASAR AL MODELO <-----')
    print('---- -----')
    print(prompt)
    print('---- -----')
    
    # Calls AI model
    assistant_response = generate_response(prompt)

    # Cuts incomplete sentence
    final_response = cleaning_response(assistant_response)
    
    # Adds user's msg to the history
    add_user_message(user_msg, conversation_history_list)
    
    # Adds model's msg to the history
    add_assistant_message(final_response, conversation_history_list)
    
    # Store history into the DB
    if prev_history:
        prev_history.content = json.dumps(conversation_history_list)
        prev_history.save()
    else:
        ConversationHistory.objects.create(
            token=token,
            content = json.dumps(conversation_history_list),
            user_id=user_id if user_id is not None else None,
        )

    data = {
        "final_response": final_response,
        "prev_data": prev_data
    }
    
    return data
    # return final_response
