verification_timestamp = await verify_user(bot, user_id, token)
if verification_timestamp:
    message = await get_verification_message()
    await bot.send_message(user_id, message)
