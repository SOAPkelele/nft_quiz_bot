from aiogram import types
from loguru import logger

from app.handlers.start import send_language_keyboard
from app.keyboards import MenuKb
from app.misc import i18n
from app.settings import MENU_MESSAGE
from app.utils import delete_message

gettext = i18n.gettext

about_us = gettext("Они пишут о нас")
local_trade_info = f"{about_us}:\n\n" \
                   "<b>ENTREPRENEUR</b>\n" \
                   "https://www.entrepreneur.com/article/388049\n\n" \
                   "<b>FORBES</b>\n" \
                   "https://www.forbes.fr/business/simplifier-le-monde-de-la-finance-decentralisee-le-nouveau-management-de-localtrade/\n\n" \
                   "<b>YAHOO</b>\n" \
                   "https://finance.yahoo.com/news/localtrade-exchange-shares-latest-strategic-175000265.html?guccounter=1\n\n" \
                   "<b>INVESTING</b>\n" \
                   "https://www.investing.com/news/cryptocurrency-news/how-a-crypto-exchange-platform-is-going-global-the-rise-of-localtrade-2591587\n\n" \
                   "<b>VC</b>\n" \
                   "https://vc.ru/u/185546-ikrom-ergashev/290483-mozhet-li-novichok-zarabotat-v-defi-kak-osvoit-6-pribylnyh-instrumentov-dohodnogo-fermerstva\n\n" \
                   "<b>NEWSBTC</b>\n" \
                   "https://www.newsbtc.com/news/company/can-decentralized-finance-become-the-futures-new-digital-economy/\n\n" \
                   "<b>BTCMANAGER</b>\n" \
                   "https://btcmanager.com/localtrades-literacy-crypto-defi/\n\n" \
                   "🌟 Our media 🌟\n" \
                   "Exchange Website - https://localtrade.cc/\n" \
                   "DeFi Lab Website - https://lab.localtrade.cc/\n" \
                   "Community - https://t.me/lt_community\n" \
                   "Telegram Channel - https://t.me/localtradecc\n" \
                   "Twitter - https://twitter.com/LocaltradeC\n" \
                   "Facebook - https://www.facebook.com/localtrade.cc\n" \
                   "Instagram - https://www.instagram.com/localtrade.cc\n" \
                   "LinkedIn - https://www.linkedin.com/company/local-trade/\n" \
                   "Medium - https://blog.localtrade.cc/\n" \
                   "Wiki - https://docs.localtrade.cc/\n" \
                   "YouTube - https://www.youtube.com/CryptoTalkz\n" \
                   "Help center - https://localtradesupport.zendesk.com/"


async def menu_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] requested menu")
    await call.answer(cache_time=60)
    await delete_message(call.message)
    await call.message.answer(MENU_MESSAGE, reply_markup=MenuKb().main(gettext))


async def learn_more_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to learn more about LocalTrade")
    await call.message.edit_text(gettext(local_trade_info),
                                 reply_markup=MenuKb().back_to_menu(gettext),
                                 disable_web_page_preview=True)


async def set_language_handler(call: types.CallbackQuery):
    logger.info(f"User [{call.from_user.id}] wants to change lang")
    await delete_message(call.message)
    await send_language_keyboard(call.message)
