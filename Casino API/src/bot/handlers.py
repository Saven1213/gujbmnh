import asyncio
from idlelib.editor import keynames
from pkgutil import get_data
from random import choice
from time import sleep

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup


from aiogram import Router
import random

from aiogram import F, Router, Bot, types #                 Импорт роутера и F
from aiogram.filters import CommandStart, Command, CommandObject  #    Импорт команды CommandStart и Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton



from src.api.models.requests import check_user, add_user, check_balance, lose_balance, add_balance, check_name, add_name, add_info_game, \
    check_info_game, check_refferals, add_refferal

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext, command: CommandObject):
    username = message.from_user.username
    tg_id = message.from_user.id

    try:
        text = command.text.split(' ')[1]
    except IndexError:
        text = None

    check_reg = await check_user(tg_id)


    find_ref_make = await check_user(text)

    await state.clear()

    if text is not None:
        if text != tg_id:

            if check_reg:
                pass
            else:

                await add_user(username, tg_id)
                await message.answer(f'Вас пригласил - @{find_ref_make[2]}')
                await add_refferal(find_ref_make[1], tg_id)
        else:
            pass



    else:
        if check_reg:
            pass
        else:
            await add_user(username, tg_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Начать', callback_data='main')
        ]
    ])


    await message.answer("""
Добро пожаловать в CASINO777\n\nТут вы проиграете все свои деньги!
    """, reply_markup=keyboard)

@router.callback_query(F.data == 'main')
async def main_page(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Игры', callback_data='games')
        ],
        [
            InlineKeyboardButton(text='Баланс', callback_data='balance')
        ],
        [
            InlineKeyboardButton(text='Профиль', callback_data='profile'),
            InlineKeyboardButton(text='Поддержка', callback_data='support')
        ]
    ])

    await callback.message.edit_text("""
    Проиграй свое очко!
    """, reply_markup=keyboard)

@router.callback_query(F.data == 'support')
async def support(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Написать в поддержку', url='https://t.me/Marinacj')
        ],
        [
            InlineKeyboardButton(text='Дальше проёбывать бабло!', callback_data='main')
        ]
    ])

    await callback.message.edit_text('Вам все равно никто не ответит\n\nХАХАХАХАХАХАХАХАХАХАХ', reply_markup=keyboard)

@router.callback_query(F.data == 'balance')
async def balance(callback: CallbackQuery):
    tg_id = callback.from_user.id
    user_balance = await check_balance(tg_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Пополнить', callback_data='deposit'),
            InlineKeyboardButton(text='Вывести', callback_data='withdraw')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='main')
        ]
    ])

    await callback.message.edit_text(f'Ваш баланс: {user_balance[0]} $', reply_markup=keyboard)

@router.callback_query(F.data == 'games')
async def games(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Угадай число', callback_data='game1'),
            InlineKeyboardButton(text='Рулетка', callback_data='game2')
        ],
        [
            InlineKeyboardButton(text='Камень, Ножницы, Бумага', callback_data='game3'),
            InlineKeyboardButton(text='Счастливый Кубик', callback_data='game4')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='main')
        ]
    ])

    await callback.message.edit_text('Выбери игру', reply_markup=keyboard)

@router.callback_query(F.data == 'game1')
async def guess_the_number(callback: CallbackQuery, state: FSMContext):
    # info_stake = await state.update_data(stake=10)
    info_stake = await state.get_data()

    stake_dict = info_stake.get('stake', {}).copy()

    if 'stake_gn' not in stake_dict:
        stake_dict['stake_gn'] = 10

        await state.update_data(stake=stake_dict)


    tg_id = callback.from_user.id

    balancee = await check_balance(tg_id)


    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(1,7,2):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=str(i), callback_data=f'gn_{str(i)}'),
            InlineKeyboardButton(text=str(i+1), callback_data=f'gn_{str(i+1)}')
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Размер ставки', callback_data='count_stake_gn'),

    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='games')
    ])

    info = await state.get_data()

    current_stake_gn = stake_dict['stake_gn']

    await callback.message.edit_text(f'Ваша ставка: {current_stake_gn}\n\nБаланс: {balancee[0]} $\n\nНажмите на любое число', reply_markup=keyboard)

@router.callback_query(F.data.startswith('gn'))
async def sel_num(callback: CallbackQuery, state: FSMContext):
    data = callback.data.split('_')[1]

    await callback.message.delete()


    info_stake = await state.get_data()

    stake = info_stake['stake']['stake_gn']

    tg_id = callback.from_user.id

    keyboard_if_not_bal = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Баланс', callback_data='balance'),
            InlineKeyboardButton(text='В главное меню', callback_data='main')
        ]
    ])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Ещё', callback_data='game1')
        ],
        [
            InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main')
        ]
    ])





    user_balance = await check_balance(tg_id)
    user_balance = user_balance[0]
    # print(f'Баланс: {user_balance}')
    # print(f'Ставка: {stake}')

    if user_balance >= stake:
        dice_message = await callback.message.answer_dice()

        await lose_balance(tg_id, stake)

        # random_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]



        await asyncio.sleep(2)








        # bot_select = random.choice(random_list)


        bot_select = dice_message.dice.value



        if int(data) == int(bot_select):
            win_result = stake*6
            try:

                await dice_message.edit_text(f'Поздравляю!!! Вы выиграли {win_result}', reply_markup=keyboard)


            except Exception:

                await callback.message.answer(f'Поздравляю!!! Вы выиграли {win_result}', reply_markup=keyboard)
                await add_info_game(tg_id, 'gn', win_result, 'win', stake)

            finally:
                await add_balance(tg_id, stake*6)
        else:
            try:

                await callback.dice_message.edit_text(f'Увы, но у бота {bot_select}', reply_markup=keyboard)
                await add_info_game(tg_id, 'gn', stake - stake * 2, 'lose', stake)

            except Exception:

                await callback.message.answer(f'Увы, но у бота {bot_select}', reply_markup=keyboard)
                await add_info_game(tg_id, 'gn', stake - stake * 2, 'lose')

    else:
        await callback.message.answer('К сожалению у вас не хватает средств чтобы сделать ставку\n\nПополните баланс и мы ждем вас снова!', reply_markup=keyboard_if_not_bal)


class Gn(StatesGroup):
    value_st = State()



@router.callback_query(F.data == 'count_stake_gn')
async def count_stake(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите размер ставки')

    await state.set_state(Gn.value_st)


@router.message(Gn.value_st)
async def enter_stake(message: Message, state: FSMContext):
    text = message.text

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])

    for i in range(1, 7, 2):
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=str(i), callback_data=f'gn_{str(i)}'),
            InlineKeyboardButton(text=str(i + 1), callback_data=f'gn_{str(i + 1)}')
        ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Размер ставки', callback_data='count_stake'),

    ])
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='games')
    ])

    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='game1')
        ]
    ])

    try:
        stake_amount = int(text)
        if stake_amount < 10:
            await message.answer(
                'Минимальная ставка - 10 $', reply_markup=keyboard_back)
            return
    except ValueError:
        await message.answer('Некорректный ввод. Пожалуйста, введите числовое значение для ставки.', reply_markup=keyboard_back)
        return

    await state.update_data(stake={'stake_gn': stake_amount})

    await message.answer(f'Ваша ставка: {text}\n\nНажмите на любое число', reply_markup=keyboard)




@router.callback_query(F.data == 'game3')
async def skp(callback: CallbackQuery, state: FSMContext):

    current_fsm_data = await state.get_data()

    tg_id = callback.from_user.id


    balancee = await check_balance(tg_id)

    stake_dict = current_fsm_data.get('stake', {}).copy()


    if 'stake_skp' not in stake_dict:
        stake_dict['stake_skp'] = 10

        await state.update_data(stake=stake_dict)


        current_stake_skp = stake_dict['stake_skp']
    else:
        current_stake_skp = current_fsm_data['stake']['stake_skp']








    # n_data = await state.get_data()
    #
    # print(n_data)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Камень', callback_data='skpg_stone'),
            InlineKeyboardButton(text='Ножницы', callback_data='skpg_scissors')
        ],
        [
            InlineKeyboardButton(text='Бумага', callback_data='skpg_paper')
        ],
        [
            InlineKeyboardButton(text='Размер ставки', callback_data='stake_count_skp')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='main')
        ]
    ])


    await callback.message.edit_text(f'Ставка: {current_stake_skp}\n\nБаланс: {balancee[0]} $\n\nВыбери действие!', reply_markup=keyboard)


class Skp(StatesGroup):
    value_st = State()

@router.callback_query(F.data == 'stake_count_skp')
async def count_skp(callback: CallbackQuery, state: FSMContext):

    await state.set_state(Skp.value_st)

    await callback.message.edit_text('Введите размер ставки\n\nМинимальная ставка - 10 $')

@router.message(Skp.value_st)
async def count_skp_2(message: Message, state: FSMContext):
    msg = message.text

    tg_id = message.from_user.id


    keyboard_if_not_bal = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Баланс', callback_data='balance'),
            InlineKeyboardButton(text='Назад', callback_data='game3')
        ]

    ])


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Камень', callback_data='skpg_stone'),
            InlineKeyboardButton(text='Ножницы', callback_data='skpg_scissors')
        ],
        [
            InlineKeyboardButton(text='Бумага', callback_data='skpg_paper')
        ],
        [
            InlineKeyboardButton(text='Размер ставки', callback_data='stake_count_skp')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='main')
        ]
    ])

    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='game3')
        ]
    ])

    balancee = await check_balance(tg_id)

    balancee = balancee[0]



    stake_amount = int(msg)
    if stake_amount <= balancee:

        try:


                if stake_amount < 10:
                    await message.answer(
                        'Минимальная ставка - 10 $', reply_markup=keyboard_back)
                    return

        except ValueError:
            await message.answer('Некорректный ввод. Пожалуйста, введите числовое значение для ставки.', reply_markup=keyboard_back)
            return
    else:

        await message.answer(f'Ставка не может быть больше чем ваш баланс!\n\nВаш баланс {balancee} $', reply_markup=keyboard_if_not_bal)
        return



    await state.update_data(stake={'stake_skp': stake_amount})

    await message.answer(f'Выберите действие!\n\nВаша ставка: {stake_amount}', reply_markup=keyboard)

@router.callback_query(F.data.split('_')[0] == 'skpg')
async def logic_game3(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id

    balancee = await check_balance(tg_id)
    balancee = balancee[0]

    fsm = await state.get_data()

    stake = fsm['stake']['stake_skp']




    keyboard_if_not_bal = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Баланс', callback_data='balance')
        ],
        [
            InlineKeyboardButton(text='В главное меню', callback_data='main')
        ]
    ])




    if balancee >= stake:





        await lose_balance(tg_id, stake)

        data = callback.data.split('_')[1]

        game_list = ['scissors', 'paper', 'stone']

        choice_bot = random.choice(game_list)

        fsm = await state.get_data()

        stake = fsm['stake']['stake_skp']

        if data == 'scissors' and choice_bot == 'scissors':
            #Draw

            win = 'Ничья'

        elif data == 'scissors' and choice_bot == 'stone':
            win = 'Бот'
        elif data == 'scissors' and choice_bot == 'paper':

            win = 'Вы'

        elif data == 'paper' and choice_bot == 'paper':

            win = 'Ничья'

        elif data == 'paper' and choice_bot == 'scissors':

            win = 'Бот'

        elif data == 'paper' and choice_bot == 'stone':

            win = 'Вы'

        elif data == 'stone' and choice_bot == 'stone':

            win = 'ничья'

        elif data == 'stone' and choice_bot == 'paper':

            win = 'Бот'

        elif data == 'stone' and choice_bot == 'scissors':
            win = 'Вы'


        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Ещё', callback_data='game3')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='main')
            ]
        ])

        win_result = float(stake) * 1.5


        if data == 'scissors':
            user_item = 'Ножницы'
        elif data == 'stone':
            user_item = 'Камень'
        elif data == 'paper':
            user_item = 'Бумага'

        if choice_bot == 'scissors':
            bot_item = 'Ножницы'

        elif choice_bot == 'stone':
            bot_item = 'Камень'

        elif choice_bot == 'paper':
            bot_item = 'Бумага'

        if win.lower() == 'вы':




            await callback.message.edit_text(f'Вы выиграли {win_result} $! \n\nУ вас {user_item}\n\nУ бота {bot_item}', reply_markup=keyboard)
            await add_balance(tg_id, win_result)
            await add_info_game(tg_id, 'skp', win_result, 'win', stake)

        elif win.lower() == 'ничья':

            await callback.message.edit_text(f'Ничья! вы с ботом выбросили: {bot_item}', reply_markup=keyboard)
            await add_balance(tg_id, stake)
            await add_info_game(tg_id, 'skp', str(0), 'draw', stake)
            # print(stake)


        else:
            stakex2 = stake * 2
            await callback.message.edit_text(f'Увы, вы проиграли {int(stake)} $\n\nУ вас {user_item}\n\nУ бота {bot_item}', reply_markup=keyboard)
            await add_info_game(tg_id, 'skp', stake - stakex2, 'lose', stake)
            # print(stake)

    else:
        await callback.message.edit_text('На вашем счете не хватает средств! Пополните баланс и возвращайтесь', reply_markup=keyboard_if_not_bal)

@router.callback_query(F.data == 'profile')
async def prof(callback: CallbackQuery):

    tg_id = callback.from_user.id

    name_data = await check_name(tg_id)

    if name_data:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='История игр', callback_data='games_history-1')
            ],
            [
                InlineKeyboardButton(text='Реффералы', callback_data='refferals')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='main')
            ]

        ])



        await callback.message.edit_text(f'Добро пожаловать, {name_data}!', reply_markup=keyboard)

    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[

            [
                InlineKeyboardButton(text='Добавить уникальное имя', callback_data='add_name')
            ],
            [
                InlineKeyboardButton(text='История игр', callback_data='games_history-1')
            ],
            [
                InlineKeyboardButton(text='Реффералы', callback_data='refferals')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='main')
            ]

        ])


        await callback.message.edit_text('Ваш профиль!', reply_markup=keyboard)

class Name(StatesGroup):
    name = State()

@router.callback_query(F.data == 'add_name')
async def add_nm(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Name.name)

    await callback.message.answer('Введите ваш никнейм')

@router.message(Name.name)
async def enter_name(message: Message):

    msg = message.text

    tg_id =  message.from_user.id

    await add_name(tg_id, msg)


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Вернуться в меню', callback_data='profile')
        ]
    ])

    await message.answer(f'Ваш никнейм {msg}', reply_markup=keyboard)

@router.callback_query(F.data == 'games_history-1')
async def ghistory(callback: CallbackQuery):
    tg_id = callback.from_user.id
    rg = await check_info_game(tg_id)  # result_games

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='profile')]
    ])

    page_list = []
    data = callback.data.split('-')[1]

    try:
        for i in rg:
            if i[-1] == 1:
                page_list.append(i)

        for info in page_list:
            if info[3].lower() == 'win':
                text = 'Выигрыш✅'
            elif info[3].lower() == 'lose':
                text = 'Поражение❌'
            elif info[3].lower() == 'draw':
                text = 'Ничья〽️'
            else:
                text = 'Непонятный результат'

            keyboard.inline_keyboard.append([InlineKeyboardButton(text=f'Игра {info[2]} -- {info[4]} $ | {text}',  callback_data=f'info_game-{info[0]}')])

    except IndexError:
        await callback.message.edit_text('Вы не сыграли ещё ни одной игры!', reply_markup=keyboard_back)
        return

    if not page_list:
        await callback.message.edit_text('Вы не сыграли пока ни одной игры!', reply_markup=keyboard_back)
        return

    # pages = check_info_game(tg_id)
    #
    # try:
    #     last_page = pages[-1][-1]
    # except IndexError:
    #     last_page = pages[-1]





    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='⏪', callback_data=f'last_page_history-{int(data) - 1}'),
        InlineKeyboardButton(text='⏩', callback_data=f'next_page_history-{int(data) + 1}')
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text='Назад', callback_data='profile')
    ])

    try:
         await callback.message.edit_text(f'Ваши игры\n\nстраница: {data}', reply_markup=keyboard)

    except TelegramBadRequest:

        pass

@router.callback_query(F.data.startswith('last_page_history'))
async def last_page_h(callback: CallbackQuery):
    data = callback.data.split('-')[1]

    if int(data) <= 1:
        pass

    else:

        tg_id = callback.from_user.id

        info_game = await check_info_game(tg_id)

        item_lst = []

        keyboard = InlineKeyboardMarkup(inline_keyboard=[])

        for game in info_game:
            try:
                if game[-1] == int(data):
                    item_lst.append(game)
                else:
                    pass

            except IndexError:
                pass

        for info in item_lst:
            if info[3].lower() == 'win':
                text = 'Выигрыш✅'
            elif info[3].lower() == 'lose':
                text = 'Поражение❌'
            elif info[3].lower() == 'draw':
                text = 'Ничья〽️'
            else:
                text = 'Непонятный результат'









            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text=f'Игра {info[2]} -- {info[4]} $ | {text}', callback_data=f'info_game-{info[0]}')
            ])


        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='⏪', callback_data=f'last_page_history-{int(data) - 1}'),
            InlineKeyboardButton(text='⏩', callback_data=f'next_page_history-{int(data) + 1}')
        ])

        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Назад', callback_data='profile')
        ])

        await callback.message.edit_text(f'Ваши игры\n\nстраница: {data}', reply_markup=keyboard)

@router.callback_query(F.data.startswith('next_page_history'))
async def last_page_h(callback: CallbackQuery):
    data = callback.data.split('-')[1]

    tg_id = callback.from_user.id

    info_game = await check_info_game(tg_id)

    try:
        if int(data) == info_game[-1][-1]:

            pass

        else:





            item_lst = []

            keyboard = InlineKeyboardMarkup(inline_keyboard=[])

            for game in info_game:
                try:
                    if game[-1] == int(data):
                        item_lst.append(game)

                    else:
                        pass

                except IndexError:
                    pass



            for info in item_lst:
                if info[3].lower() == 'win':
                    text = 'Выигрыш✅'
                elif info[3].lower() == 'lose':
                    text = 'Поражение❌'
                elif info[3].lower() == 'draw':
                    text = 'Ничья〽️'
                else:
                    text = 'Непонятный результат'


                keyboard.inline_keyboard.append([
                    InlineKeyboardButton(text=f'Игра {info[2]} -- {info[4]} $ | {text}', callback_data=f'info_game-{info[0]}')
                ])

            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text='⏪', callback_data=f'last_page_history-{int(data) - 1}'),
                InlineKeyboardButton(text='⏩', callback_data=f'next_page_history-{int(data) + 1}')
            ])

            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text='Назад', callback_data='profile')
            ])

            await callback.message.edit_text(f'Ваши игры\n\nстраница: {data}', reply_markup=keyboard)
    except IndexError:
        pass

@router.callback_query(F.data == 'refferals')
async def refferals_menu(callback: CallbackQuery):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Просмотреть моих реффералов', callback_data='my_refferals')
        ],
        [
            InlineKeyboardButton(text='Личная рефферальная ссылка', callback_data='refferal_link')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='profile')
        ]
    ])
    await callback.message.edit_text('Тут ты сможешь приглашать друзей и знакомых и получать за это вознаграждение!\n\n<blockquote><code>1 человек - 1 $\n\n2 человека - 3 $\n\n3 человека - 5 $\n</code></blockquote>\n\n\n❗️Важно❗️\nРефферал должен сделать оборот на сумму 100 $ чтобы получить вознаграждение', parse_mode='HTML', reply_markup=keyboard)

@router.callback_query(F.data == 'my_refferals')
async def refferals(callback: CallbackQuery):
    tg_id = callback.from_user.id

    refferal_list = await check_refferals(tg_id)

    if refferal_list:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        if len(refferal_list) > 1:
            for refferal in refferal_list:

                id_r = refferal[2]

                user = await check_user(id_r)

                keyboard.inline_keyboard.append([
                    InlineKeyboardButton(text=f'@{user[2]}', callback_data=f'ref_user-{user[0]}')
                ])


        else:
            id_r = refferal_list[0][2]

            user = await check_user(id_r)

            keyboard.inline_keyboard.append([
                InlineKeyboardButton(text=f'@{user[2]}', callback_data=f'ref_user-{user[1]}')
            ])
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text='Назад', callback_data='refferals')
        ])

        await callback.message.edit_text('Ваши реффералы: ', reply_markup=keyboard)

    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Личная рефферальная ссылка', callback_data='refferal_link')
            ],
            [
                InlineKeyboardButton(text='Назад', callback_data='refferals')
            ]
        ])

        await callback.message.edit_text('У вас пока нет реффералов', reply_markup=keyboard)

@router.callback_query(F.data == 'refferal_link')
async def ref_link(callback: CallbackQuery):

    tg_id = callback.from_user.id

    refferal_link = f'https://t.me/loodplace_bot?start={tg_id}'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='refferals')
        ]
    ])

    await callback.message.edit_text(f'Ваша рефферальная ссылка <blockquote><code>{refferal_link}</code></blockquote>', parse_mode='HTML', reply_markup=keyboard)




@router.callback_query(F.data.startswith('ref_user'))
async def refur(callback: CallbackQuery):

    data = callback.data.split('-')[1]

    user = await check_user(data)

    gamess = await check_info_game(data)
    # print(gamess)
    summ_stake = 0

    for i in gamess:
        if i is not None and i[-1] is not None:
            summ_stake += i[-1]

    len_games = len(gamess) if gamess is not None else 0

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='refferals')
        ]
    ])

    await callback.message.edit_text(f'Пользователь - @{user[2]}\n\nСыграно игр - {len_games} || на сумму {summ_stake} $', reply_markup=keyboard)
























