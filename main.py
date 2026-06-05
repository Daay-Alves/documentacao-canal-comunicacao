import re
import telebot

# Insira aqui o ID do seu grupo ou o @ do seu canal público
ID_CANAL = "@ExemploPIE"
CHAVE_API = "8285282045:AAHa7PSI0UmX5AJz-bIO40GHsMkV2HjcKBc"
search_strings = ['suspeita', 'invadindo', 'roubo' , 'Roubo' ,'ROUBO' , 'roubando']
bot = telebot.TeleBot(CHAVE_API)


def validar_cadastro(id_ctt,lista_ctt = []):
    for i in lista_ctt:
        if(id_ctt == i["Number"]):
            return i
    return -1

def filtrar_string(msg_ctt):
    print("Searching for:", search_strings)
    # Create pattern: 'Python|data|Java'
    pattern = '|'.join(search_strings)
    matches = re.findall(pattern, msg_ctt)

    if matches:
        print(f"Found: {matches}")
        return matches
    else:
        print("No matches found")
        return -1

# Esse gatilho captura QUALQUER mensagem de texto enviada para o bot
@bot.message_handler(func=lambda message: True)
def ouvir_msg(message):
    Contatos = []


    # Retirar esses valores da API
    id_ctt = message.from_user.id  #recebido da API
    msg_ctt = message.text.lower()  #recebido da API
    if str(message.chat.id) == str(ID_CANAL):
        return
    else:
        # executado assim que receber msg
        if (validar_cadastro(id_ctt, Contatos) == -1):
            # implementar codigo de cadatro do usuario
            print("FLUXO: cadastro")

            # responder com msg questionando o endereço para ser cadastrado
            print("responder msg")

            # executar apos msg do usuario com endereço de cadastro
            Contatos.append({"Number": id_ctt,"Name":message.from_user.username, "Adress": msg_ctt})
            for i in filtrar_string(msg_ctt):
                match i:
                    case 'roubo':
                        print("Suspeita roubo")
                        try:

                            # Envia o texto direto para o grupo/canal configurado
                            bot.send_message(ID_CANAL, ("Suspeita de roubo: "+msg_ctt))

                            # Dá um feedback amigável no privado do usuário para ele saber que deu certo
                            bot.reply_to(
                                message, "🚀 Sua mensagem foi enviada para o grupo com sucesso!"
                            )

                        except Exception as e:
                            bot.reply_to(
                                message,
                                "⚠️ Não consegui enviar sua mensagem para o grupo. Verifique as configurações.",
                            )
                            print(f"Erro detalhado: {e}")


                        # inserir logica
                        print("Suspeita")
                    case -1:
                        bot.reply_to(
                            message,
                            "⚠️ Não consegui entender sua mensagem, tente utilizar termos mais claros sobre o relato. Como por exemplo: Roubo, Invasão, Furto, Vandalismo...",
                        )
                        print("Nao foi localizada nenhuma palavra chave")

        else:
            # realizar tratamento de Strings para identificar palavras chave e direcionar ao fluxo correto de resposta
            print("FLUXO: ocorrencia")
            #   necessario analisar string e procurar ocorrencias de uma palavra dentro da msg
            #   será necessario armazenar essas ocorrencias em uma lista e executar uma função com mach en cada uma dessas __
            # ocorrencias e executar codigo correspondente a ocorrencia encontrada

            for i in filtrar_string(msg_ctt):
                match i:
                    case 'roubo' | 'Roubo' | 'ROUBO' | 'roubando':
                        print("Suspeita roubo")
                        try:

                            # Envia o texto direto para o grupo/canal configurado
                            bot.send_message(ID_CANAL, ("Suspeita de roubo: " + msg_ctt))

                            # Dá um feedback amigável no privado do usuário para ele saber que deu certo
                            bot.reply_to(
                                message, "🚀 Sua mensagem foi enviada para o grupo com sucesso!"
                            )

                        except Exception as e:
                            bot.reply_to(
                                message,
                                "⚠️ Não consegui enviar sua mensagem para o grupo. Verifique as configurações.",
                            )
                            print(f"Erro detalhado: {e}")

                        # inserir logica

                    case 'furtando':
                        print("Suspeita furtando")

                    case -1:
                        bot.reply_to(
                            message,
                            "⚠️ Não consegui entender sua mensagem, tente utilizar termos mais claros sobre o relato. Como por exemplo: Roubo, Invasão, Furto, Vandalismo...",
                        )
                        print("Nao foi localizada nenhuma palavra chave")

def  main():
    bot.infinity_polling()
main()