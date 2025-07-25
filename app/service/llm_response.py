from langchain.memory import ConversationBufferWindowMemory
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains.conversation.base import ConversationChain
from langchain.prompts import PromptTemplate



class IAresponse:
    def __init__(self, api_key:str, ia_model:str, system_prompt:str, resume_lead:str = ""):
        self.api_key = api_key
        self.ai_model = ia_model
        self.system_prompt = system_prompt

        if resume_lead:
            print("Resumo localizado!")
            response_prompt = """
                historico da conversa:
                {history}

                usuário: {input}
                """
            resume_lead += f"\nresumo de todas as interações que teve com este lead: {resume_lead}"
        else:
            response_prompt = """
                historico da conversa:
                {history}

                usuário: {input}
                """
        
        self.system_prompt += response_prompt
        if not self.ai_model:
            self.ai_model = "gpt-4o-mini"
            
    def generate_response(self, message_lead:str, history_message:list=[]) -> str:
        try:
            chat = ChatOpenAI(model=self.ai_model, api_key=self.api_key)
            memory = ConversationBufferWindowMemory(k=20)
            review_template = PromptTemplate.from_template(self.system_prompt)

            conversation = ConversationChain(
                llm=chat,
                memory=memory,
                prompt=review_template
            )

            # alimentar a memoria da IA com o historico
            if not history_message:
                conversation.memory.chat_memory.add_user_message(message_lead)
            else:
                for msg in history_message:
                    if msg["role"] == "user":
                        conversation.memory.chat_memory.add_user_message(msg.get("content") or "")

                    elif msg["role"] == "assitant":
                        conversation.memory.chat_memory.add_ai_message(msg.get("content") or "")

            print(f"Total de interações: {len(history_message)}")

            resposta = conversation.predict(input=message_lead)

            print(f"Resposta da IA: {resposta}")

            return resposta

        except Exception as ex:
            print(f"Erro ao processar resposta: {ex}")
            return ""
    
    def generate_resume(self, history_message:list=[]) -> str:
        try:
            message = "Gere um resumo detalhado dessa conversa"
            system_prompt = """
            Você é um assistente especializado em resumir conversas com leads. Seu objetivo é identificar, extrair e armazenar de forma clara todos os pontos-chave e informações importantes discutidas durante a conversa. Ao elaborar o resumo, siga estas diretrizes:

            1. **Identificação dos Pontos-Chave:** Extraia os tópicos principais da conversa, incluindo necessidades, interesses, objeções e próximos passos do lead.
            2. **Organização das Informações:** Estruture o resumo de maneira clara e organizada, facilitando a visualização dos dados mais relevantes.
            3. **Foco nas Informações Relevantes:** Certifique-se de que nenhuma informação importante seja omitida. Dados como informações de contato, dúvidas específicas e requisitos do lead devem ser destacados.
            4. **Clareza e Concisão:** O resumo deve ser conciso, mas detalhado o suficiente para fornecer um panorama completo da conversa.
            5. **Privacidade e Segurança:** Garanta que todas as informações sensíveis sejam tratadas com a devida confidencialidade.

            Utilize este prompt para transformar a conversa em um resumo que possibilite um acompanhamento eficaz e estratégico do lead.

            Histórico da conversa:
            {history}
            Usuário: {input}
            """

            chat = ChatOpenAI(model=self.ai_model, api_key=self.api_key)
            memory = ConversationBufferWindowMemory(k=60)
            review_template = PromptTemplate.from_template(system_prompt)
            conversation = ConversationChain(
                llm=chat,
                memory=memory,
                prompt=review_template
            )

            # Alimenta a memória com cada mensagem do histórico
            if not history_message:
                conversation.memory.chat_memory.add_user_message(message)
            else:
                for msg in history_message:

                    #Adicionando memoria do User
                    if msg["role"] == "user":
                        conversation.memory.chat_memory.add_user_message(msg.get("content") or "")
                    
                    #Adicionando memoria da IA
                    elif msg["role"] == "assistant":
                        conversation.memory.chat_memory.add_ai_message(msg.get("content") or "")

            print(f"Total de {len(history_message)} interações")   
            resposta = conversation.predict(input=message)
            print(f"Resposta da IA   : {resposta}")
            
            return resposta
        except Exception as ex:
            print(f"❌ Erro ao processar resposta: {ex}")
            return None