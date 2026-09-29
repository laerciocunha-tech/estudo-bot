from datetime import datetime
import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ativa os logs no terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Função para carregar os erros do arquivo JSON
def carregar_erros():
    try:
        with open("erros.json", "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

# 1. Comando /duvida (Com botões de navegação rápida)
async def duvida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resposta = (
        "🤖 **Central de Ajuda do Grupo Ti Ba/Se** 🚀 \n\n"
        "Aqui você encontra o resumo de todas as soluções: /regras /aplicativos /links /textos /pdv XX /erro XX"
    )
    
    teclado = [
        [
            InlineKeyboardButton("📱 Aplicativos", callback_data="aplicativos"),
            InlineKeyboardButton("📜 Regras", callback_data="regras"),
        ],
        [    
            InlineKeyboardButton("🌍 Links", callback_data="links"),
            InlineKeyboardButton("📝 Textos", callback_data="textos"),
            InlineKeyboardButton("🔓 Senha PDV", callback_data="pdv"),
            InlineKeyboardButton("🚨 Erro Sitef", callback_data="erro"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    await update.message.reply_text(resposta, reply_markup=reply_markup, parse_mode="Markdown")

# 2. Comando /aplicativos
async def aplicativos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resposta = (
        "📱 **Aplicativos Recomendados:**\n\n"
        "• [Essenciais](https://grupomateus-my.sharepoint.com/:f:/r/personal/laercio_cunha_grupomateus_com/Documents/Aplicativos/Programas%20essenciais/Nuvem?d=w322da82ecbd74cff94990d6395205521&csf=1&web=1&e=2MLOwX) - Aplicativos pós formatação.\n"
    )
    await update.message.reply_text(resposta, parse_mode="Markdown", disable_web_page_preview=True)

# 3. Comando /regras
async def regras(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resposta = (
        "📜 **Regras do Grupo:**\n\n"
        "1. Respeite todos os membros.\n"
        "2. Proibido spam ou divulgação sem autorização.\n"
        "3. Mantenha o foco nos temas do grupo."
    )
    await update.message.reply_text(resposta, parse_mode="Markdown")

# 4. Comando /links
async def links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resposta = (
        "🔗 **Links Úteis:**\n\n"
        "• [Maxipos](http://pdv.mateus/maxipos_backoffice/app)\n"
        "• [Gmsuite](https://gmsuite.com.br)\n"
        "• [Trilogo](https://grupomateus.trilogo.app)\n"
        "• [Faturamento](http://faturamento.mateus/login)\n"
        "• [Cloud Prix](https://www.cloudprix.com.br)"
    )
    await update.message.reply_text(resposta, parse_mode="Markdown", disable_web_page_preview=True)

# 5. Comando /textos
async def textos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    resposta = (
        "📄 **Textos e Manuais:**\n\n"
        "• [Documentos](https://grupomateus-my.sharepoint.com/:f:/p/laercio_cunha/IgA3P8lR4XHPTJ--8hPddpVBAZnLYG1iS3UsaOysCHQp06A?e=JYim0f)\n"
    )
    await update.message.reply_text(resposta, parse_mode="Markdown", disable_web_page_preview=True)
    
# 6. Comando /pdv
async def pdv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        numero_pdv = context.args[0]
        hoje = datetime.now()
        data_base = int(f"{hoje.day}{hoje.month}")
        senha_num = data_base + int(numero_pdv)
        
        resposta = f"🔓PDV {numero_pdv}\nSenha: pdv@{senha_num}"
        await update.message.reply_text(resposta)
    else:
        await update.message.reply_text(
            "⚠️ Por favor, informe o número do PDV. Exemplo: `/pdv 999`", 
            parse_mode="Markdown"
        )

# 7. Novo Comando para buscar os erros do Sitef via JSON (ex: /erro 22)
async def erro_sitef(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        codigo_informado = context.args[0]
        
        # Carrega a base de dados do JSON
        erros_base = carregar_erros()
        erro = erros_base.get(codigo_informado)
        
        if erro:
            resposta = (
                f"🚨 Código - {erro['codigo']}\n"
                f"💬 Descrição: {erro['descricao']}\n"
                f"🗣 Ação - {erro['acao']}\n"
                f"🏌️‍♂️Permite retentativa: {erro['retentativa']}\n"
                f"#ErrosSitef"
            )
        else:
            resposta = f"❌ O código `{codigo_informado}` não foi encontrado na base de dados."
            
        await update.message.reply_text(resposta, parse_mode="Markdown")
    else:
        await update.message.reply_text(
            "⚠️ Por favor, informe o código do erro. Exemplo: `/erro 22`", 
            parse_mode="Markdown"
        )

def main():
    TOKEN = "8651236045:AAHPJf9dWkBkEFjAu76E81v2f-bj3qNBUao"
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Registra os comandos
    app.add_handler(CommandHandler("duvida", duvida))
    app.add_handler(CommandHandler("aplicativos", aplicativos))
    app.add_handler(CommandHandler("regras", regras))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("textos", textos))
    app.add_handler(CommandHandler("pdv", pdv))
    app.add_handler(CommandHandler("erro", erro_sitef)) # Comando para consultar os erros
   
    print("🤖 Bot com JSON de erros rodando! Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()