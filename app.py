import os
from typing import Final
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from pesq_access import PesqAccess

######### Variaveis de ambiente
load_dotenv()

TOKEN = os.environ.get("TOKEN")

## Variables and parameters
BOT_USERNAME: Final = '@pesqele_bot'
PARAMS = {
  'root': 'https://pesqele-divulgacao.tse.jus.br',
  'stats_path' : '/app/pesquisa/listarEstatisticos.xhtml',
  'stats_code' : None,
  'html_search' : {
    'input_code_id' : 'formPesquisa:j_id_1m',
    'search_btn_id' : 'formPesquisa:j_id_2a', 
    'table_result_id' : 'formPesquisa:tabelaPesquisas'
  },
  'time_sleeping' : {
    'main_page' : 0.9,
    'query_result' : 3
  }
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Por favor digite seu CONRE:')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Eu sou um robô da Statscon! Basta digitar seu CONRE para que eu possa criar uma tabela.')

## Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    PARAMS['stats_code'] = processed
    pesqac = PesqAccess(PARAMS)

    return pesqac.request_table()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    response: str = handle_response(text)

    await update.message.reply_text(response, parse_mode='Markdown')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(token=TOKEN).build()

    ## Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    ## Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    ## Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=5)

