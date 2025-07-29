# from os.path import curdir
# from shutil import which
# from tabnanny import check
# import aiosqlite
# from aiogram.client.default import Default
# from sqlalchemy import String, ForeignKey
# from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, async_session
#
# import sqlite3
#
#
#
#







# async def add_user(username, tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         await conn.execute("""
#         INSERT INTO users (tg_id, username, balance, refferals, ban) VALUES (?,?,?,?,?)
#         """, (tg_id, username, 0, 0, 'False'))
#         await conn.commit()
#
# async def check_user(tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT * FROM users WHERE tg_id = ?
#         """, (tg_id,))
#         data = await cursor.fetchone()
#         return data
#
# async def check_balance(tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT balance FROM users WHERE tg_id = ?
#         """, (tg_id,))
#         result = await cursor.fetchone()
#         return result
#
# async def add_balance(tg_id, wl):
#     current_balance = await check_balance(tg_id)
#     async with aiosqlite.connect("../api/models/models.db") as conn:
#         await conn.execute("""
#         UPDATE users SET balance = ? WHERE tg_id = ?
#         """, (wl + current_balance[0], tg_id))
#         await conn.commit()
#
# async def lose_balance(tg_id, stake):
#     current_balance = await check_balance(tg_id)
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         await conn.execute("""
#         UPDATE users SET balance = ? WHERE tg_id = ?
#         """, (current_balance[0] - stake, tg_id))
#         await conn.commit()
#
# async def check_name(tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT name FROM users WHERE tg_id = ?
#         """, (tg_id,))
#         data = await cursor.fetchone()
#         return data[0] if data else None
#
# async def add_name(tg_id, name):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         await conn.execute("""
#         UPDATE users SET name = ? WHERE tg_id = ?
#         """, (name, tg_id))
#         await conn.commit()
#
# async def add_info_game(tg_id, game, value, result, stake):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT username FROM users WHERE tg_id = ?
#         """, (tg_id,))
#         username = (await cursor.fetchone())[0]
#
#         cursor = await conn.execute("""
#         SELECT page FROM history WHERE tg_id = ? GROUP BY page
#         """, (tg_id,))
#         unique_pages = await cursor.fetchall()
#
#         page_counts = {}
#         for page in unique_pages:
#             page_number = page[0]
#             cursor = await conn.execute("""
#             SELECT COUNT(*) FROM history WHERE tg_id = ? AND page = ?
#             """, (tg_id, page_number))
#             count = (await cursor.fetchone())[0]
#             page_counts[page_number] = count
#
#         current_page = 1
#         while current_page in page_counts and page_counts[current_page] >= 6:
#             current_page += 1
#
#         await conn.execute("""
#         INSERT INTO history (tg_id, game, result, value, username, page, stake) VALUES (?,?,?,?,?,?,?)
#         """, (tg_id, game, result, value, username, current_page, stake))
#         await conn.commit()
#
# async def check_info_game(tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT * FROM history WHERE tg_id = ?
#         """, (tg_id,))
#         result = await cursor.fetchall()
#         return result
#
#
#
# async def check_refferals(tg_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         cursor = await conn.execute("""
#         SELECT * FROM refferals WHERE tg_id = ?
#         """, (tg_id,))
#         result = await cursor.fetchall()
#         return result
#
# async def add_refferal(tg_id, ref_id):
#     async with aiosqlite.connect('../api/models/models.db') as conn:
#         await conn.execute("""
#         INSERT INTO refferals (tg_id, refferal) VALUES (?,?)
#         """, (tg_id, ref_id))
#
#         await conn.commit()










