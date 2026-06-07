import re
import telebot

# Insira aqui o ID do seu grupo ou o @ do seu canal público
ID_CANAL = "@ExemploPIE"
CHAVE_API = "8285282045:AAHa7PSI0UmX5AJz-bIO40GHsMkV2HjcKBc"
search_strings = ['suspeita', 'invadindo', 'roubo' , 'Roubo' ,'ROUBO' , 'roubando', 'roubado','fogo' , 'incendio' 'roubo' ,'roubando' , 'roubado' , 'assalto', 'invadindo' ,'invasao' , 'arrombamento',
                 'suspeito' , 'suspeita' , 'rondando','fogo' , 'incendio','acidente' ,'batida']
bot = telebot.TeleBot(CHAVE_API)
Contatos = {}

#funcao para validar se o contato ja se cadastrou
def validar(message):
    if (message.from_user.id not in Contatos) :
        print("FLUXO: cadastro")
        # Pede o endereço e registra no next_step_handler...
        Contatos[message.from_user.id] = {
            "status": -1,
            "mensagem_pendente": message.text
        }

        bot.reply_to(
            message,
            "Olá! Identifiquei que este é o seu primeiro contato.\n"
            "Já vou enviar seu alerta preciso apenas que me informe seu endereço para vincular a mensagem e realiazar seu cadastro.\n"
            "Peço que responda essa mensagem apenas com o nome da sua rua."
        )
        return -1
    if Contatos[message.from_user.id].get("status") == -1:
        print(f"FLUXO: Salvando endereço")

        Contatos[message.from_user.id]["status"] = 1
        Contatos[message.from_user.id]["Adress"] = message.text

        bot.reply_to(message, "✅ Cadastro realizado com sucesso! Analisando o seu alerta...")
        enviar_alerta(Contatos[message.from_user.id].get("mensagem_pendente"), message)
        return 2

    return 1

#funcao para filtrar a mensagem
def filtrar_string(msg_ctt):

    print("Searching for:", search_strings)
    # Create pattern: 'Python|data|Java'
    pattern = '|'.join(search_strings)
    matches = re.findall(pattern, msg_ctt.lower())

    if matches:
        print(f"Found: {matches}")
        return matches
    else:
        print("No matches found")
        return []

#Funcao para escolher o tipo de ocorrencia com base na mensagem filtrada
def enviar_alerta(msg_ctt,message):
    palavras_encontradas = filtrar_string(msg_ctt)
    if not palavras_encontradas:
        bot.reply_to(
            message,
            "⚠️ Não consegui entender sua mensagem. Tente utilizar termos mais claros como: Roubo, Invasão, Furto, Vandalismo, Fogo..."
        )
        print("Nenhuma palavra-chave localizada.")
        return



    for i in palavras_encontradas:


        match i:
            case 'roubo' | 'roubando' | 'roubado' | 'assalto':
                tipo_alerta = "🚨 SUSPEITA DE ROUBO"
            case 'invadindo' | 'invasao' | 'arrombamento':
                tipo_alerta = "🧱 SUSPEITA DE INVASÃO"
            case 'suspeito' | 'suspeita' | 'rondando':
                tipo_alerta = "👀 ATIVIDADE SUSPEITA"
            case 'fogo' | 'incendio':
                tipo_alerta = "🔥 ALERTA DE INCÊNDIO"
            case 'acidente' | 'batida':
                tipo_alerta = "🚗 ACIDENTE DE TRÂNSITO"
            case _:  # O underline (_) funciona como um "default" para qualquer outra palavra da lista
                tipo_alerta = f"⚠️ ALERTA GERAL ({i.upper()})"

        try:
            endereco = Contatos[message.from_user.id].get("Adress", "Endereço não informado")
            mensagem_final = f"{tipo_alerta}\n📍 Endereço: {endereco}\n📝 Relato: {msg_ctt}"

            bot.send_message(ID_CANAL, mensagem_final)
            bot.reply_to(message, "🚀 Sua mensagem foi enviada para o canal de alertas com sucesso!")

        except Exception as e:
            bot.reply_to(message, "⚠️ Não consegui enviar sua mensagem para o grupo. Verifique as configurações.")
            print(f"Erro detalhado: {e}")

# Esse gatilho captura QUALQUER mensagem de texto enviada para o bot
@bot.message_handler(func=lambda message: True)
def ouvir_msg(message):
    if str(message.chat.id) == str(ID_CANAL):
        return
    else:
        if (validar(message)== 1):
            enviar_alerta(message.text,message)


def  main():
    bot.infinity_polling()
main()