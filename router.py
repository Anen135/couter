from os import getenv
from dotenv import load_dotenv
from game import Game
from player import Player
from states import GameStates

from aiogram import Dispatcher, Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
router = Router()
game = Game()
dp = Dispatcher()
dp.include_router(router)

def get_user_state(bot: Bot, user_id: int) -> FSMContext:
    return FSMContext( storage=dp.fsm.storage, key=StorageKey(bot.id, user_id, user_id) )
async def send_player_info(bot: Bot):
    for user in game.game_players:
        try:
            await bot.send_message(user.id, f"You: \n{user}")
        except Exception as e:
            print(f"Error on {user.id}: {e}")

# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Hello! I'm a bot created with aiogram.")

@router.message(lambda m: m.text == "/reload_game")
async def reload_game(message: Message):
    game.end_game()
    await message.answer("Game ready!")

@router.message(lambda m: m.text == "/join")
async def join_game(message: Message):
    if game.game_started:
        await message.answer("Game already started!")
        return
    game.game_players.add(Player(message.from_user.id, message.from_user.first_name, game.init_hp))
    await message.answer(f"{message.from_user.first_name} joined the game!")

@router.message(lambda m: m.text == "/start_game")
async def start_game(message: Message, bot : Bot):
    if not game.game_players:
        await message.answer("No players for the game!")
        return
    game.start_game()
    
    await message.answer("Game started!")
    await message.answer(str(game.question))
    for user in game.game_players:
        state = get_user_state(bot, user.id)
        await state.set_state(GameStates.waiting_for_answer)
        try:
            await bot.send_message(user.id, f"You: \n{user}")
        except Exception as e:
            print(f"Error on {user.id}: {e}")

@router.message(GameStates.waiting_for_answer)
async def handle_answer(message: Message, state: FSMContext):
    player = next((p for p in game.game_players if p.id == message.from_user.id), None)
    if not player:
        await message.answer("You are not in the game!")
        return
    player.answer = message.text
    await message.answer(f"Your answer: {message.text}")
    await state.clear()
    
@router.message(lambda m: m.text == "/check_answers")
async def check_answers(message: Message, bot : Bot):
    await message.answer("Checking answers...")
    if any(p.answer == "" for p in game.game_players):
        await message.answer("Not all players answered!")
        return
    game.handle_answers()
    await send_player_info(bot)

@router.message(lambda m: m.text == "/next_question")
async def next_question(message: Message, bot : Bot):
        game.set_random_question()
        await message.answer(str(game.question))
        for user in game.game_players:
            user.answer = ""
            state = get_user_state(bot, user.id)
            await state.set_state(GameStates.waiting_for_answer)
            await bot.send_message(user.id, "You: \n" + str(user))